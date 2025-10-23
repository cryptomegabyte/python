import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/preact'
import userEvent from '@testing-library/user-event'
import { App } from './app'

// Mock fetch globally
global.fetch = vi.fn()

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the main heading', () => {
    render(<App />)
    expect(screen.getByText('Text Prediction Demo')).toBeInTheDocument()
  })

  it('renders the description', () => {
    render(<App />)
    expect(screen.getByText(/Enter text and get AI-powered continuations/)).toBeInTheDocument()
  })

  it('renders form elements', () => {
    render(<App />)
    expect(screen.getByLabelText(/Input Text/)).toBeInTheDocument()
    expect(screen.getByLabelText(/Max Length/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Predict Text/ })).toBeInTheDocument()
  })

  it('shows error for empty text submission', async () => {
    const user = userEvent.setup()
    render(<App />)

    const submitButton = screen.getByRole('button', { name: /Predict Text/ })
    await user.click(submitButton)

    // Since it's HTML5 validation, check that the textarea is invalid
    const textInput = screen.getByLabelText(/Input Text/)
    expect(textInput).toBeInvalid()
  })

  it('submits form and shows prediction', async () => {
    const mockResponse = {
      prediction: 'Hello world, this is a test prediction',
      input_length: 11,
      generated_length: 25
    }

    // Create a promise that we can resolve later
    let resolvePromise
    const promise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    global.fetch.mockReturnValueOnce(promise)

    const user = userEvent.setup()
    render(<App />)

    const textInput = screen.getByLabelText(/Input Text/)
    const submitButton = screen.getByRole('button', { name: /Predict Text/ })

    await user.type(textInput, 'Hello world')
    await user.click(submitButton)

    // Check loading state immediately after click
    expect(screen.getByRole('button', { name: /Generating\.\.\./ })).toBeInTheDocument()

    // Resolve the fetch
    resolvePromise({
      ok: true,
      json: () => Promise.resolve(mockResponse)
    })

    // Wait for result
    await waitFor(() => {
      expect(screen.getByText('Prediction:')).toBeInTheDocument()
      expect(screen.getByText(mockResponse.prediction)).toBeInTheDocument()
    })

    // Verify API call
    expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: 'Hello world', max_length: 50 }),
    })
  })

  it('shows error on API failure', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({ detail: 'Model error' })
    })

    const user = userEvent.setup()
    render(<App />)

    const textInput = screen.getByLabelText(/Input Text/)
    const submitButton = screen.getByRole('button', { name: /Predict Text/ })

    await user.type(textInput, 'Test')
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText('Model error')).toBeInTheDocument()
    })
  })

  it('updates max length slider', async () => {
    const user = userEvent.setup()
    render(<App />)

    const slider = screen.getByLabelText(/Max Length/)
    await user.click(slider)
    // Simulate changing the value
    fireEvent.change(slider, { target: { value: '100' } })

    expect(slider.value).toBe('100')
  })

  it('disables button during loading', async () => {
    global.fetch.mockImplementation(() => new Promise(() => {})) // Never resolves

    const user = userEvent.setup()
    render(<App />)

    const textInput = screen.getByLabelText(/Input Text/)
    const submitButton = screen.getByRole('button', { name: /Predict Text/ })

    await user.type(textInput, 'Test')
    await user.click(submitButton)

    expect(submitButton).toBeDisabled()
  })
})