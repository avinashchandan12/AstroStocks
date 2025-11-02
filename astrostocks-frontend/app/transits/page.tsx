'use client'

import { useState, useEffect } from 'react'
import DashboardLayout from '@/components/layout/DashboardLayout'
import { apiClient } from '@/lib/api-client'
import type { TransitResponse, PlanetaryTransit } from '@/types/astro'
import toast from 'react-hot-toast'
import { CalendarIcon, SparklesIcon, ArrowPathIcon } from '@heroicons/react/24/outline'

export default function TransitsPage() {
  const [transitsData, setTransitsData] = useState<TransitResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedDate, setSelectedDate] = useState<string>('')
  
  useEffect(() => {
    // Set default date to today
    const today = new Date().toISOString().split('T')[0]
    setSelectedDate(today)
    loadTransits(today)
  }, [])

  const loadTransits = async (date: string, hardRefresh: boolean = false) => {
    setLoading(true)
    try {
      const data = await apiClient.getTransits(date, hardRefresh)
      setTransitsData(data)
      if (hardRefresh) {
        toast.success('Transit data refreshed and recalculated', { duration: 2000 })
      } else if (data.cached) {
        toast.success('Loaded from cache', { duration: 2000 })
      } else {
        toast.success('Transit data calculated and cached', { duration: 2000 })
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || error.message || 'Failed to load transits')
      console.error('Error loading transits:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = () => {
    if (selectedDate) {
      loadTransits(selectedDate, true)
    }
  }

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newDate = e.target.value
    setSelectedDate(newDate)
    if (newDate) {
      loadTransits(newDate)
    }
  }

  const formatDate = (isoString?: string) => {
    if (!isoString) return 'N/A'
    const date = new Date(isoString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const getStatusColor = (status?: string) => {
    if (!status) return 'text-gray-400 bg-gray-400/10'
    const statusLower = status.toLowerCase()
    if (statusLower.includes('exalted')) return 'text-purple-400 bg-purple-400/10'
    if (statusLower.includes('debilitated') || statusLower.includes('weak')) return 'text-red-400 bg-red-400/10'
    return 'text-yellow-400 bg-yellow-400/10'
  }

  const getMotionColor = (motion?: string) => {
    if (!motion) return 'text-gray-400'
    if (motion.toLowerCase() === 'retrograde') return 'text-orange-400'
    return 'text-green-400'
  }

  const getPlanetIcon = (planet: string) => {
    // You can add emoji icons for planets here
    const planetEmojis: Record<string, string> = {
      'Sun': '☉',
      'Moon': '☽',
      'Mars': '♂',
      'Mercury': '☿',
      'Jupiter': '♃',
      'Venus': '♀',
      'Saturn': '♄',
      'Rahu': '☊',
      'Ketu': '☋',
    }
    return planetEmojis[planet] || '○'
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white flex items-center space-x-2">
              <SparklesIcon className="h-8 w-8 text-astro-gold" />
              <span>Planetary Transits</span>
            </h1>
            <p className="mt-2 text-sm text-gray-400">
              View planetary positions and transits for any date
            </p>
          </div>
          
          {/* Date Picker and Refresh Button */}
          <div className="mt-4 sm:mt-0">
            <label htmlFor="transit-date" className="block text-sm font-medium text-gray-300 mb-2">
              Select Date
            </label>
            <div className="flex space-x-2">
              <div className="relative flex-1">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <CalendarIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="date"
                  id="transit-date"
                  value={selectedDate}
                  onChange={handleDateChange}
                  className="block w-full pl-10 pr-3 py-2 border border-cosmic-700 rounded-lg bg-cosmic-800/50 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-astro-gold focus:border-transparent"
                />
              </div>
              <button
                onClick={handleRefresh}
                disabled={loading || !selectedDate}
                className="px-4 py-2 rounded-lg font-medium bg-astro-gold hover:bg-astro-gold/90 text-astro-stellar transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                title="Refresh transit data (bypass cache)"
              >
                <ArrowPathIcon className={`h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
                <span className="hidden sm:inline">Refresh</span>
              </button>
            </div>
          </div>
        </div>

        {/* Cache Status */}
        {transitsData && (
          <div className={`px-4 py-2 rounded-lg border ${
            transitsData.cached 
              ? 'bg-green-500/10 border-green-500/30 text-green-400' 
              : 'bg-blue-500/10 border-blue-500/30 text-blue-400'
          }`}>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">
                {transitsData.cached ? '✓ Loaded from cache' : '✓ Calculated and cached'}
              </span>
              <span className="text-xs text-gray-400">
                {formatDate(transitsData.timestamp)}
              </span>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && !transitsData && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(9)].map((_, i) => (
              <div
                key={i}
                className="glass rounded-xl p-6 border border-cosmic-700/50 animate-pulse"
              >
                <div className="h-6 bg-cosmic-700 rounded w-3/4 mb-4"></div>
                <div className="h-4 bg-cosmic-700 rounded w-1/2 mb-2"></div>
                <div className="h-4 bg-cosmic-700 rounded w-full"></div>
              </div>
            ))}
          </div>
        )}

        {/* Transits Grid */}
        {!loading && transitsData && transitsData.transits.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {transitsData.transits.map((transit, index) => (
              <div
                key={`${transit.planet}-${index}`}
                className="glass rounded-xl p-6 border border-cosmic-700/50 hover:border-astro-gold/50 transition-all hover:shadow-lg hover:shadow-astro-gold/10"
              >
                {/* Planet Header */}
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="text-3xl">{getPlanetIcon(transit.planet)}</div>
                    <div>
                      <h3 className="text-xl font-bold text-white">{transit.planet}</h3>
                      <p className="text-sm text-gray-400">Planet</p>
                    </div>
                  </div>
                  <span className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium ${getStatusColor(transit.status || transit.dignity)}`}>
                    {transit.status || transit.dignity || 'Normal'}
                  </span>
                </div>

                {/* Sign */}
                <div className="mb-4">
                  <p className="text-xs text-gray-400 mb-1">Current Sign (Rashi)</p>
                  <p className="text-lg font-semibold text-astro-gold">{transit.sign}</p>
                </div>

                {/* Nakshatra */}
                {transit.nakshatra && (
                  <div className="mb-4">
                    <p className="text-xs text-gray-400 mb-1">Nakshatra</p>
                    <p className="text-base font-semibold text-purple-300">{transit.nakshatra}</p>
                  </div>
                )}

                {/* Motion */}
                <div className="mb-4">
                  <p className="text-xs text-gray-400 mb-1">Motion</p>
                  <p className={`text-sm font-medium ${getMotionColor(transit.motion)}`}>
                    {transit.motion || 'Direct'}
                  </p>
                </div>

                {/* Transit Timing */}
                {(transit.transit_start || transit.transit_end) && (
                  <div className="mt-4 pt-4 border-t border-cosmic-700/50 space-y-2">
                    {transit.transit_start && (
                      <div>
                        <p className="text-xs text-gray-400 mb-1">Entered Sign</p>
                        <p className="text-xs text-gray-300">{formatDate(transit.transit_start)}</p>
                      </div>
                    )}
                    {transit.transit_end && (
                      <div>
                        <p className="text-xs text-gray-400 mb-1">Leaves Sign</p>
                        <p className="text-xs text-gray-300">{formatDate(transit.transit_end)}</p>
                      </div>
                    )}
                  </div>
                )}

                {/* Additional Details */}
                <div className="mt-4 pt-4 border-t border-cosmic-700/50 grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <p className="text-gray-400">Longitude</p>
                    <p className="text-gray-300">{transit.longitude.toFixed(2)}°</p>
                  </div>
                  <div>
                    <p className="text-gray-400">Degree in Sign</p>
                    <p className="text-gray-300">{transit.degree_in_sign.toFixed(2)}°</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && (!transitsData || transitsData.transits.length === 0) && (
          <div className="text-center py-12 glass rounded-xl border border-cosmic-700/50">
            <p className="text-gray-400">No transit data available.</p>
            <p className="text-sm text-gray-500 mt-2">Please select a date to view transits.</p>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}

