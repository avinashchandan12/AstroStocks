// TypeScript types matching backend API schemas

export interface SectorPrediction {
  sector: string
  planetary_influence: string
  trend: string
  reason: string
  top_stocks?: string[]
  accuracy_estimate?: number
  sector_id?: number
  sector_name?: string
  confidence?: string // 'Low' | 'Medium' | 'High'
  ai_insights?: string // JSON string containing AI insights
}

export interface PlanetaryTransit {
  planet: string
  longitude: number
  latitude: number
  sign: string
  degree_in_sign: number
  dignity: string
  retrograde: boolean
  motion: string
  speed: number
  status?: string
  date?: string
  nakshatra?: string
}

export interface KeyInfluence {
  planet: string
  sign: string
  influence_type: string
  strength: number
  description: string
}

export interface MarketPrediction {
  overall_sentiment: string
  sector_predictions: SectorPrediction[]
  key_influences?: KeyInfluence[]
  ai_analysis?: string
}

export interface LocationInfo {
  latitude: number
  longitude: number
  timezone: string
}

export interface PredictRequest {
  date?: string
  time?: string
  latitude?: number
  longitude?: number
  timezone?: string
}

export interface PredictResponse {
  prediction_date: string
  location: LocationInfo
  planetary_transits: PlanetaryTransit[]
  market_prediction: MarketPrediction
  past_market_data?: any
  confidence: number
}

export interface AnalyzeRequest {
  stocks?: Stock[]
  transits?: any
}

export interface Stock {
  symbol: string
  script_code?: string
  sector: string
  sector_id?: number
  past_6m_return?: number
  volatility?: string
  pe_ratio?: number
  price_trend?: string
  news_sentiment?: string
}

export interface AnalyzeResponse {
  sector_predictions: SectorPrediction[]
  overall_market_sentiment?: string
  accuracy_estimate?: string
  timestamp?: string
}

export interface EnhancedAnalyzeResponse {
  top_recommendations: Array<{
    symbol: string
    sector: string
    recommendation: string
    reasoning: string
    confidence: number
  }>
  sector_analysis: Array<{
    sector: string
    planetary_influence: string
    trend: string
    ai_insights: string
    confidence: number
    stocks_in_sector?: Stock[]
  }>
  overall_market_sentiment: string
  timestamp: string
}

export interface Sector {
  id: number
  name: string
  description?: string
  past_6m_return?: number
  past_1y_return?: number
  volatility?: string
  market_cap?: number
  exchange?: string
  country?: string
  created_at: string
  updated_at?: string
}

export interface StreamingChunk {
  status: 'started' | 'processing' | 'complete' | 'error'
  message?: string
  stage?: string
  data?: any
  error?: string
  date?: string
  count?: number
  index?: number
}

