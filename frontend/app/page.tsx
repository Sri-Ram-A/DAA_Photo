import Link from "next/link"
 
export default function Home(){
  return(
    <>
    <Link href="/upload">Upload Image?</Link>
    <Link href="/view">View Images?</Link>
    </>
  )
}