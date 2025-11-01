'use client'

import { useMemo } from 'react'
import {
  ChartBarIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  MinusIcon,
} from '@heroicons/react/24/outline'
import type { SectorPrediction } from '@/types/astro'

interface KPICardsProps {
  predictions: SectorPrediction[]
}

export default function KPICards({ predictions }: KPICardsProps) {
  const stats = useMemo(() => {
    const total = predictions.length
    const bullish = predictions.filter((p) => p.trend === 'Bullish').length
    const bearish = predictions.filter((p) => p.trend === 'Bearish').length
    const neutral = predictions.filter((p) => p.trend === 'Neutral').length

    // Confidence breakdown
    const highConfidence = predictions.filter((p) => p.confidence === 'High').length
    const mediumConfidence = predictions.filter((p) => p.confidence === 'Medium').length
    const lowConfidence = predictions.filter((p) => p.confidence === 'Low').length

    // Calculate percentages
    const bullishPercent = total > 0 ? ((bullish / total) * 100).toFixed(1) : '0'
    const bearishPercent = total > 0 ? ((bearish / total) * 100).toFixed(1) : '0'
    const neutralPercent = total > 0 ? ((neutral / total) * 100).toFixed(1) : '0'

    return {
      total,
      bullish,
      bearish,
      neutral,
      bullishPercent,
      bearishPercent,
      neutralPercent,
      highConfidence,
      mediumConfidence,
      lowConfidence,
    }
  }, [predictions])

  const kpiCards = [
    {
      title: 'Total Sectors',
      value: stats.total,
      icon: ChartBarIcon,
      color: 'text-blue-400 bg-blue-400/10 border-blue-400/20',
      change: null,
    },
    {
      title: 'Bullish Sectors',
      value: stats.bullish,
      subtitle: `${stats.bullishPercent}%`,
      icon: ArrowTrendingUpIcon,
      color: 'text-green-400 bg-green-400/10 border-green-400/20',
      change: null,
    },
    {
      title: 'Bearish Sectors',
      value: stats.bearish,
      subtitle: `${stats.bearishPercent}%`,
      icon: ArrowTrendingDownIcon,
      color: 'text-red-400 bg-red-400/10 border-red-400/20',
      change: null,
    },
    {
      title: 'Neutral Sectors',
      value: stats.neutral,
      subtitle: `${stats.neutralPercent}%`,
      icon: MinusIcon,
      color: 'text-gray-400 bg-gray-400/10 border-gray-400/20',
      change: null,
    },
    {
      title: 'High Confidence',
      value: stats.highConfidence,
      icon: ChartBarIcon,
      color: 'text-purple-400 bg-purple-400/10 border-purple-400/20',
      change: null,
    },
    {
      title: 'Medium Confidence',
      value: stats.mediumConfidence,
      icon: ChartBarIcon,
      color: 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20',
      change: null,
    },
  ]

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {kpiCards.map((kpi, index) => {
        const Icon = kpi.icon
        return (
          <div
            key={index}
            className="glass rounded-xl p-6 border border-cosmic-700/50 hover:border-cosmic-600 transition-all"
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <p className="text-sm text-gray-400 mb-1">{kpi.title}</p>
                <div className="flex items-baseline space-x-2">
                  <p className="text-3xl font-bold text-white">{kpi.value}</p>
                  {kpi.subtitle && (
                    <p className="text-sm text-gray-400">({kpi.subtitle})</p>
                  )}
                </div>
              </div>
              <div className={`p-3 rounded-lg border ${kpi.color}`}>
                <Icon className="h-6 w-6" />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

