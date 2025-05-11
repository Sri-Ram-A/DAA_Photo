'use client'
import React from 'react'
import Image from 'next/image'
import './modal.css'

interface ModalProps {
    id: number
    title: string
    description: string
    image_url: string
    uploaded_at: string
    creator: number
    onClose: () => void
}

export default function Modal({ id, title, description, image_url, uploaded_at, creator, onClose }: ModalProps) {
    return (
        <div className="modal-overlay">
            <div className="modal-container">
                <button 
                    onClick={onClose}
                    className="modal-close-button"
                    title="Close"
                >
                    ✕
                </button>
                
                <div className="modal-image-container">
                    <Image
                        src={image_url}
                        alt={title}
                        fill
                        className="object-cover"
                    />
                </div>

                <div className="modal-text">
                    <h2 className="modal-title">📌 {title}</h2>
                    <p className="modal-description">📝 {description}</p>

                    <div className="modal-meta">
                        <p>📅 Uploaded on: <strong>{new Date(uploaded_at).toLocaleDateString()}</strong></p>
                        <p>🧑‍💻 Creator ID: <strong>{creator}</strong></p>
                        <p>🔗 Image URL: <a href={image_url} target="_blank" rel="noopener noreferrer">{image_url}</a></p>
                        <p>🆔 Internal Image ID: <strong>{id}</strong></p>
                    </div>
                </div>
            </div>
        </div>
    )
}
