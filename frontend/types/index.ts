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
