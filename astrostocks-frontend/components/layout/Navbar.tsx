'use client'

import { Fragment } from 'react'
import { useSession, signOut } from 'next-auth/react'
import { Disclosure, Menu, Transition } from '@headlessui/react'
import { Bars3Icon, XMarkIcon, SparklesIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', current: false },
  { name: 'Predictions', href: '/predictions', current: false },
  { name: 'Sectors', href: '/sectors', current: false },
]

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ')
}

export default function Navbar() {
  const { data: session } = useSession()

  return (
    <Disclosure as="nav" className="bg-astro-stellar border-b border-cosmic-800">
      {({ open }) => (
        <>
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 items-center justify-between">
              {/* Left side - Logo and Navigation */}
              <div className="flex items-center">
                <Link href="/dashboard" className="flex items-center space-x-2">
                  <SparklesIcon className="h-8 w-8 text-astro-gold" />
                  <span className="text-xl font-bold text-white">AstroStocks</span>
                </Link>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={classNames(
                        'inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium',
                        item.current
                          ? 'border-astro-gold text-white'
                          : 'border-transparent text-gray-300 hover:border-astro-gold/50 hover:text-white'
                      )}
                    >
                      {item.name}
                    </Link>
                  ))}
                </div>
              </div>

              {/* Right side - User menu */}
              <div className="flex items-center">
                {session ? (
                  <Menu as="div" className="relative ml-3">
                    <Menu.Button className="flex items-center rounded-full bg-cosmic-700 px-4 py-2 text-sm font-medium text-white hover:bg-cosmic-600">
                      <span className="mr-2">{session.user?.name || session.user?.email}</span>
                      <span className="h-8 w-8 rounded-full bg-astro-gold flex items-center justify-center text-astro-stellar font-bold">
                        {(session.user?.name || session.user?.email)?.[0]?.toUpperCase()}
                      </span>
                    </Menu.Button>
                    <Transition
                      as={Fragment}
                      enter="transition ease-out duration-100"
                      enterFrom="transform opacity-0 scale-95"
                      enterTo="transform opacity-100 scale-100"
                      leave="transition ease-in duration-75"
                      leaveFrom="transform opacity-100 scale-100"
                      leaveTo="transform opacity-0 scale-95"
                    >
                      <Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                        <Menu.Item>
                          {({ active }) => (
                            <Link
                              href="/profile"
                              className={classNames(
                                active ? 'bg-gray-100' : '',
                                'block px-4 py-2 text-sm text-gray-700'
                              )}
                            >
                              Your Profile
                            </Link>
                          )}
                        </Menu.Item>
                        <Menu.Item>
                          {({ active }) => (
                            <button
                              onClick={() => signOut()}
                              className={classNames(
                                active ? 'bg-gray-100' : '',
                                'block w-full text-left px-4 py-2 text-sm text-gray-700'
                              )}
                            >
                              Sign out
                            </button>
                          )}
                        </Menu.Item>
                      </Menu.Items>
                    </Transition>
                  </Menu>
                ) : (
                  <Link
                    href="/login"
                    className="ml-3 inline-flex items-center rounded-md bg-astro-gold px-4 py-2 text-sm font-medium text-astro-stellar hover:bg-astro-gold/90"
                  >
                    Sign In
                  </Link>
                )}
              </div>

              {/* Mobile menu button */}
              <div className="sm:hidden">
                <Disclosure.Button className="inline-flex items-center justify-center rounded-md bg-cosmic-700 p-2 text-gray-300 hover:bg-cosmic-600 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-astro-gold">
                  <span className="sr-only">Open main menu</span>
                  {open ? (
                    <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                  ) : (
                    <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                  )}
                </Disclosure.Button>
              </div>
            </div>
          </div>

          <Disclosure.Panel className="sm:hidden">
            <div className="space-y-1 pb-3 pt-2">
              {navigation.map((item) => (
                <Disclosure.Button
                  key={item.name}
                  as={Link}
                  href={item.href}
                  className={classNames(
                    'block border-l-4 py-2 pl-3 pr-4 text-base font-medium',
                    item.current
                      ? 'border-astro-gold bg-cosmic-800 text-white'
                      : 'border-transparent text-gray-300 hover:border-astro-gold/50 hover:bg-cosmic-800 hover:text-white'
                  )}
                >
                  {item.name}
                </Disclosure.Button>
              ))}
            </div>
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  )
}

