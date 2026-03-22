import { useQuery } from '@tanstack/react-query'
import { api } from '@/api/client'
import type { DashboardSummary } from '@/types/api'

export const useDashboard = () =>
  useQuery({
    queryKey: ['dashboard-summary'],
    queryFn: async () => (await api.get<DashboardSummary>('/dashboard/summary')).data,
  })
