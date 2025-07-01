// pages/image-processor.tsx or any component file
import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import Image from 'next/image';

const ImageProcessor = () => {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [processType, setProcessType] = useState('grayscale');

  // Handle file input change
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    } else {
      setFile(null);
    }
  };

  // Handle form submission
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!file) {
      alert('Please select a file before submitting.');
      return;
    }

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('image_url', file); // 👈 File is non-null now
    formData.append('process_type', processType);

    try {
      const res = await axios.post('http://localhost:8000/api/images/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      console.log('Upload successful:', res.data);
      alert('Upload successful!');
    } catch (error: unknown) {
      // Type-safe error handling for any axios version
      if (error && typeof error === 'object' && 'response' in error) {
        // This is likely an axios error
        const axiosError = error as { 
          response?: { 
            data?: { message?: string } | string 
          }; 
          message?: string 
        };
        const responseData = axiosError.response?.data;
        const errorMessage = typeof responseData === 'object' && responseData?.message 
          ? responseData.message 
          : axiosError.message || 'Request failed';
        
        console.error('Upload failed:', axiosError.response?.data || axiosError.message);
        alert(`Upload failed: ${errorMessage}`);
      } else if (error instanceof Error) {
        console.error('Upload failed:', error.message);
        alert(`Upload failed: ${error.message}`);
      } else {
        console.error('Upload failed:', 'An unknown error occurred');
        alert('Upload failed: An unknown error occurred');
      }
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      <Image
        src="/bg6.png"
        style={{ objectFit: 'cover', width: '100%', height: 'auto' }}
        width={800}
        height={600}
        alt="Background"
      />

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Title"
          required
        />
        <br />
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description"
          required
        />
        <br />
        <input
          type="file"
          onChange={handleFileChange}
          accept="image/*"
          required
        />
        <br />
        <select value={processType} onChange={(e) => setProcessType(e.target.value)}>
          <option value="grayscale">Grayscale</option>
          <option value="resolution">Resolution</option>
        </select>
        <br />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
};

export default ImageProcessor;