import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface MeshUpload {
  id: number
  user_id: number
  file_path: string
  version: number
  is_baseline: boolean
  upload_date: string
}

export interface ComparisonData {
  id: number
  baseline_id: number
  comparison_id: number
  statistics: {
    avg_magnitude: number
    max_magnitude: number
    increase_percentage: number
    decrease_percentage: number
  }
  region_statistics: Record<string, {
    total_vertices: number
    avg_magnitude: number
    max_magnitude: number
    increase_percentage: number
    decrease_percentage: number
  }>
  color_data: {
    colors: number[][]
    vertices: number[][]
    color_format: string
    color_range: number[]
  }
  created_at: string
}

export interface Insight {
  id: number
  comparison_id: number
  text: string
  confidence: number
  created_at: string
}

export interface ActionPlan {
  id: number
  user_id: number
  plan_type: string
  content: any
  is_active: boolean
  created_at: string
}

export const uploadMesh = async (file: File, userId: number): Promise<MeshUpload> => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post(`/upload/?user_id=${userId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const getComparison = async (baselineId: number, comparisonId: number): Promise<ComparisonData> => {
  const response = await api.get(`/comparison/${baselineId}/${comparisonId}`)
  return response.data
}

export const getLatestComparison = async (userId: number): Promise<ComparisonData> => {
  const response = await api.get(`/comparison/user/${userId}/latest`)
  return response.data
}

export const getInsights = async (comparisonId: number): Promise<Insight> => {
  const response = await api.get(`/insights/${comparisonId}`)
  return response.data
}

export const getActionPlans = async (userId: number): Promise<ActionPlan[]> => {
  const response = await api.get(`/actions/${userId}`)
  return response.data
}

export const listUserMeshes = async (userId: number): Promise<MeshUpload[]> => {
  const response = await api.get(`/upload/user/${userId}`)
  return response.data
}

