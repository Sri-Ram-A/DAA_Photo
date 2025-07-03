'use client'
import React, { useState } from 'react';
import { postImage } from '@/services';
import { useRouter } from 'next/navigation';
import { Upload as UploadIcon, Image as ImageIcon, User, FileText } from 'lucide-react';

export default function Upload() {
  const [title, setTitle] = useState('');
  const [creator, setCreator] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!image) return;
    setIsSubmitting(true);
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('image_url', image);
    formData.append('creator', creator);

    const res = await postImage(formData);
    if (!res.ok) {
      setIsSubmitting(false);
      router.push('/view');
      return;
    }

    router.push('/');
  };

  return (
    <div className="relative w-full h-screen overflow-hidden flex justify-center items-center">
      {/* Background Layers with Animation */}
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

      {/* Glassmorphic Form */}
      <div className="bg-white/15 backdrop-blur-lg rounded-2xl p-10 shadow-2xl w-full max-w-md border border-white/18 text-center text-white z-10">
        <h2 className="text-2xl font-bold mb-2">Upload Image</h2>
        <p className="mb-6">Please fill out the form below to upload</p>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title Input */}
          <div className="space-y-2">
            <label className="flex items-center text-sm font-medium text-white/90 mb-2">
              <FileText className="w-4 h-4 mr-2" />
              Title
            </label>
            <input
              type="text"
              placeholder="Enter a compelling title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="w-full px-4 py-3.5 rounded-xl bg-white/95 text-gray-800 placeholder-gray-500 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all duration-200 font-medium"
            />
          </div>

          {/* Creator Input */}
          <div className="space-y-2">
            <label className="flex items-center text-sm font-medium text-white/90 mb-2">
              <User className="w-4 h-4 mr-2" />
              Creator
            </label>
            <input
              type="text"
              placeholder="Your name or handle"
              value={creator}
              onChange={(e) => setCreator(e.target.value)}
              required
              className="w-full px-4 py-3.5 rounded-xl bg-white/95 text-gray-800 placeholder-gray-500 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all duration-200 font-medium"
            />
          </div>

          {/* Description Textarea */}
          <div className="space-y-2">
            <label className="flex items-center text-sm font-medium text-white/90 mb-2">
              <FileText className="w-4 h-4 mr-2" />
              Description
            </label>
            <textarea
              placeholder="Describe your content..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              rows={4}
              className="w-full px-4 py-3.5 rounded-xl bg-white/95 text-gray-800 placeholder-gray-500 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all duration-200 font-medium resize-none"
            />
          </div>

          {/* File Upload */}
          <div className="w-full px-2 py-3 rounded-lg bg-white/95 border-2 border-dashed border-gray-300 hover:border-gray-400 transition-all duration-200 text-center cursor-pointer group">
            <div className="flex flex-col items-center space-y-1">
              <div className="text-gray-600 text-sm">
                {image ? (
                  <span className="font-medium text-gray-800">{image.name}</span>
                ) : (
                  <>
                    <p className="font-medium">Click to upload image</p>
                    <p className="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
                  </>
                )}
              </div>
            </div>
          </div>


          {/* Submit Button */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full px-6 py-4 bg-gradient-to-r from-white to-white/95 hover:from-white/95 hover:to-white text-gray-900 font-bold rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center space-x-2"
          >
            {isSubmitting ? (
              <>
                <div className="w-5 h-5 border-2 border-gray-400 border-t-gray-700 rounded-full animate-spin"></div>
                <span>Uploading...</span>
              </>
            ) : (
              <>
                <UploadIcon className="w-5 h-5" />
                <span>Upload Content</span>
              </>
            )}
          </button>
        </form>
      </div>


      {/* Animation Keyframes (in global.css or in a style tag) */}
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