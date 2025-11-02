'use client'

import { useState, useEffect } from 'react'
import type { PlanetTransit } from '@/types/astro'
import { ClockIcon } from '@heroicons/react/24/outline'

interface TransitTimingTableProps {
  planetTransits: PlanetTransit[]
}

export default function TransitTimingTable({ planetTransits }: TransitTimingTableProps) {
  const [timeRemaining, setTimeRemaining] = useState<Record<string, string>>({})

  useEffect(() => {
    if (!planetTransits || planetTransits.length === 0) return

    const updateTimers = () => {
      const timers: Record<string, string> = {}
      
      planetTransits.forEach((transit) => {
        if (!transit.transit_end) {
          timers[transit.planet] = 'N/A'
          return
        }

        const now = new Date()
        const end = new Date(transit.transit_end)

        if (end <= now) {
          timers[transit.planet] = 'Transit ended'
          return
        }

        const diff = end.getTime() - now.getTime()
        const days = Math.floor(diff / (1000 * 60 * 60 * 24))
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))

        if (days > 0) {
          timers[transit.planet] = `${days}d ${hours}h`
        } else if (hours > 0) {
          timers[transit.planet] = `${hours}h ${minutes}m`
        } else {
          timers[transit.planet] = `${minutes}m`
        }
      })

      setTimeRemaining(timers)
    }

    updateTimers()
    const interval = setInterval(updateTimers, 60000) // Update every minute

    return () => clearInterval(interval)
  }, [planetTransits])

  if (!planetTransits || planetTransits.length === 0) {
    return null
  }

  const formatDate = (isoString?: string) => {
    if (!isoString) return 'N/A'
    const date = new Date(isoString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  const getStatusColor = (status?: string) => {
    if (!status) return 'text-gray-400 bg-gray-400/10'
    const statusLower = status.toLowerCase()
    if (statusLower.includes('exalted')) return 'text-purple-400 bg-purple-400/10'
    if (statusLower.includes('debilitated') || statusLower.includes('weak')) return 'text-red-400 bg-red-400/10'
    return 'text-yellow-400 bg-yellow-400/10'
  }

  return (
    <div>
      <div className="flex items-center space-x-2 mb-4">
        <ClockIcon className="h-5 w-5 text-astro-gold" />
        <h4 className="text-sm font-semibold text-white">Planetary Transit Timing</h4>
      </div>
      <div className="overflow-x-auto rounded-lg border border-cosmic-700/50 bg-cosmic-800/20">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-cosmic-700/50 bg-cosmic-800/40">
              <th className="text-left py-3 px-4 text-gray-300 font-semibold text-xs uppercase tracking-wider">Planet</th>
              <th className="text-left py-3 px-4 text-gray-300 font-semibold text-xs uppercase tracking-wider">Sign</th>
              <th className="text-left py-3 px-4 text-gray-300 font-semibold text-xs uppercase tracking-wider">Status</th>
              <th className="text-left py-3 px-4 text-gray-300 font-semibold text-xs uppercase tracking-wider">Started</th>
              <th className="text-left py-3 px-4 text-gray-300 font-semibold text-xs uppercase tracking-wider">Ends</th>
              <th className="text-left py-3 px-4 text-gray-300 font-semibold text-xs uppercase tracking-wider">Time Remaining</th>
            </tr>
          </thead>
          <tbody>
            {planetTransits.map((transit, index) => (
              <tr
                key={`${transit.planet}-${index}`}
                className="border-b border-cosmic-700/30 hover:bg-cosmic-700/30 transition-colors"
              >
                <td className="py-3 px-4">
                  <span className="font-semibold text-white text-base">{transit.planet}</span>
                </td>
                <td className="py-3 px-4">
                  <span className="text-gray-300 font-medium">{transit.sign}</span>
                </td>
                <td className="py-3 px-4">
                  <span className={`inline-flex items-center px-2 py-1 rounded-md text-xs font-medium ${getStatusColor(transit.status)}`}>
                    {transit.status || 'Normal'}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <span className="text-gray-400 text-xs">{formatDate(transit.transit_start)}</span>
                </td>
                <td className="py-3 px-4">
                  <span className="text-gray-400 text-xs">{formatDate(transit.transit_end)}</span>
                </td>
                <td className="py-3 px-4">
                  <span className="text-astro-gold font-semibold">
                    {timeRemaining[transit.planet] || 'Calculating...'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

