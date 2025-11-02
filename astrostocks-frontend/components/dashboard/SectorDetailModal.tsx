'use client'

import { Fragment } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { XMarkIcon } from '@heroicons/react/24/outline'
import type { SectorPrediction } from '@/types/astro'
import TransitTimingTable from './TransitTimingTable'

interface SectorDetailModalProps {
  prediction: SectorPrediction | null
  isOpen: boolean
  onClose: () => void
}

export default function SectorDetailModal({ prediction, isOpen, onClose }: SectorDetailModalProps) {
  if (!prediction) return null

  const TrendIcon = {
    Bullish: '📈',
    Bearish: '📉',
    Neutral: '➖',
  }[prediction.trend] || '➖'

  const trendColors = {
    Bullish: 'text-green-400 bg-green-400/10 border-green-400/20',
    Bearish: 'text-red-400 bg-red-400/10 border-red-400/20',
    Neutral: 'text-gray-400 bg-gray-400/10 border-gray-400/20',
  }

  const trendColor = trendColors[prediction.trend as keyof typeof trendColors] || trendColors.Neutral

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/60 backdrop-blur-sm" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-4xl transform overflow-hidden rounded-2xl glass border border-cosmic-700/50 p-6 text-left align-middle shadow-xl transition-all">
                {/* Header */}
                <div className="flex items-start justify-between mb-6">
                  <div className="flex-1">
                    <Dialog.Title className="text-2xl font-bold text-white mb-2">
                      {prediction.sector_name || prediction.sector}
                    </Dialog.Title>
                    <div className="flex items-center space-x-3 flex-wrap gap-2">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${trendColor}`}>
                        {TrendIcon} {prediction.trend}
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
                    </div>
                  </div>
                  <button
                    onClick={onClose}
                    className="p-2 rounded-lg hover:bg-cosmic-700 transition-colors"
                  >
                    <XMarkIcon className="h-6 w-6 text-gray-300" />
                  </button>
                </div>

                {/* Content */}
                <div className="space-y-6 max-h-[70vh] overflow-y-auto pr-2">
                  {/* Planetary Influence */}
                  <div>
                    <h3 className="text-sm font-semibold text-gray-400 mb-2">Planetary Influence</h3>
                    <p className="text-sm text-gray-300 leading-relaxed">{prediction.planetary_influence}</p>
                  </div>

                  {/* Transit Timing Table */}
                  {prediction.planet_transits && prediction.planet_transits.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-400 mb-3">Transit Analysis</h3>
                      <TransitTimingTable planetTransits={prediction.planet_transits} />
                    </div>
                  )}

                  {/* Reasoning */}
                  <div>
                    <h3 className="text-sm font-semibold text-gray-400 mb-2">Reasoning</h3>
                    <p className="text-sm text-gray-300 leading-relaxed">{prediction.reason}</p>
                  </div>

                  {/* AI Insights */}
                  {prediction.ai_insights && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-400 mb-2">AI Insights</h3>
                      <div className="bg-cosmic-800/50 rounded-lg p-4 border border-cosmic-700">
                        {(() => {
                          // Handle case where ai_insights is already an object
                          if (typeof prediction.ai_insights === 'object' && prediction.ai_insights !== null) {
                            const parsed = prediction.ai_insights as any
                            return (
                              <div className="space-y-3">
                                {parsed.actionable_insight && (
                                  <div>
                                    <p className="text-xs text-gray-400 mb-1 font-medium">Actionable Insight:</p>
                                    <p className="text-sm text-astro-gold leading-relaxed">{parsed.actionable_insight}</p>
                                  </div>
                                )}
                                {parsed.confidence !== undefined && (
                                  <div>
                                    <p className="text-xs text-gray-400 mb-1 font-medium">Confidence Score:</p>
                                    <p className="text-lg font-semibold text-white">
                                      {(parsed.confidence * 100).toFixed(1)}%
                                    </p>
                                  </div>
                                )}
                                {parsed.reason && (
                                  <div>
                                    <p className="text-xs text-gray-400 mb-1 font-medium">Detailed Reasoning:</p>
                                    <p className="text-sm text-gray-300 leading-relaxed">{parsed.reason}</p>
                                  </div>
                                )}
                              </div>
                            )
                          }
                          
                          // Handle case where ai_insights is a string
                          if (typeof prediction.ai_insights === 'string') {
                            try {
                              const cleanedInsights = prediction.ai_insights.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim()
                              const parsed = JSON.parse(cleanedInsights)
                              return (
                                <div className="space-y-3">
                                  {parsed.actionable_insight && (
                                    <div>
                                      <p className="text-xs text-gray-400 mb-1 font-medium">Actionable Insight:</p>
                                      <p className="text-sm text-astro-gold leading-relaxed">{parsed.actionable_insight}</p>
                                    </div>
                                  )}
                                  {parsed.confidence !== undefined && (
                                    <div>
                                      <p className="text-xs text-gray-400 mb-1 font-medium">Confidence Score:</p>
                                      <p className="text-lg font-semibold text-white">
                                        {(parsed.confidence * 100).toFixed(1)}%
                                      </p>
                                    </div>
                                  )}
                                  {parsed.reason && (
                                    <div>
                                      <p className="text-xs text-gray-400 mb-1 font-medium">Detailed Reasoning:</p>
                                      <p className="text-sm text-gray-300 leading-relaxed">{parsed.reason}</p>
                                    </div>
                                  )}
                                </div>
                              )
                            } catch {
                              // If parsing fails, display as plain text
                              return (
                                <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
                                  {prediction.ai_insights.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim()}
                                </p>
                              )
                            }
                          }
                          
                          // Fallback: display as string
                          return (
                            <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
                              {String(prediction.ai_insights)}
                            </p>
                          )
                        })()}
                      </div>
                    </div>
                  )}

                  {/* Top Stocks */}
                  {prediction.top_stocks && prediction.top_stocks.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-400 mb-2">Top Stocks</h3>
                      <div className="flex flex-wrap gap-2">
                        {prediction.top_stocks.map((stock, i) => (
                          <span
                            key={i}
                            className="inline-flex items-center px-3 py-2 rounded-lg bg-cosmic-700/50 text-sm font-medium text-gray-300 hover:bg-cosmic-700 transition-colors"
                          >
                            {stock}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  )
}

