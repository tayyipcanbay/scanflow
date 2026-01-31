import { useState, useEffect } from 'react'
import { getInsights } from '../services/api'
import type { Insight } from '../services/api'

interface InsightsPanelProps {
  comparisonId: number | null
}

export default function InsightsPanel({ comparisonId }: InsightsPanelProps) {
  const [insight, setInsight] = useState<Insight | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!comparisonId) {
      setInsight(null)
      return
    }

    setLoading(true)
    getInsights(comparisonId)
      .then(setInsight)
      .catch(err => console.error('Error loading insights:', err))
      .finally(() => setLoading(false))
  }, [comparisonId])

  if (!comparisonId) {
    return (
      <div className="info-panel">
        <h3>AI Insights</h3>
        <p>Select a comparison to view insights</p>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="info-panel">
        <h3>AI Insights</h3>
        <p>Generating insights...</p>
      </div>
    )
  }

  if (!insight) {
    return (
      <div className="info-panel">
        <h3>AI Insights</h3>
        <p>No insights available</p>
      </div>
    )
  }

  return (
    <div className="info-panel">
      <h3>AI Insights</h3>
      <div className="insight-content">
        <p>{insight.text}</p>
        <div className="insight-confidence">
          Confidence: {(insight.confidence * 100).toFixed(0)}%
        </div>
      </div>
    </div>
  )
}

