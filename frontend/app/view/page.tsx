"use client"
import React, { useEffect, useState } from "react"
import { getImages } from "@/services/imageService"
import Masonry from '@mui/lab/Masonry';
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
    const [text, setText] = useState<String>("")
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
        
        <Masonry columns={3} spacing={2}>
            {images.map((image) => (
                <div key={image.id}>
                    <img
                        src={image.image_url}
                        alt={image.title}
                    />
                </div>
            ))}
        </Masonry>
    )
}
