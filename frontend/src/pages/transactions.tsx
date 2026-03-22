import { Card, SectionTitle, Skeleton } from '@/components/ui'
import { useTransactions } from '@/hooks/useTransactions'
import { formatCurrency } from '@/lib/utils'

export const TransactionsPage = () => {
  const { data, isLoading } = useTransactions()
  if (isLoading || !data) return <Skeleton className="h-[420px]" />

  return (
    <div className="space-y-6">
      <SectionTitle title="Transactions" subtitle="Review, search, and correct categorized transactions." />
      <Card>
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-slate-400">
              <tr>
                <th className="pb-3">Date</th>
                <th className="pb-3">Description</th>
                <th className="pb-3">Category</th>
                <th className="pb-3 text-right">Amount</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {data.map((transaction) => (
                <tr key={transaction.id}>
                  <td className="py-4 pr-4 text-slate-300">{transaction.date}</td>
                  <td className="py-4 pr-4">
                    <div className="font-medium text-white">{transaction.description}</div>
                    <div className="text-xs text-slate-500">{transaction.merchant}</div>
                  </td>
                  <td className="py-4 pr-4 text-slate-300">{transaction.category?.name ?? 'Uncategorized'}</td>
                  <td className="py-4 text-right font-medium text-white">{formatCurrency(Number(transaction.amount))}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
