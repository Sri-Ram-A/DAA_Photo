import os
import shutil # For cleaning up temp step images
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageOps # ImageDraw for highlighting
import numpy as np
from scipy.fftpack import dct
import matplotlib
matplotlib.use('Agg') # Use Agg backend for Matplotlib to avoid GUI issues on servers
import matplotlib.pyplot as plt

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
# Subfolder for temporary step images, relative to UPLOAD_FOLDER
# We'll serve images from here directly
TEMP_STEPS_SUBFOLDER = 'temp_step_images'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
HASH_SIZE = 8
HIGH_FREQ_FACTOR = 4
RESIZE_DIM = HASH_SIZE * HIGH_FREQ_FACTOR

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Path for serving step images: UPLOAD_FOLDER/TEMP_STEPS_SUBFOLDER
app.config['STEP_IMAGES_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], TEMP_STEPS_SUBFOLDER)
app.config['SECRET_KEY'] = 'your_very_secret_key_for_session_v3_gray' # Changed key
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ensure upload and step image directories exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['STEP_IMAGES_FOLDER']):
    os.makedirs(app.config['STEP_IMAGES_FOLDER'])


# --- Helper Function for Allowed Files ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Perceptual Hash Logic ---
EDUCATIONAL_OUTPUT_MODE = 'WEB' # 'CONSOLE', 'WEB', 'NONE'

def _get_step_image_savename(base_filename, step_name, orientation_name_safe):
    """Generates a unique filename for a step image."""
    return f"{secure_filename(base_filename)}_{orientation_name_safe}_{step_name}.png"

def _log_educational_step(message, image_url=None, base_filename=None, orientation_name_safe=""):
    """Logs educational steps, now can include an image URL."""
    if EDUCATIONAL_OUTPUT_MODE == 'CONSOLE' or EDUCATIONAL_OUTPUT_MODE == 'WEB':
        print(message)
        if image_url:
            print(f"  Image: {image_url}")

    if EDUCATIONAL_OUTPUT_MODE == 'WEB':
        if 'educational_log' not in session:
            session['educational_log'] = []
        log_entry = {"text": message}
        if image_url:
            log_entry["image_url"] = url_for('serve_step_image', filename=os.path.basename(image_url))
        session['educational_log'].append(log_entry)
        session.modified = True

def _clear_temp_step_images(base_filename, orientation_name_safe="all"):
    """Clears temporary step images for a given base filename and orientation, or all."""
    if not os.path.exists(app.config['STEP_IMAGES_FOLDER']):
        return
    for item in os.listdir(app.config['STEP_IMAGES_FOLDER']):
        prefix_to_match = secure_filename(base_filename)
        if orientation_name_safe != "all":
            prefix_to_match += f"_{orientation_name_safe}_"
        if item.startswith(prefix_to_match):
            try:
                os.remove(os.path.join(app.config['STEP_IMAGES_FOLDER'], item))
            except Exception as e:
                print(f"Warning: Could not remove temp step image {item}: {e}")


