'use client'

import { useState } from 'react'
import { format } from 'date-fns'
import { Popover, Transition } from '@headlessui/react'
import { CalendarIcon, XMarkIcon } from '@heroicons/react/24/outline'

interface DateRangeFilterProps {
  onDateChange: (date: string) => void
  selectedDate: string
}

const quickDateOptions = [
  { label: 'Today', days: 0 },
  { label: 'Tomorrow', days: 1 },
  { label: 'Next Week', days: 7 },
]

export default function DateRangeFilter({ onDateChange, selectedDate }: DateRangeFilterProps) {
  const [dateInput, setDateInput] = useState(selectedDate)

  const handleDateSelect = (date: string) => {
    setDateInput(date)
    onDateChange(date)
  }

  const handleQuickSelect = (days: number) => {
    const date = new Date()
    date.setDate(date.getDate() + days)
    const dateStr = format(date, 'yyyy-MM-dd')
    handleDateSelect(dateStr)
  }

  return (
    <div className="flex items-center space-x-4">
      {/* Quick Date Selectors */}
      <div className="flex items-center space-x-2">
        {quickDateOptions.map((option) => (
          <button
            key={option.label}
            onClick={() => handleQuickSelect(option.days)}
            className="px-3 py-1.5 rounded-lg text-sm font-medium bg-cosmic-700 hover:bg-cosmic-600 text-white transition-colors"
          >
            {option.label}
          </button>
        ))}
      </div>

      {/* Custom Date Picker */}
      <Popover className="relative">
        {({ open }) => (
          <>
            <Popover.Button className="inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium bg-cosmic-700 hover:bg-cosmic-600 text-white transition-colors">
              <CalendarIcon className="h-4 w-4 mr-2" />
              {dateInput ? format(new Date(dateInput), 'MMM dd, yyyy') : 'Select Date'}
            </Popover.Button>

            <Transition
              enter="transition ease-out duration-200"
              enterFrom="opacity-0 translate-y-1"
              enterTo="opacity-100 translate-y-0"
              leave="transition ease-in duration-150"
              leaveFrom="opacity-100 translate-y-0"
              leaveTo="opacity-0 translate-y-1"
            >
              <Popover.Panel className="absolute left-0 z-10 mt-2 w-80 glass rounded-xl p-4 border border-cosmic-700 shadow-xl">
                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-200">
                    Select Date
                  </label>
                  <input
                    type="date"
                    value={dateInput}
                    onChange={(e) => {
                      if (e.target.value) {
                        handleDateSelect(e.target.value)
                      }
                    }}
                    className="w-full px-3 py-2 rounded-lg border border-cosmic-600 bg-cosmic-800 text-white focus:outline-none focus:ring-2 focus:ring-astro-gold focus:border-astro-gold"
                  />
                  {dateInput && (
                    <button
                      onClick={() => {
                        setDateInput('')
                        onDateChange(format(new Date(), 'yyyy-MM-dd'))
                      }}
                      className="w-full inline-flex items-center justify-center px-3 py-2 rounded-lg text-sm font-medium bg-cosmic-700 hover:bg-cosmic-600 text-white transition-colors"
                    >
                      <XMarkIcon className="h-4 w-4 mr-2" />
                      Clear
                    </button>
                  )}
                </div>
              </Popover.Panel>
            </Transition>
          </>
        )}
      </Popover>
    </div>
  )
}

