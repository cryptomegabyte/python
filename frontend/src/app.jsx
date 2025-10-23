import { useState } from 'preact/hooks'
import './app.css'

export function App() {
  const [text, setText] = useState('')
  const [maxLength, setMaxLength] = useState(50)
  const [prediction, setPrediction] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setLoading(true)
    setError('')
    setPrediction('')

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, max_length: maxLength }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Prediction failed')
      }

      const data = await response.json()
      setPrediction(data.prediction)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div class="container">
      <h1>Text Prediction Demo</h1>
      <p>Enter text and get AI-powered continuations using FastAPI + ML</p>

      <form onSubmit={handleSubmit} class="prediction-form">
        <div class="input-group">
          <label for="text">Input Text:</label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Start typing your text here..."
            rows="4"
            required
          />
        </div>

        <div class="input-group">
          <label for="maxLength">Max Length: {maxLength}</label>
          <input
            type="range"
            id="maxLength"
            min="10"
            max="200"
            value={maxLength}
            onChange={(e) => setMaxLength(parseInt(e.target.value))}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Predict Text'}
        </button>
      </form>

      {error && <div class="error">{error}</div>}

      {prediction && (
        <div class="result">
          <h3>Prediction:</h3>
          <p>{prediction}</p>
        </div>
      )}
    </div>
  )
}
