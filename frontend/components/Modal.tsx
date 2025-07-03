'use client'
import React from 'react'
import Image from 'next/image'
import { X, User, Calendar, Hash, Eye } from 'lucide-react'
import { ModalProps } from "@/types"

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
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString("en-US", {
            month: "short",
            day: "numeric",
            year: "numeric",
        })
    }

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm" onClick={onClose}>
            <div 
                className="relative bg-slate-900/90 border border-slate-700/50 rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto"
                onClick={(e) => e.stopPropagation()}
            >
                <button 
                    className="absolute top-4 right-4 p-2 rounded-full bg-slate-800/50 hover:bg-slate-700/50 transition-colors"
                    onClick={onClose}
                    title="Close"
                >
                    <X className="w-5 h-5 text-slate-300" />
                </button>

                <div className="grid md:grid-cols-2 gap-6 p-6">
                    {/* Image Section */}
                    <div className="relative aspect-square rounded-lg overflow-hidden border border-slate-700/50">
                        <Image
                            src={image_url}
                            alt={title}
                            fill
                            className="object-cover"
                            onError={(e) => {
                                const target = e.target as HTMLImageElement;
                                target.style.objectFit = 'cover';
                                target.style.filter = 'blur(2px)';
                            }}
                        />
                    </div>

                    {/* Details Section */}
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-2xl font-bold text-white mb-2">{title}</h2>
                            <p className="text-slate-300">{description}</p>
                        </div>

                        {/* Metadata */}
                        <div className="space-y-4">
                            <div className="flex items-center gap-3">
                                <div className="flex items-center gap-2 bg-slate-800/50 px-3 py-1.5 rounded-full border border-blue-500/30">
                                    <User className="w-4 h-4 text-blue-400" />
                                    <span className="text-blue-300 text-sm">Creator {creator}</span>
                                </div>
                                <div className="flex items-center gap-2 text-slate-400 text-sm">
                                    <Calendar className="w-4 h-4" />
                                    {formatDate(uploaded_at)}
                                </div>
                            </div>

                            {/* PHash Section */}
                            <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700/30">
                                <div className="flex items-center gap-2 mb-3">
                                    <Hash className="w-5 h-5 text-purple-400" />
                                    <h3 className="text-purple-300 font-medium">PHash Signature</h3>
                                </div>
                                <code className="text-slate-300 text-sm font-mono break-all bg-slate-900/50 p-3 rounded block">
                                    {phash}
                                </code>
                            </div>

                            <a
                                href={image_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center justify-center w-full py-2.5 px-4 rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition-colors"
                            >
                                View Original Image
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}