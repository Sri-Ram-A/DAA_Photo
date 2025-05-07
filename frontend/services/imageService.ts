import { BASE_API_URL } from '@/api';
// You can do same functionality without async function also
export const postImage = async (formData: FormData) => {
  try {
    const res = await fetch(BASE_API_URL, {
      method: 'POST',
      body: formData,
    });
    
    if (!res.ok) {
      const errorData = await res.json();
      console.error('Upload failed:', errorData);
      throw new Error(`Upload failed: ${JSON.stringify(errorData)}`);
    }
    
    const data = await res.json();
    console.log('Uploaded:', data);
    return data;
  } catch (err) {
    console.error('Upload failed due to:', err);
    throw err;
  }
};

export const getImages = async () => {
  try {
    const res = await fetch(BASE_API_URL);
    return await res.json();
  } catch (err) {
    console.error('Fetching images failed due to:', err);
    throw err;
  }
};
