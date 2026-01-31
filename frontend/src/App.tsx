import { useState } from 'react'
import MeshViewer from './components/MeshViewer'
import TimelineSlider from './components/TimelineSlider'
import ComparisonView from './components/ComparisonView'
import InsightsPanel from './components/InsightsPanel'
import ActionPlans from './components/ActionPlans'
import './App.css'
import './components/App.css'

function App() {
  const [selectedComparison, setSelectedComparison] = useState<number | null>(null)
  const [userId] = useState(1) // TODO: Get from auth

  return (
    <div className="app">
      <header className="app-header">
        <h1>3D Body Progress Engine</h1>
        <p>Visualize your body transformation over time</p>
      </header>
      
      <main className="app-main">
        <div className="viewer-section">
          <MeshViewer 
            comparisonId={selectedComparison}
            userId={userId}
          />
          <TimelineSlider 
            userId={userId}
            onComparisonSelect={setSelectedComparison}
          />
        </div>
        
        <div className="info-section">
          <ComparisonView comparisonId={selectedComparison} />
          <InsightsPanel comparisonId={selectedComparison} />
          <ActionPlans userId={userId} />
        </div>
      </main>
    </div>
  )
}

export default App

