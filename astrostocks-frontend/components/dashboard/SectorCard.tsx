'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import type { SectorPrediction } from '@/types/astro'
import {
  ChevronDownIcon,
  ChevronUpIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  MinusIcon,
} from '@heroicons/react/24/outline'
import TransitTimer from './TransitTimer'
import TransitTimingTable from './TransitTimingTable'
import SectorDetailModal from './SectorDetailModal'

interface SectorCardProps {
  prediction: SectorPrediction
  isStreaming?: boolean
  index: number
}

const trendIcons = {
  Bullish: ArrowTrendingUpIcon,
  Bearish: ArrowTrendingDownIcon,
  Neutral: MinusIcon,
}

const trendColors = {
  Bullish: 'text-green-400 bg-green-400/10 border-green-400/20',
  Bearish: 'text-red-400 bg-red-400/10 border-red-400/20',
  Neutral: 'text-gray-400 bg-gray-400/10 border-gray-400/20',
}

export default function SectorCard({ prediction, isStreaming = false, index }: SectorCardProps) {
  const [expanded, setExpanded] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const TrendIcon = trendIcons[prediction.trend as keyof typeof trendIcons] || trendIcons.Neutral
  const trendColor = trendColors[prediction.trend as keyof typeof trendColors] || trendColors.Neutral

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: index * 0.1 }}
        className={`glass rounded-xl p-6 border border-cosmic-700/50 hover:border-cosmic-600 transition-all cursor-pointer ${
          isStreaming ? 'animate-pulse-glow' : ''
        }`}
        onClick={() => setIsModalOpen(true)}
      >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-white mb-1">{prediction.sector_name || prediction.sector}</h3>
          <div className="flex items-center space-x-3 flex-wrap gap-2">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${trendColor}`}>
              <TrendIcon className="h-4 w-4 mr-1" />
              {prediction.trend}
            </span>
            {prediction.confidence && (
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                prediction.confidence === 'High' 
                  ? 'text-purple-400 bg-purple-400/10 border-purple-400/20 border'
                  : prediction.confidence === 'Medium'
                  ? 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20 border'
                  : 'text-gray-400 bg-gray-400/10 border-gray-400/20 border'
              }`}>
                {prediction.confidence} Confidence
              </span>
            )}
            {!prediction.confidence && prediction.accuracy_estimate && (
              <span className="text-xs text-gray-400">
                {Math.round(prediction.accuracy_estimate * 100)}% confidence
              </span>
            )}
          </div>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation()
            setExpanded(!expanded)
          }}
          className="p-1 rounded-lg hover:bg-cosmic-700 transition-colors"
        >
          {expanded ? (
            <ChevronUpIcon className="h-5 w-5 text-gray-300" />
          ) : (
            <ChevronDownIcon className="h-5 w-5 text-gray-300" />
          )}
        </button>
      </div>

      {/* Planetary Influence */}
      <div className="mb-4">
        <p className="text-sm text-gray-300 line-clamp-2">{prediction.planetary_influence}</p>
      </div>

      {/* Top Stocks */}
      {prediction.top_stocks && prediction.top_stocks.length > 0 && (
        <div className="mb-4">
          <p className="text-xs text-gray-400 mb-2">Top Stocks:</p>
          <div className="flex flex-wrap gap-2">
            {prediction.top_stocks.slice(0, 3).map((stock, i) => (
              <span
                key={i}
                className="inline-flex items-center px-2 py-1 rounded-md bg-cosmic-700/50 text-xs font-medium text-gray-300"
              >
                {stock}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Transit Timing Summary */}
      {(prediction.transit_start || prediction.transit_end) && (
        <TransitTimer 
          startTime={prediction.transit_start}
          endTime={prediction.transit_end}
        />
      )}

      {/* Expanded Content */}
      {expanded && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="pt-4 border-t border-cosmic-700"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="space-y-4">
            <div>
              <p className="text-xs text-gray-400 mb-1 font-medium">Reasoning:</p>
              <p className="text-sm text-gray-300 leading-relaxed">{prediction.reason}</p>
            </div>
            
            {/* Transit Timing Table */}
            {prediction.planet_transits && prediction.planet_transits.length > 0 && (
              <TransitTimingTable planetTransits={prediction.planet_transits} />
            )}
            
            {prediction.ai_insights && (
              <div>
                <p className="text-xs text-gray-400 mb-2 font-medium">AI Insights:</p>
                <div className="bg-cosmic-800/50 rounded-lg p-3 border border-cosmic-700">
                  {(() => {
                    try {
                      // Try to parse and format the JSON insights
                      const cleanedInsights = prediction.ai_insights.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim()
                      const parsed = JSON.parse(cleanedInsights)
                      return (
                        <div className="space-y-2">
                          {parsed.actionable_insight && (
                            <div>
                              <p className="text-xs text-gray-400 mb-1">Actionable Insight:</p>
                              <p className="text-sm text-astro-gold leading-relaxed">{parsed.actionable_insight}</p>
                            </div>
                          )}
                          {parsed.confidence !== undefined && (
                            <div>
                              <p className="text-xs text-gray-400 mb-1">Confidence Score:</p>
                              <p className="text-sm text-white">
                                {(parsed.confidence * 100).toFixed(1)}%
                              </p>
                            </div>
                          )}
                        </div>
                      )
                    } catch {
                      // If parsing fails, show raw content
                      return (
                        <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
                          {prediction.ai_insights.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim()}
                        </p>
                      )
                    }
                  })()}
                </div>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </motion.div>
    
    {/* Detail Modal */}
    <SectorDetailModal
      prediction={prediction}
      isOpen={isModalOpen}
      onClose={() => setIsModalOpen(false)}
    />
    </>
  )
}

