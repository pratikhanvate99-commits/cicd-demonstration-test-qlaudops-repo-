import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

globalThis.fetch = vi.fn().mockRejectedValue(new Error('API unavailable'))
afterEach(() => cleanup())

class ResizeObserverMock implements ResizeObserver {
  constructor(private callback: ResizeObserverCallback) {}
  observe(target: Element) {
    this.callback([{ target, contentRect: { width: 800, height: 240 } } as ResizeObserverEntry], this)
  }
  unobserve() {}
  disconnect() {}
}

globalThis.ResizeObserver = ResizeObserverMock
