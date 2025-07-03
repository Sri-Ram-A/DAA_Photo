export interface ModalProps {
    id: number
    title: string
    description: string
    image_url: string
    uploaded_at: string
    creator: number
    phash: string
    onClose: () => void
}
export interface ImageData {
    id: number
    title: string
    description: string
    image_url: string
    uploaded_at: string
    creator: number
    phash: string
    processing_type: string  // ✅ Added field
}