def _calculate_single_phash(image_obj, orientation_name="Image", base_filename_for_steps="temp"):
    """
    Calculates a single pHash. Now saves and logs intermediate images.
    base_filename_for_steps is used to name the saved step images.
    """
    orientation_name_safe = secure_filename(orientation_name.replace(" ", "_").replace("°", "deg"))
    step_img_path = None

    _log_educational_step(f"\n--- [{orientation_name}] Starting pHash Calculation ---",
                          base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)

    # 1. Resize Image
    resized_image = image_obj.resize((RESIZE_DIM, RESIZE_DIM), Image.Resampling.LANCZOS)
    step_img_savename = _get_step_image_savename(base_filename_for_steps, "resized", orientation_name_safe)
    step_img_path = os.path.join(app.config['STEP_IMAGES_FOLDER'], step_img_savename)
    resized_image.save(step_img_path)
    _log_educational_step(f"[{orientation_name}] Step 1: Resized to {RESIZE_DIM}x{RESIZE_DIM} pixels.",
                          image_url=step_img_path, base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)

    # 2. Convert to Grayscale
    grayscale_image = resized_image.convert("L")
    step_img_savename = _get_step_image_savename(base_filename_for_steps, "grayscale", orientation_name_safe)
    step_img_path = os.path.join(app.config['STEP_IMAGES_FOLDER'], step_img_savename)
    grayscale_image.save(step_img_path)
    _log_educational_step(f"[{orientation_name}] Step 2: Converted to Grayscale.",
                          image_url=step_img_path, base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)

    # 3. DCT
    image_array = np.array(grayscale_image, dtype=float)
    dct_coeffs_rows = dct(image_array, type=2, norm='ortho', axis=1)
    _log_educational_step(f"[{orientation_name}] Step 3a: DCT - Applied row-wise transform.",
                          base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)
    dct_coeffs_full = dct(dct_coeffs_rows, type=2, norm='ortho', axis=0)
    _log_educational_step(f"[{orientation_name}] Step 3b: DCT - Applied column-wise. Full 2D DCT coefficients obtained.",
                          base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)

    # 4. Reduce DCT and Visualize
    dct_reduced = dct_coeffs_full[:HASH_SIZE, :HASH_SIZE]
    plt.figure(figsize=(4,4)) # Matplotlib figure size
    # CHANGED cmap to 'gray' for grayscale DCT visualization
    plt.imshow(np.log(np.abs(dct_reduced) + 1e-9), cmap='gray', interpolation='nearest')
    plt.title(f"Reduced DCT ({HASH_SIZE}x{HASH_SIZE})", fontsize=8)
    plt.xticks([])
    plt.yticks([])
    step_img_savename = _get_step_image_savename(base_filename_for_steps, "dct_reduced_viz", orientation_name_safe)
    step_img_path = os.path.join(app.config['STEP_IMAGES_FOLDER'], step_img_savename)
    plt.savefig(step_img_path, bbox_inches='tight')
    plt.close()
    _log_educational_step(f"[{orientation_name}] Step 4: DCT - Reduced to top-left {HASH_SIZE}x{HASH_SIZE} low-frequency coefficients (visualization below).",
                          image_url=step_img_path, base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)

    # Visualize 8x8 area on grayscale image
    img_with_highlight = grayscale_image.copy().convert("RGB")
    draw = ImageDraw.Draw(img_with_highlight)
    highlight_size_on_resized_img = HASH_SIZE
    draw.rectangle([(0,0), (highlight_size_on_resized_img-1, highlight_size_on_resized_img-1)], outline="red", width=1)
    step_img_savename = _get_step_image_savename(base_filename_for_steps, "grayscale_highlighted", orientation_name_safe)
    step_img_path = os.path.join(app.config['STEP_IMAGES_FOLDER'], step_img_savename)
    img_with_highlight.save(step_img_path)
    _log_educational_step(f"[{orientation_name}] Illustrative: Top-left {HASH_SIZE}x{HASH_SIZE} area of the {RESIZE_DIM}x{RESIZE_DIM} grayscale image (related to DCT focus).",
                          image_url=step_img_path, base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)

    # 5. Compute Median
    ac_coeffs = dct_reduced.flatten()[1:]
    median_val = np.median(ac_coeffs)
    _log_educational_step(f"[{orientation_name}] Step 5: Calculated median of AC DCT coefficients: {median_val:.2f}.",
                          base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)

    # 6. Binarize
    binary_fingerprint_matrix = (dct_reduced >= median_val)
    _log_educational_step(f"[{orientation_name}] Step 6: Binarized coefficients against median -> {HASH_SIZE*HASH_SIZE}-bit fingerprint matrix.",
                          base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)

    # 7. Construct Hash
    binary_hash_string = "".join(binary_fingerprint_matrix.flatten().astype(int).astype(str))
    hex_length = (HASH_SIZE * HASH_SIZE) // 4
    hash_value_int = int(binary_hash_string, 2)
    hex_hash = f"{hash_value_int:0{hex_length}x}"
    _log_educational_step(f"[{orientation_name}] Step 7: Constructed Hex Hash for this orientation: {hex_hash}.",
                          base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)
    _log_educational_step(f"--- [{orientation_name}] Finished pHash Calculation ---",
                          base_filename=base_filename_for_steps, orientation_name_safe=orientation_name_safe)
    return hex_hash


