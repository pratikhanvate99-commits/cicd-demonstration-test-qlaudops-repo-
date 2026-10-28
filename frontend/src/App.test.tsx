import { fireEvent, render, screen, within } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import App from './App'

describe('QlaudOps command center', () => {
  it('renders dashboard and navigates to all page categories', () => {
    render(<App />)
    expect(screen.getByRole('heading', { name: 'Good afternoon, Jordan' })).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: /Kubernetes/ }))
    expect(screen.getByRole('heading', { name: 'Kubernetes' })).toBeInTheDocument()
  })

  it('opens global search with the keyboard shortcut and filters pages', () => {
    render(<App />)
    fireEvent.keyDown(window, { key: 'k', ctrlKey: true })
    const input = screen.getByPlaceholderText('Search pages, services, pipelines...')
    fireEvent.change(input, { target: { value: 'security' } })
    const searchResults = within(input.closest('.search-modal')!)
    expect(searchResults.getByRole('button', { name: /Security/ })).toBeInTheDocument()
    expect(searchResults.queryByRole('button', { name: /Kubernetes/ })).not.toBeInTheDocument()
  })

  it('requires a second explicit action to confirm demo rollback', () => {
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /Deployments/ }))
    fireEvent.click(screen.getByRole('button', { name: 'Rollback latest' }))
    expect(screen.getByText(/no live infrastructure will be changed/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Confirm rollback' })).toBeInTheDocument()
  })

  it('shows the simulated failure cause and blocked downstream stages', async () => {
    vi.stubGlobal('fetch', vi.fn().mockImplementation(async (url: string) => url === '/health'
      ? { ok: true }
      : { json: async () => ({ scenario: 'failure', status: 'failed', duration: '48s', message: 'Intentional demo assertion failure. Build and deployment were blocked.', stages: [{ name: 'validate', status: 'passed' }, { name: 'test', status: 'failed' }, { name: 'build', status: 'blocked' }, { name: 'deploy', status: 'blocked' }] }) }))
    render(<App />)
    fireEvent.click(screen.getByRole('button', { name: /Trigger failure/ }))
    expect(await screen.findByText('Root cause')).toBeInTheDocument()
    expect(screen.getByText(/test stage intentionally failed in a controlled demo fixture/i)).toBeInTheDocument()
    expect(screen.getAllByText('blocked')).toHaveLength(2)
    vi.unstubAllGlobals()
  })

  it('does not crash when health fetch rejects', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('offline')))
    render(<App />)
    expect(screen.getByText(/Demo fixtures active/)).toBeInTheDocument()
    vi.unstubAllGlobals()
  })
})
