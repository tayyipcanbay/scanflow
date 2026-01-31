import { useState, useEffect } from 'react'
import { listUserMeshes } from '../services/api'
import type { MeshUpload } from '../services/api'

interface TimelineSliderProps {
  userId: number
  onComparisonSelect: (comparisonId: number | null) => void
}

export default function TimelineSlider({ userId, onComparisonSelect }: TimelineSliderProps) {
  const [meshes, setMeshes] = useState<MeshUpload[]>([])
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listUserMeshes(userId)
      .then(data => {
        setMeshes(data)
        setLoading(false)
        // Auto-select latest if available
        if (data.length > 0) {
          const latest = data[data.length - 1]
          setSelectedIndex(data.length - 1)
          onComparisonSelect(latest.id)
        }
      })
      .catch(err => {
        console.error('Error loading meshes:', err)
        setLoading(false)
      })
  }, [userId, onComparisonSelect])

  const handleSliderChange = (index: number) => {
    setSelectedIndex(index)
    if (meshes[index]) {
      onComparisonSelect(meshes[index].id)
    }
  }

  if (loading) {
    return <div>Loading timeline...</div>
  }

  if (meshes.length === 0) {
    return (
      <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
        No mesh uploads found. Upload a mesh to get started.
      </div>
    )
  }

  return (
    <div style={{ marginTop: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
        <span style={{ fontSize: '14px', color: '#666' }}>Week 0</span>
        <span style={{ fontSize: '14px', color: '#666' }}>
          Week {meshes.length - 1}
        </span>
      </div>
      
      <input
        type="range"
        min="0"
        max={meshes.length - 1}
        value={selectedIndex ?? 0}
        onChange={(e) => handleSliderChange(parseInt(e.target.value))}
        style={{ width: '100%' }}
      />
      
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px' }}>
        {meshes.map((mesh, index) => (
          <div
            key={mesh.id}
            style={{
              textAlign: 'center',
              fontSize: '12px',
              color: selectedIndex === index ? '#667eea' : '#999',
              fontWeight: selectedIndex === index ? 'bold' : 'normal'
            }}
          >
            <div>V{mesh.version}</div>
            {mesh.is_baseline && <div style={{ fontSize: '10px' }}>Baseline</div>}
          </div>
        ))}
      </div>
    </div>
  )
}

