import { useQuery } from '@tanstack/react-query'
import { api } from '@/api/client'
import type { Goal } from '@/types/api'

export const useGoals = () =>
  useQuery({
    queryKey: ['goals'],
    queryFn: async () => (await api.get<Goal[]>('/goals')).data,
  })
