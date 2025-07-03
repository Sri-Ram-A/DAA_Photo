'use client'
import React, { useState } from 'react';
import { Toaster, toast } from 'sonner'
import { useRouter } from 'next/navigation';
import { Upload as UploadIcon, Image as ImageIcon, User, FileText, X } from 'lucide-react';
import { postImage } from '@/services';

export default function Upload() {
  const [title, setTitle] = useState('');
  const [creator, setCreator] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [processingType, setProcessingType] = useState('none');

  const router = useRouter();

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {


    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const removeImage = () => {
    setImage(null);
    setPreview(null);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!image) return;

    setIsSubmitting(true);
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('image_url', image);
    formData.append('creator', creator);
    formData.append('processing_type', processingType);

    try {
      const res = await postImage(formData);

      if (res.ok) {
        const data = await res.json();
        toast.success('Image uploaded successfully!', {
          description: 'Your image has been added to the gallery'
        });
        router.push('/');
      } else {
        // Handle specific error cases
        const errorData = await res.json().catch(() => ({})); // Fallback if no JSON

        if (res.status === 403) {
          toast.error('Duplicate Image Found', {
            description: errorData.error || 'This image already exists in our system',
            action: {
              label: 'View Gallery',
              onClick: () => router.push('/view')
            }
          });
        } else {
          toast.error('Upload Failed', {
            description: errorData.error || 'An unexpected error occurred'
          });
        }
      }
    } catch (error) {
      console.error('Upload error:', error);
      toast.error('Network Error', {
        description: 'Failed to connect to the server'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="relative w-full min-h-screen overflow-hidden flex justify-center items-center p-4">
      {/* Animated Background Layers */}
      <div
        className="absolute inset-0 bg-cover bg-center opacity-0 animate-fadeImages"
        style={{
          backgroundImage: "url('/bg1.jpg')",
          animationDelay: '0s',
          animationDuration: '15s'
        }}
      />
      <div
        className="absolute inset-0 bg-cover bg-center opacity-0 animate-fadeImages"
        style={{
          backgroundImage: "url('/bg2.jpg')",
          animationDelay: '6s',
          animationDuration: '15s'
        }}
      />
      <div
        className="absolute inset-0 bg-cover bg-center opacity-0 animate-fadeImages"
        style={{
          backgroundImage: "url('/bg3.jpeg')",
          animationDelay: '9s',
          animationDuration: '15s'
        }}
      />

      {/* Glassmorphism Overlay */}
      <div className="absolute inset-0 bg-black/20 backdrop-blur-sm" />

      {/* Main Upload Card with Glassmorphism */}
      <div className="relative w-full max-w-6xl bg-white/10 backdrop-blur-lg rounded-xl shadow-2xl overflow-hidden flex flex-col md:flex-row border border-white/20 z-10">
        {/* Left Side - Image Preview/Upload */}
        <div className="md:w-1/2 p-8 flex flex-col items-center justify-center bg-white/5">
          {preview ? (
            <div className="relative w-full h-full flex items-center justify-center">
              <img
                src={preview}
                alt="Preview"
                className="max-h-[70vh] max-w-full object-contain rounded-lg border border-white/20"
              />
              <button
                onClick={removeImage}
                className="absolute top-4 right-4 bg-white/80 hover:bg-white p-2 rounded-full shadow-md transition-all"
              >
                <X className="w-5 h-5 text-gray-700" />
              </button>
            </div>
          ) : (
            <div className="w-full h-full flex flex-col items-center justify-center space-y-4 text-white">
              <div className="p-6 bg-white/20 rounded-full shadow-sm backdrop-blur-sm">
                <ImageIcon className="w-10 h-10 text-white/80" />
              </div>
              <h3 className="text-xl font-semibold">Select an image to upload</h3>
              <p className="text-white/70 text-center max-w-md">
                Drag & drop an image here, or click to browse files
              </p>
              <label className="px-6 py-3 bg-white/20 hover:bg-white/30 text-white font-medium rounded-lg cursor-pointer transition-colors border border-white/30">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="hidden"
                />
                Select Image
              </label>
              <p className="text-xs text-white/50 mt-2">PNG, JPG up to 10MB</p>
            </div>
          )}
        </div>

        {/* Right Side - Form */}
        <div className="md:w-1/2 p-8 flex flex-col bg-white/10 backdrop-blur-sm">
          <h2 className="text-2xl font-bold text-white mb-6">Upload Details</h2>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-1">
              <label className="block text-sm font-medium text-white/80">Title</label>
              <input
                type="text"
                placeholder="Give your image a title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                className="w-full px-4 py-3 bg-white/90 text-gray-800 border border-white/30 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400 outline-none transition placeholder-gray-500"
              />
            </div>

            <div className="space-y-1">
              <label className="block text-sm font-medium text-white/80">Creator</label>
              <input
                type="text"
                placeholder="Your name or username"
                value={creator}
                onChange={(e) => setCreator(e.target.value)}
                required
                className="w-full px-4 py-3 bg-white/90 text-gray-800 border border-white/30 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400 outline-none transition placeholder-gray-500"
              />
            </div>

            <div className="space-y-1">
              <label className="block text-sm font-medium text-white/80">Description</label>
              <textarea
                placeholder="Tell us about this image..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
                rows={5}
                className="w-full px-4 py-3 bg-white/90 text-gray-800 border border-white/30 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400 outline-none transition resize-none placeholder-gray-500"
              />
            </div>

            <div className="space-y-1">
              <label className="block text-sm font-medium text-white/80">Processing Type</label>
              <select
                value={processingType}
                onChange={(e) => setProcessingType(e.target.value)}
                className="w-full px-4 py-3 bg-white/90 text-gray-800 border border-white/30 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400 outline-none transition"
              >
                <option value="none">No Processing</option>
                <option value="grayscale">Convert to Grayscale</option>
                <option value="resolution">Enhance Resolution</option>
                {/* <option value="compress">Compress Image</option> */}
              </select>
            </div>

            <div className="pt-4">
              <button
                type="submit"
                disabled={isSubmitting || !image}
                className={`w-full py-3 px-6 rounded-lg font-medium flex items-center justify-center space-x-2 transition-colors ${isSubmitting || !image
                  ? 'bg-gray-400/30 text-white/50 cursor-not-allowed'
                  : 'bg-blue-500/90 hover:bg-blue-600/90 text-white shadow-md'
                  }`}
              >
                {isSubmitting ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/50 border-t-white rounded-full animate-spin"></div>
                    <span>Uploading...</span>
                  </>
                ) : (
                  <>
                    <UploadIcon className="w-5 h-5" />
                    <span>Upload Image</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Animation Keyframes */}
      <style jsx global>{`
        @keyframes fadeImages {
          0% { opacity: 0; }
          5% { opacity: 1; }
          30% { opacity: 1; }
          35% { opacity: 1; }
          100% { opacity: 0; }
        }
        .animate-fadeImages {
          animation-name: fadeImages;
          animation-iteration-count: infinite;
          animation-timing-function: ease-in-out;
        }
      `}</style>
    </div>
  );
}