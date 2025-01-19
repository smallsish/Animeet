'use client'

import Image from 'next/image'
import React from 'react'
interface Props {
    link: string
}
const BackButton = ({link}: Props) => {
  return (
    <div className="flex items-center mt-8 ml-8">
      <button onClick={() => { window.location.href = link }}>
      <div className="w-[2rem] h-[2rem] relative">
          <Image 
            src="/back_arrow.png" 
            alt="Back Arrow" 
            fill 
            sizes="(max-width: 768px) 2rem, 2rem"
            className="object-contain"
          />
        </div>
      </button>
        {/* <button >
            <img src="/back_arrow.png" className="w-8 h-8" onClick={() => {window.location.href = link}}></img>
        </button> */}
        <span className="text-lg font-bold">Back to Home</span>
    </div>
  )
}

export default BackButton