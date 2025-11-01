'use client'

import { useState } from 'react'
import { signIn } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { SparklesIcon } from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const result = await signIn('credentials', {
        redirect: false,
        email,
        password,
      })

      if (result?.error) {
        toast.error(result.error)
      } else {
        toast.success('Logged in successfully!')
        router.push('/dashboard')
      }
    } catch (error) {
      toast.error('An error occurred during login')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-astro-stellar via-cosmic-900 to-astro-stellar py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="flex justify-center">
            <div className="rounded-full bg-cosmic-700 p-3">
              <SparklesIcon className="h-12 w-12 text-astro-gold" />
            </div>
          </div>
          <h2 className="mt-6 text-center text-4xl font-extrabold text-white">
            Sign in to AstroStocks
          </h2>
          <p className="mt-2 text-center text-sm text-gray-300">
            Predict stock movements using celestial wisdom
          </p>
        </div>
        <form className="mt-8 space-y-6 glass rounded-xl p-8" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-200">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-cosmic-600 bg-cosmic-800 placeholder-gray-400 text-white rounded-lg focus:outline-none focus:ring-astro-gold focus:border-astro-gold focus:z-10 sm:text-sm"
                placeholder="Enter your email"
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-200">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 appearance-none relative block w-full px-3 py-2 border border-cosmic-600 bg-cosmic-800 placeholder-gray-400 text-white rounded-lg focus:outline-none focus:ring-astro-gold focus:border-astro-gold focus:z-10 sm:text-sm"
                placeholder="Enter your password"
              />
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                className="h-4 w-4 text-astro-gold focus:ring-astro-gold border-cosmic-600 rounded bg-cosmic-800"
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-300">
                Remember me
              </label>
            </div>

            <div className="text-sm">
              <a href="#" className="font-medium text-astro-gold hover:text-astro-gold/80">
                Forgot your password?
              </a>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-astro-stellar bg-astro-gold hover:bg-astro-gold/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-astro-gold disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>

          <div className="text-center">
            <span className="text-gray-300">Don't have an account? </span>
            <Link href="/signup" className="font-medium text-astro-gold hover:text-astro-gold/80">
              Sign up
            </Link>
          </div>
        </form>
      </div>
    </div>
  )
}

