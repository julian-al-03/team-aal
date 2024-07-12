import React from 'react'
import Image from 'next/image'

type Props = {}

export default function Navbar({}: Props) {
  return (
    <nav className="flex flex-row w-screen h-16 items-center border-b-2 border-gray-200 text-blue-500">
        <Image
            src="/wizard_2.png"
            width={32}
            height={32}
            alt="Wizzard"
            className="ml-4"
        />
        <p className="font-bold text-3xl ml-1">dataviz</p>
    </nav>
  )
}