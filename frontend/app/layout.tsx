'use client'
import './globals.css'
import { Toaster } from 'sonner'
// Toaster needs 'use client' remember
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}
      <Toaster position="top-right" richColors /> 
      </body>
    </html>
  )
}
