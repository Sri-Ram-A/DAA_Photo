'use client'
import React, { useState } from 'react';
import { postImage } from '@/services/imageService';
import { useRouter } from 'next/navigation';
import './upload.css';
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function Upload() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [processType, setProcessType] = useState(''); // New state for process type
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!image) return;
    if (!processType) {
      toast.error("Please select a process type");
      return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('image_url', image);
    formData.append('creator', '1');
    formData.append('process_type', processType); // Add process type to form data

    const res = await postImage(formData);
    if (!res.ok) {
      toast.error("Error while Posting");
      return;
    }

    toast.success("Posted Successfully");
    router.push('/');
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
          <textarea
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          ></textarea>
          
          {/* New Process Type Selection */}
          <select
            value={processType}
            onChange={(e) => setProcessType(e.target.value)}
            required
          >
            <option value="">Select Process Type</option>
            <option value="grayscale">Grayscale</option>
            <option value="resolution">Resolution</option>
          </select>
          
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setImage(e.target.files?.[0] || null)}
            required
          />
          <button type="submit">
            Upload
          </button>
        </form>
      </div>
    </div>
  );
}