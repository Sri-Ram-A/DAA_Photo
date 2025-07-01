'use client'
import React, { useState } from 'react';
import { postImage } from '@/services/imageService';
import { useRouter } from 'next/navigation';
import './upload.css';

export default function Upload() {
  const [title, setTitle] = useState('');
  const [creator, setCreator] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [processingType, setProcessingType] = useState('none'); // 🔧 NEW STATE
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
    formData.append('processing_type', processingType); // 🔧 NEW FIELD

    const res = await postImage(formData);
    if (!res.ok) {
      setIsSubmitting(false);
      router.push('/view');
      return;
    }

    router.push('/view');
  };

  return (
    <div className="upload-container">
      {/* Background Layers */}
      <div className="bg bg1"></div>
      <div className="bg bg2"></div>
      <div className="bg bg3"></div>

      {/* Glassmorphic Upload Form */}
      <div className="upload-form">
        <h2>Upload Image</h2>
        <p>Please fill out the form below to upload</p>
        <form onSubmit={handleSubmit} encType="multipart/form-data">
          <input
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Creator"
            value={creator}
            onChange={(e) => setCreator(e.target.value)}
            required
          />
          <textarea
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          ></textarea>
          <select
            value={processingType}
            onChange={(e) => setProcessingType(e.target.value)}
            required
          >
            <option value="none">No Processing</option>
            <option value="grayscale">Grayscale</option>
            <option value="resolution">High Resolution</option>
          </select>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setImage(e.target.files?.[0] || null)}
            required
          />
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Uploading..." : "Upload"}
          </button>
        </form>
      </div>
    </div>
  );
}
