import { useState, useEffect } from 'react'
import { getActionPlans } from '../services/api'
import type { ActionPlan } from '../services/api'

interface ActionPlansProps {
  userId: number
}

export default function ActionPlans({ userId }: ActionPlansProps) {
  const [plans, setPlans] = useState<ActionPlan[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getActionPlans(userId)
      .then(setPlans)
      .catch(err => {
        console.error('Error loading action plans:', err)
        setPlans([])
      })
      .finally(() => setLoading(false))
  }, [userId])

  if (loading) {
    return (
      <div className="info-panel">
        <h3>Action Plans</h3>
        <p>Loading plans...</p>
      </div>
    )
  }

  if (plans.length === 0) {
    return (
      <div className="info-panel">
        <h3>Action Plans</h3>
        <p>No action plans available. Upload meshes to generate plans.</p>
      </div>
    )
  }

  return (
    <div className="info-panel">
      <h3>Action Plans</h3>
      {plans.map(plan => (
        <div key={plan.id} className="action-plan">
          <h4>{plan.plan_type === 'meal' ? '🍽️ Meal Plan' : '🏋️ Training Plan'}</h4>
          
          {plan.plan_type === 'meal' && plan.content.plan && (
            <div className="plan-content">
              <div><strong>Breakfast:</strong> {plan.content.plan.breakfast}</div>
              <div><strong>Lunch:</strong> {plan.content.plan.lunch}</div>
              <div><strong>Dinner:</strong> {plan.content.plan.dinner}</div>
              {plan.content.plan.snacks && (
                <div><strong>Snacks:</strong> {plan.content.plan.snacks}</div>
              )}
              <div style={{ marginTop: '10px', fontSize: '0.9em', color: '#666' }}>
                {plan.content.plan.calories}
              </div>
            </div>
          )}
          
          {plan.plan_type === 'training' && plan.content.schedule && (
            <div className="plan-content">
              {Object.entries(plan.content.schedule).map(([day, activity]) => (
                <div key={day}>
                  <strong>{day.replace('_', ' ').toUpperCase()}:</strong> {activity as string}
                </div>
              ))}
              <div style={{ marginTop: '10px', fontSize: '0.9em', color: '#666' }}>
                {plan.content.notes}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

