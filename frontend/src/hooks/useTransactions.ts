import { useQuery } from '@tanstack/react-query'
import { api } from '@/api/client'
import type { Transaction } from '@/types/api'

export const useTransactions = () =>
  useQuery({
    queryKey: ['transactions'],
    queryFn: async () => (await api.get<Transaction[]>('/transactions')).data,
  })
