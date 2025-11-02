'use client'

import { useState, useEffect } from 'react'
import { ClockIcon } from '@heroicons/react/24/outline'

interface TransitTimerProps {
  startTime?: string
  endTime?: string
}

export default function TransitTimer({ startTime, endTime }: TransitTimerProps) {
  const [timeRemaining, setTimeRemaining] = useState<string>('')
  const [isActive, setIsActive] = useState(true)

  useEffect(() => {
    if (!endTime) {
      setIsActive(false)
      return
    }

    const updateTimer = () => {
      const now = new Date()
      const end = new Date(endTime)

      if (end <= now) {
        setTimeRemaining('Transit ended')
        setIsActive(false)
        return
      }

      const diff = end.getTime() - now.getTime()
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))

      if (days > 0) {
        setTimeRemaining(`${days}d ${hours}h remaining`)
      } else if (hours > 0) {
        setTimeRemaining(`${hours}h ${minutes}m remaining`)
      } else {
        setTimeRemaining(`${minutes}m remaining`)
      }

      setIsActive(true)
    }

    updateTimer()
    const interval = setInterval(updateTimer, 60000) // Update every minute

    return () => clearInterval(interval)
  }, [endTime])

  if (!startTime && !endTime) {
    return null
  }

  const formatDate = (isoString: string) => {
    const date = new Date(isoString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  return (
    <div className="mt-3 pt-3 border-t border-cosmic-700/50">
      <div className="flex items-start space-x-2">
        <ClockIcon className="h-4 w-4 text-astro-gold mt-0.5 flex-shrink-0" />
        <div className="flex-1 min-w-0">
          <p className="text-xs text-gray-400 mb-1">Transit Timing:</p>
          {startTime && (
            <p className="text-xs text-gray-300">
              Started: <span className="text-gray-400">{formatDate(startTime)}</span>
            </p>
          )}
          {endTime && (
            <div className="mt-1">
              <p className="text-xs text-gray-300">
                Ends: <span className="text-gray-400">{formatDate(endTime)}</span>
              </p>
              {timeRemaining && (
                <p className={`text-xs mt-1 font-medium ${
                  isActive ? 'text-astro-gold' : 'text-gray-400'
                }`}>
                  {timeRemaining}
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

