import Image from "next/image"
import React from "react"
import { redirect } from "next/navigation"

export default function HeroSection() {
    return (
        <div
            style={{
                display: "flex",
                justifyContent: "center",
                gap: "2rem",
                padding: "2rem",
                maxWidth: "1200px",
                margin: "0 auto",
               
            }}
        >
            {/* Left div: Hero Text, slightly wider */}
            <div
                style={{
                    flex: 2,
                    background: "#f5f5f5",
                    padding: "2rem",
                    borderRadius: "12px",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "flex-start",
                }}
            >
                <h1 style={{ fontSize: "2.5rem", fontWeight: "bold", marginBottom: "0.5rem" }}>
                    Roja Vai Thaalatum
                </h1>
                <p style={{ fontSize: "1rem", color: "#555" }}>
                    Ennakendru etravale ponnagai evalo,idhayathil kair katti<br />Salaam Rocky bhai.
                </p>
            </div>

            {/* Middle div: Square with small border */}
            <div
                style={{
                    flex: 1,
                    aspectRatio: "1 / 1",
                    border: "1px solid #ddd",
                    borderRadius: "12px",
                    overflow: "hidden",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                }}
            >
                <Image
                    src="/bg5.jpg"
                    alt="Middle image"
                    width={300}
                    height={300}
                    style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                    }}
                />
            </div>

            {/* Right div: Square with image + button */}
            <div
                style={{
                    flex: 1,
                    aspectRatio: "1 / 1",
                    border: "1px solid #ddd",
                    borderRadius: "12px",
                    overflow: "hidden",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "space-between",
                    padding: "1rem",
                }}
            >
                <Image
                    src="/bg4.jpg"
                    alt="Right image"
                    width={300}
                    height={200}
                    style={{
                        width: "100%",
                        height: "auto",
                        objectFit: "cover",
                        borderRadius: "8px",
                    }}
                />
                <button
                    style={{
                        marginTop: "auto",
                        padding: "10px 16px",
                        borderRadius: "8px",
                        border: "none",
                        background: "#111",
                        color: "#fff",
                        cursor: "pointer",
                        width: "100%",
                    }}
                    onClick={() => { redirect("upload/") }}
                >Begin The Journey
                </button>
            </div>
        </div>
    )
}
