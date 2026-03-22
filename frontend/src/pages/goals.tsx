import { Card, SectionTitle, Skeleton } from '@/components/ui'
import { useGoals } from '@/hooks/useGoals'
import { formatCurrency } from '@/lib/utils'

export const GoalsPage = () => {
  const { data, isLoading } = useGoals()
  if (isLoading || !data) return <Skeleton className="h-[320px]" />

  return (
    <div className="space-y-6">
      <SectionTitle title="Goals" subtitle="Track savings progress and estimated completion dates." />
      <div className="grid gap-4 md:grid-cols-2">
        {data.map((goal) => (
          <Card key={goal.id}>
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-lg font-semibold text-white">{goal.title}</p>
                <p className="mt-1 text-sm text-slate-400">Target {formatCurrency(goal.target_amount)}</p>
              </div>
              <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-slate-300">{goal.status}</span>
            </div>
            <div className="mt-5 h-3 overflow-hidden rounded-full bg-white/5">
              <div className="h-full rounded-full bg-emerald-500" style={{ width: `${Math.min(goal.progress_percent, 100)}%` }} />
            </div>
            <div className="mt-4 flex justify-between text-sm text-slate-400">
              <span>{goal.progress_percent}% funded</span>
              <span>{goal.estimated_completion_date ?? 'Estimate pending'}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
