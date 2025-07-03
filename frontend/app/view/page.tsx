"use client"
import React, { useEffect, useState } from "react"
import Image from "next/image"
import { getImages } from "@/services/imageService"
import HeroSection from "../../components/HeroSection"
import Modal from "../../components/Modal";

interface ImageData {
    id: number
    title: string
    description: string
    image_url: string
    uploaded_at: string
    creator: number
    phash:string
}

export default function View() {
    const [images, setImages] = useState<ImageData[]>([])
    const [selectedImage, setSelectedImage] = useState<ImageData | null>(null);

    useEffect(() => {
        const fetchImages = async () => {
            const data = await getImages()
            setImages(data)
        }
        fetchImages()
    }, [])

    return (
        <>
            {selectedImage && (
                <Modal
                    id={selectedImage.id}
                    title={selectedImage.title}
                    description={selectedImage.description}
                    image_url={selectedImage.image_url}
                    uploaded_at={selectedImage.uploaded_at}
                    creator={selectedImage.creator}
                    phash={selectedImage.phash}
                    onClose={() => setSelectedImage(null)}
                />
            )}
            <hr />
            <HeroSection />
            <hr />

            <div
                style={{
                    columnCount: 3,
                    columnGap: "1rem",
                    width: "100%",
                    maxWidth: "1200px",
                    margin: "2rem auto",
                    overflowY: "auto",
                    
                }}
            >
                {images.map((image) => (
                    <div
                        key={image.id}
                        style={{
                            position: "relative",
                            breakInside: "avoid",
                            marginBottom: "1rem",
                            borderRadius: "12px",
                            overflow: "hidden",
                            boxShadow: "0 4px 12px rgba(0, 0, 0, 0.2)",
                        }}
                    >
                        <Image
                            src={image.image_url}
                            alt={image.title}
                            width={0}
                            height={0}
                            sizes="100vw"
                            style={{
                                width: "100%",
                                height: "auto",
                                display: "block",
                                borderRadius: "12px",
                                cursor: "pointer"
                            }}
                            loading="lazy"
                            blurDataURL="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
                            placeholder="blur"
                            onClick={() => setSelectedImage(image)}
                        />

                        {/* Top overlay */}
                        <div
                            style={{
                                position: "absolute",
                                top: "12px",
                                left: "12px",
                                display: "flex",
                                alignItems: "center",
                                gap: "10px",
                                background: "rgba(255, 255, 255, 0.1)",
                                backdropFilter: "blur(6px)",
                                padding: "8px 12px",
                                borderRadius: "8px",
                                zIndex: 10,
                            }}
                        >
                            <div style={{ color: "white" }}>
                                <p style={{ margin: 0, fontSize: "14px", fontWeight: 500 }}>
                                    {image.creator}
                                </p>
                            </div>
                        </div>

                        {/* Bottom overlay */}
                        <div
                            style={{
                                position: "absolute",
                                bottom: 0,
                                left: 0,
                                width: "100%",
                                padding: "16px",
                                background:
                                    "linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent)",
                                color: "white",
                                zIndex: 10,
                            }}
                        >
                            <h2 style={{ margin: 0, fontWeight: 700, fontSize: "18px" }}>
                                {image.title}
                            </h2>
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}
