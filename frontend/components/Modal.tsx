'use client'
import React from 'react'
import Image from 'next/image'
import { X } from 'lucide-react'
import './modal.css'

interface ModalProps {
    id: number
    title: string
    description: string
    image_url: string
    uploaded_at: string
    creator: number
    phash: string
    onClose: () => void
}

export default function Modal({ 
    id, 
    title, 
    description, 
    image_url, 
    uploaded_at, 
    creator,
    phash, 
    onClose 
}: ModalProps) {
    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close" onClick={onClose} title="Close">
                    <X size={20} />
                </button>
                <div className="modal-grid">
                    <div className="modal-image-container">
                        <Image
                            src={image_url}
                            alt={title}
                            fill
                            className="modal-image"
                            onError={(e) => {
                                const target = e.target as HTMLImageElement;
                                target.style.objectFit = 'cover';
                                target.style.filter = 'blur(2px)';
                            }}
                        />
                    </div>
                    <div className="modal-details">
                        <h2 className="modal-title">{title}</h2>
                        <p className="modal-description">{description}</p>
                        <div className="modal-metadata">
                            <h3>Details</h3>
                            <div className="metadata-item">
                                <span>Upload Date</span>
                                <span>{new Date(uploaded_at).toLocaleDateString('en-US', {
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                })}</span>
                            </div>
                            <div className="metadata-item">
                                <span>Creator ID</span>
                                <span>{creator}</span>
                            </div>
                            <div className="metadata-item">
                                <span>Image ID</span>
                                <span>{id}</span>
                            </div>
                            <div className="metadata-item">
                                <span>PHash</span>
                                <span className="phash">{phash}</span>
                            </div>
                        </div>
                        <a
                            href={image_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="modal-button"
                        >
                            View Original Image
                        </a>
                    </div>
                </div>
            </div>
        </div>
    )
}