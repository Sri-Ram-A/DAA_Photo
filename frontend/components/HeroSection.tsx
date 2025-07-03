import Image from "next/image"
import React from "react"
import { redirect } from "next/navigation"

export default function HeroSection() {
    return (
        <div className="flex justify-center gap-8 p-8 max-w-[1200px] mx-auto">
            {/* Left div: Hero Text, slightly wider */}
            <div className="flex-2 bg-gray-50 p-8 rounded-xl flex flex-col justify-center items-start">
                <h1 className="text-4xl font-bold mb-2">
                    Cloud Image Orchestrator
                </h1>
                <p className="text-base text-gray-600">
                    The platform for your images - hashing, huffman, housekeeping and more<br />
                </p>
            </div>

            {/* Middle div: Square with small border */}
            <div className="flex-1 aspect-square border border-gray-300 rounded-xl overflow-hidden flex items-center justify-center">
                <Image
                    src="/bg5.jpg"
                    alt="Middle image"
                    width={300}
                    height={300}
                    className="w-full h-full object-cover"
                />
            </div>

            {/* Right div: Square with image + button */}
            <div className="flex-1 aspect-square border border-gray-300 rounded-xl overflow-hidden flex flex-col items-center justify-between p-4">
                <Image
                    src="/bg4.jpg"
                    alt="Right image"
                    width={300}
                    height={200}
                    className="w-full h-auto object-cover rounded-lg"
                />
                <button
                    className="mt-auto py-2.5 px-4 rounded-lg border-none bg-black text-white cursor-pointer w-full"
                    onClick={() => { redirect("upload/") }}
                >
                    Begin The Journey
                </button>
            </div>
        </div>
    )
}