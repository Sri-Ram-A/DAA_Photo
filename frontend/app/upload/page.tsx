'use client';
import Form from 'next/form'
import { useState } from 'react';
import { postImage } from '@/services/imageService';
import { useFormStatus } from 'react-dom'


export default function Upload() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const status = useFormStatus()

  const handleSubmit = async (formData: FormData) => {
    if (!image) return;
    formData.append('title', title);
    formData.append('description', description);
    formData.append('image_url', image);
    formData.append('creator', "1"); //shpould replace this with pk will do later
    postImage(formData)
  };

  return (
    <Form action={handleSubmit} formEncType='multipart/form-data'>
      <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Title" required />
      <textarea value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" required />
      <input type="file" accept="image/*" onChange={(e) => setImage(e.target.files?.[0] || null)} required />
      <button type="submit" disabled={status.pending}>{status.pending ? 'Searching...' : 'Post'}</button>
    </Form>
  );
}
