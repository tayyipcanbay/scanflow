import { useState, useEffect } from 'react'
import { getComparison } from '../services/api'
import type { ComparisonData } from '../services/api'

interface ComparisonViewProps {
  comparisonId: number | null
}

export default function ComparisonView({ comparisonId }: ComparisonViewProps) {
  const [data, setData] = useState<ComparisonData | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!comparisonId) {
      setData(null)
      return
    }

    setLoading(true)
    // Note: This is simplified - you'd need baseline_id and comparison_id
    // In a real app, you'd get these from the comparison list
    getComparison(1, comparisonId)
      .then(setData)
      .catch(err => console.error('Error loading comparison:', err))
      .finally(() => setLoading(false))
  }, [comparisonId])

  if (!comparisonId) {
    return (
      <div className="info-panel">
        <h3>Comparison Statistics</h3>
        <p>Select a comparison to view statistics</p>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="info-panel">
        <h3>Comparison Statistics</h3>
        <p>Loading...</p>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="info-panel">
        <h3>Comparison Statistics</h3>
        <p>No data available</p>
      </div>
    )
  }

  return (
    <div className="info-panel">
      <h3>Comparison Statistics</h3>
      
      <div className="stat-grid">
        <div className="stat-item">
          <div className="stat-label">Average Change</div>
          <div className="stat-value">{data.statistics.avg_magnitude.toFixed(4)}</div>
        </div>
        
        <div className="stat-item">
          <div className="stat-label">Max Change</div>
          <div className="stat-value">{data.statistics.max_magnitude.toFixed(4)}</div>
        </div>
        
        <div className="stat-item increase">
          <div className="stat-label">Increase</div>
          <div className="stat-value">{data.statistics.increase_percentage.toFixed(1)}%</div>
        </div>
        
        <div className="stat-item decrease">
          <div className="stat-label">Decrease</div>
          <div className="stat-value">{data.statistics.decrease_percentage.toFixed(1)}%</div>
        </div>
      </div>

      <div className="region-stats">
        <h4>Region Breakdown</h4>
        {Object.entries(data.region_statistics).map(([region, stats]) => (
          <div key={region} className="region-item">
            <div className="region-name">{region.replace('_', ' ').toUpperCase()}</div>
            <div className="region-details">
              <span>↑ {stats.increase_percentage.toFixed(1)}%</span>
              <span>↓ {stats.decrease_percentage.toFixed(1)}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

