# photo_daa
DAA project for 4th semester
#to run the docker image of database
docker run --name "MiniIODatabase" -p 9000:9000 -p 9001:9001 quay.io/minio/minio server /data --console-address ":9001"

if u get this error or any error similar,delete backend/migrations folder and migrate again 
django_minio_backend.utils.ConfigurationError: The configured bucket (media) must be declared either in MINIO_PRIVATE_BUCKETS or MINIO_PUBLIC_BUCKETS
field=models.ImageField(blank=True, null=True, storage=django_minio_backend.models.MinioBackend(bucket_name='media', replace_existing=True), upload_to=api.models.upload_to),

python manage.py makemigrations api

cd project_a
docker-compose up --build


so this project is about how I and my team of 4 did a Image Coud Storage Platform using docker,This s what i did
i used django rest framework to build the backend,to connect minio with django i used django-minio-backend python package,next  i made a frontend using next js
Now for huffman encoding i performed huffman encoding (in preprocessing/huffman.py)and stored the bitstring and shape as a string using json.dumps and thrn stored it as meta data in django models()
now when a user uploads image,i find the hash using perceptual Hashing in preprocessing/phash and then if a user gives any image processing request then that is sent to free docker container and also binary search tree is used to check if a image with same hash is stored previously
https://www.docker.com/blog/how-to-dockerize-django-app/
You can build the Django Docker container with the following command:

    'corsheaders',###https://pypi.org/project/django-cors-headers/
    'django_minio_backend',###https://pypi.org/project/django-minio-backend/
    # if you remove above line,inspite of running minio server,it will not work


1
docker build -t django-docker .
To see your image, you can run:

1
docker image list
The result will look something like this:

1
2
REPOSITORY      TAG       IMAGE ID       CREATED          SIZE
django-docker   latest    ace73d650ac6   20 s
https://medium.com/@michal.drozdze/how-to-reduce-the-size-of-your-docker-image-and-build-time-by-90-23a303a54c66 ->I USED 


graphviz download
Ayyy, let’s break this down **clearly and practically**, no fluff.

---

# ⚡️ **Graphviz setup explained simply**

## 💥 What is Graphviz?

Graphviz is a tool to **create diagrams and graphs** from text (DOT) descriptions.
Python libraries like `graphviz` use this **system tool** behind the scenes to render actual image or PDF files.

---

# ✅ **Step 1: Install Graphviz system binaries**

## 💻 Windows

1️⃣ Download installer:
👉 [Graphviz Windows download](https://graphviz.org/download/#windows)
(Usually a `.exe` installer, for example `graphviz-*.exe`.)

2️⃣ Install it (click Next, Next, Next).

3️⃣ Important: During install, **check the box that says "Add Graphviz to the system PATH"**.
If you forget → no worries, we can fix manually.

---

## 🍏 macOS

```bash
brew install graphviz
```

---

## 🐧 Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install graphviz
```

---

# ✅ **Step 2: Check if Graphviz is on PATH**

Open **Command Prompt** or Terminal and type:

```bash
dot -V
```

✅ If you see something like:

```
dot - graphviz version 2.50.0 (2023-01-01)
```

You're golden.

❌ If it says "command not found" or "not recognized" → fix PATH manually.

---

# ✅ **Step 3: Add Graphviz to PATH manually (if needed)**

## Windows

1️⃣ Find where Graphviz installed (usually `C:\Program Files\Graphviz\bin`).

2️⃣ Open **System Properties** → Advanced → Environment Variables.

3️⃣ Under **System variables**, find `Path` → Edit → New → paste:

```
C:\Program Files\Graphviz\bin
```

4️⃣ Click OK everywhere. Close and reopen terminal.

---

## macOS/Linux

Usually handled by brew or package manager automatically.
If needed, you can add:

```bash
export PATH="/usr/local/bin:$PATH"
```

To `~/.zshrc` or `~/.bashrc`.

---

# ✅ **Step 4: Install Python package**

```bash
pip install graphviz
```

---

# ✅ **Step 5: Test in Python**

```python
from graphviz import Digraph

dot = Digraph(comment="Test Graph")
dot.node('A', 'Start')
dot.node('B', 'End')
dot.edge('A', 'B', 'Go')

dot.render('test_graph', format='pdf', view=True)
```

✅ Should generate `test_graph.pdf` and open it.

---

# 💥 **Summary table**

| 💻 Step                 | ✅ What to do                      |
| ----------------------- | --------------------------------- |
| Install system binaries | Download or use package manager   |
| Check PATH              | Run `dot -V`                      |
| Fix PATH                | Add Graphviz `bin` folder to PATH |
| Install Python          | `pip install graphviz`            |
| Test it!                | Create & render a small diagram   |

---

⚡️ Short and solid!
If you'd like, I can also give you a **quick `.bat` file or shell snippet to set the PATH automatically**, just say "make me script"! 🚀
