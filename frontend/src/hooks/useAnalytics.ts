import { useQuery } from '@tanstack/react-query'
import { api } from '@/api/client'
import type { AnalyticsOverview, DashboardSummary, Insight } from '@/types/api'

export const useAnalyticsOverview = () =>
  useQuery({
    queryKey: ['analytics-overview'],
    queryFn: async () => (await api.get<AnalyticsOverview>('/analytics/overview')).data,
  })

export const useRecommendations = () =>
  useQuery({
    queryKey: ['recommendations'],
    queryFn: async () => (await api.get<{ insights: Insight[] }>('/recommendations')).data,
  })

export const useCategoryAnalytics = () =>
  useQuery({
    queryKey: ['analytics-categories'],
    queryFn: async () => (await api.get<Pick<DashboardSummary, 'daily_spend_chart' | 'top_expense_categories'>>('/dashboard/charts/monthly')).data,
  })
