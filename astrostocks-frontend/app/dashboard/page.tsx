'use client'

import { useState, useEffect } from 'react'
import DashboardLayout from '@/components/layout/DashboardLayout'
import SectorCard from '@/components/dashboard/SectorCard'
import { apiClient } from '@/lib/api-client'
import type { SectorPrediction } from '@/types/astro'
import toast from 'react-hot-toast'
import KPICards from '@/components/dashboard/KPICards'

export default function DashboardPage() {
  const [predictions, setPredictions] = useState<SectorPrediction[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPredictions()
  }, [])

  const loadPredictions = async () => {
    setLoading(true)
    try {
      // Call analyze endpoint without stocks - it will predict all sectors from database
      const data = await apiClient.analyze({})
      setPredictions(data.sector_predictions || [])
      toast.success('Predictions loaded successfully!')
    } catch (error: any) {
      toast.error(error.message || 'Failed to load predictions')
      console.error('Error loading predictions:', error)
    } finally {
      setLoading(false)
    }
  }


  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">Market Predictions</h1>
            <p className="mt-2 text-sm text-gray-400">
              Astrological insights powered by AI analysis
            </p>
          </div>
          <button
            onClick={loadPredictions}
            disabled={loading}
            className="px-4 py-2 rounded-lg font-medium bg-astro-gold hover:bg-astro-gold/90 text-astro-stellar transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Loading...' : 'Refresh Predictions'}
          </button>
        </div>

        {/* KPI Cards */}
        {!loading && predictions.length > 0 && (
          <KPICards predictions={predictions} />
        )}

        {/* Loading State */}
        {loading && predictions.length === 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
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

        {/* Sector Predictions Grid */}
        {!loading && predictions.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {predictions.map((prediction, index) => (
              <SectorCard
                key={`${prediction.sector_id || prediction.sector}-${index}`}
                prediction={prediction}
                index={index}
                isStreaming={false}
              />
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && predictions.length === 0 && (
          <div className="text-center py-12 glass rounded-xl border border-cosmic-700/50">
            <p className="text-gray-400">No predictions available.</p>
            <p className="text-sm text-gray-500 mt-2">Click "Refresh Predictions" to load sector analysis.</p>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}

