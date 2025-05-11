"use client"
import React, { useEffect, useState } from "react"
import { getImages } from "@/services/imageService"
import Image from 'next/image'

interface ImageData {
    id: number
    title: string
    description: string
    image_url: string
    uploaded_at: string
    creator: number
}

export default function View() {
    const [text,setText]=useState<String>("")
    const [images, setImages] = useState<ImageData[]>([])

    useEffect(() => {
        const fetchImages = async () => {
            const data = await getImages()
            setImages(data)
            console.log(data)
        }
        fetchImages()
    }, [])

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
            {images.map((image) => (
                <div key={image.id} className="border rounded-lg p-4">
                    <Image 
                        src={image.image_url}
                        alt={image.title}
                        width={400}
                        height={300}
                        className="rounded-lg"
                    />
                    <h2 className="text-xl font-semibold mt-2">{image.title}</h2>
                    <p className="text-gray-600">{image.description}</p>
                    <p className="text-sm text-gray-500">Uploaded: {new Date(image.uploaded_at).toLocaleDateString()}</p>
                </div>
            ))}
        </div>
    )
}