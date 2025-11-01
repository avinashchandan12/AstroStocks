'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    router.push('/dashboard')
  }, [router])

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-astro-stellar via-cosmic-900 to-astro-stellar">
      <div className="text-center">
        <div className="inline-block animate-pulse">
          <div className="h-16 w-16 border-4 border-astro-gold border-t-transparent rounded-full"></div>
        </div>
        <p className="mt-4 text-gray-300">Redirecting to dashboard...</p>
      </div>
    </div>
  )
}