def perceptual_hash_robust(image_path, original_filename):
    _clear_temp_step_images(original_filename, orientation_name_safe="all")
    try:
        img = Image.open(image_path)
        if img.mode == 'RGBA' or img.mode == 'P':
            img = img.convert('RGB')
    except Exception as e:
        _log_educational_step(f"ERROR: Could not load image for hashing: {e}")
        return None

    _log_educational_step(f"\n===== Starting Robust Perceptual Hash for: {original_filename} =====")
    _log_educational_step(f"Goal: Generate a {HASH_SIZE*HASH_SIZE}-bit hash robust to rotation/mirroring.")

    orientations_data = [
        ("Original", img.copy()),
        ("Rotated 90 deg", img.copy().rotate(90, expand=True)),
        ("Mirrored Original", ImageOps.mirror(img.copy())),
    ]

    candidate_hashes = []
    _log_educational_step("\n--- Processing Different Orientations (showing detailed steps for some) ---")
    for name, current_img_obj in orientations_data:
        phash = _calculate_single_phash(current_img_obj,
                                        orientation_name=name,
                                        base_filename_for_steps=original_filename)
        if phash:
            candidate_hashes.append(phash)
        else:
            _log_educational_step(f"WARNING: Failed to get hash for orientation: {name}")

    if not candidate_hashes:
        _log_educational_step("ERROR: No valid hashes generated from any orientation.")
        return None

    canonical_hash = min(candidate_hashes)
    _log_educational_step("\n--- Canonical Hash Selection ---")
    _log_educational_step(f"Candidate hashes from processed orientations: {candidate_hashes}")
    _log_educational_step(f"FINAL CANONICAL HASH (smallest of candidates): {canonical_hash}")
    _log_educational_step(f"=======================================================")
    return canonical_hash

# --- Flask Routes ---
@app.route('/', methods=['GET'])
def index():
    edu_log = session.pop('educational_log', [])
    error_msg = session.pop('error_message', None)
    return render_template('index.html',
                           uploaded_file_name=session.get('uploaded_file_name'),
                           final_hash=session.get('final_hash'),
                           error_message=error_msg,
                           educational_log=edu_log)

@app.route('/step_images/<filename>')
def serve_step_image(filename):
    return send_from_directory(app.config['STEP_IMAGES_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    session.pop('educational_log', None)
    session.pop('error_message', None)
    session.pop('final_hash', None)

    if 'file' not in request.files:
        flash('No file part')
        session['error_message'] = 'No file part selected.'
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        session['error_message'] = 'No file selected for upload.'
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        original_filename = file.filename
        filename_secure = secure_filename(original_filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_secure)
        _clear_temp_step_images(original_filename, "all")
        file.save(filepath)
        session['uploaded_file_path'] = filepath
        session['uploaded_file_name'] = original_filename
        session['uploaded_file_name_secure'] = filename_secure
        flash(f'Image "{original_filename}" uploaded. Ready to obtain hash.')
        return redirect(url_for('index'))
    else:
        flash('Invalid file type.')
        session['error_message'] = 'Invalid file type.'
        return redirect(url_for('index'))

@app.route('/get_hash', methods=['POST'])
def get_hash_route():
    session.pop('educational_log', None)
    session.pop('error_message', None)
    session.pop('final_hash', None)

    uploaded_file_path = session.get('uploaded_file_path')
    original_uploaded_filename = session.get('uploaded_file_name')

    if not uploaded_file_path or not os.path.exists(uploaded_file_path) or not original_uploaded_filename:
        flash('No image uploaded or file not found. Please upload an image first.')
        session['error_message'] = 'No image uploaded or file not found.'
        return redirect(url_for('index'))

    _log_educational_step(f"\n===== USER REQUESTED HASH FOR: {original_uploaded_filename} =====")
    final_hash = perceptual_hash_robust(uploaded_file_path, original_filename=original_uploaded_filename)

    if final_hash:
        session['final_hash'] = final_hash
        flash(f'Perceptual Hash for "{original_uploaded_filename}" obtained.')
    else:
        flash(f'Could not generate hash for "{original_uploaded_filename}". See process log.')
        session['error_message'] = f'Could not generate hash for "{original_uploaded_filename}".'
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)