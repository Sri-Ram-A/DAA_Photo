'use client'
import Image from 'next/image'
import { redirect } from 'next/navigation'
import { useEffect } from 'react';
export default function Home() {
  useEffect(() => {
    // Hide scrollbar
    document.body.style.overflow = 'hidden';
    // Cleanup function to reset the overflow when the component unmounts
    return () => {
      document.body.style.overflow = 'auto';
    };
  }, []);
  return (
    <section style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      height: '100vh',
      padding: '0 5%',
      color: 'white',
      overflow: 'hidden', // Prevent scrolling
      position: 'relative', // Positioning for the background image
    }}>
      {/* Background Image */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: -1, // Send the background image behind the content
      }}>
        <Image
          src="/bg6.png" // Replace with your PNG image path
          alt="Background Image"
          layout="fill" // Use fill to cover the entire section
          objectFit="cover" // Cover the section without distortion
        />
      </div>

      {/* Left side (Text Section) */}
      <div style={{ maxWidth: '50%' }}>
        <h1 style={{ fontSize: '5rem', fontWeight: 'bold', color: '#ff6200' }}>Star Magics</h1>
        <p style={{ fontSize: '1.5rem', margin: '20px 0', color: '#ff6200' }}>
          Unlock the magic of creativity and innovation.
        </p>

        {/* Buttons */}
        <div>
          <button onClick={()=>{redirect("/upload")}} style={{
            backgroundColor: '#ff6200',
            color: 'white',
            fontSize: '1.2rem',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '5px',
            marginRight: '10px',
            cursor: 'pointer',
            transition: '0.3s'
          }}>
            Create
          </button>
          <button  onClick={()=>{redirect("/view")}} style={{
            backgroundColor: '#ff6200',
            color: 'white',
            fontSize: '1.2rem',
            padding: '10px 20px',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            transition: '0.3s'
          }}>
            Inspire
          </button>
        </div>
      </div>

      {/* Right side (Image Section) - Removed as background is now set */}
    </section>
  )
}
