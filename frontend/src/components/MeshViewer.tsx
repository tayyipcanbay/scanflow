import { useRef, useEffect, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import * as THREE from 'three'
import { getComparison } from '../services/api'
import type { ComparisonData } from '../services/api'

interface MeshViewerProps {
  comparisonId: number | null
  userId: number
}

function MeshModel({ comparisonData }: { comparisonData: ComparisonData | null }) {
  const meshRef = useRef<THREE.Mesh>(null)
  const [geometry, setGeometry] = useState<THREE.BufferGeometry | null>(null)

  useEffect(() => {
    if (!comparisonData?.color_data) return

    const { vertices, colors } = comparisonData.color_data

    // Create geometry
    const geom = new THREE.BufferGeometry()
    geom.setAttribute('position', new THREE.Float32BufferAttribute(vertices.flat(), 3))
    
    // Normalize colors from 0-255 to 0-1
    const normalizedColors = colors.map(c => [c[0] / 255, c[1] / 255, c[2] / 255]).flat()
    geom.setAttribute('color', new THREE.Float32BufferAttribute(normalizedColors, 3))

    setGeometry(geom)
  }, [comparisonData])

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.005
    }
  })

  if (!geometry) {
    return null
  }

  return (
    <mesh ref={meshRef} geometry={geometry}>
      <meshStandardMaterial vertexColors />
    </mesh>
  )
}

export default function MeshViewer({ comparisonId, userId }: MeshViewerProps) {
  const [comparisonData, setComparisonData] = useState<ComparisonData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!comparisonId) {
      setComparisonData(null)
      return
    }

    setLoading(true)
    setError(null)

    // For now, we'll need to get baseline and comparison IDs
    // This is a simplified version - in production, you'd get these from the comparison
    getComparison(1, comparisonId)
      .then(data => {
        setComparisonData(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [comparisonId])

  return (
    <div style={{ width: '100%', height: '600px', position: 'relative' }}>
      {loading && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 10,
          color: '#333'
        }}>
          Loading mesh...
        </div>
      )}
      
      {error && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 10,
          color: 'red',
          background: 'white',
          padding: '20px',
          borderRadius: '8px'
        }}>
          Error: {error}
        </div>
      )}

      {!comparisonData && !loading && !error && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 10,
          color: '#666',
          background: 'white',
          padding: '20px',
          borderRadius: '8px'
        }}>
          Select a comparison to view 3D mesh
        </div>
      )}

      <Canvas>
        <PerspectiveCamera makeDefault position={[0, 0, 5]} />
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <OrbitControls />
        <MeshModel comparisonData={comparisonData} />
        <gridHelper args={[10, 10]} />
      </Canvas>

      {comparisonData && (
        <div style={{
          position: 'absolute',
          bottom: '20px',
          left: '20px',
          background: 'rgba(255, 255, 255, 0.9)',
          padding: '10px',
          borderRadius: '8px',
          fontSize: '12px'
        }}>
          <div>🟢 Green = Reduction</div>
          <div>🔴 Red = Increase</div>
          <div>⚪ White = No Change</div>
        </div>
      )}
    </div>
  )
}

