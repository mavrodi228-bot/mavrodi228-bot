import { Card, SectionTitle, Skeleton, Badge } from '@/components/ui'
import { SpendLineChart, CategoryPieChart } from '@/components/charts'
import { useDashboard } from '@/hooks/useDashboard'
import { formatCurrency } from '@/lib/utils'

export const DashboardPage = () => {
  const { data, isLoading } = useDashboard()
  if (isLoading || !data) {
    return <Skeleton className="h-[480px]" />
  }

  const stats = [
    ['Income', data.total_income],
    ['Expenses', data.total_expenses],
    ['Net balance', data.net_balance],
    ['Month-end forecast', data.forecast_balance],
  ]

  return (
    <div className="space-y-8">
      <SectionTitle title="Financial command center" subtitle="Income, expenses, forecast, and score in one place." />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {stats.map(([label, value]) => (
          <Card key={label}>
            <p className="text-sm text-slate-400">{label}</p>
            <p className="mt-3 text-3xl font-semibold text-white">{formatCurrency(Number(value))}</p>
          </Card>
        ))}
      </div>
      <div className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        <Card>
          <SectionTitle title="Spending pace" subtitle="Daily expenses for the current month." />
          <SpendLineChart data={data.daily_spend_chart} />
        </Card>
        <Card>
          <SectionTitle title="Category mix" subtitle="Largest spending buckets." />
          <CategoryPieChart data={data.category_share_chart} />
        </Card>
      </div>
      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card>
          <SectionTitle title="Financial Stability Score" subtitle="Custom metric from 0 to 100." />
          <div className="flex items-center gap-6">
            <div className="flex h-28 w-28 items-center justify-center rounded-full border border-emerald-500/30 bg-emerald-500/10 text-4xl font-semibold text-emerald-300">
              {data.stability_score.score}
            </div>
            <div className="space-y-3">
              <Badge>{data.stability_score.summary}</Badge>
              <ul className="space-y-2 text-sm text-slate-300">
                {data.stability_score.drivers.map((driver) => (
                  <li key={driver}>• {driver}</li>
                ))}
              </ul>
              <p className="text-sm text-slate-400">{data.stability_score.improvements.join(' ')}</p>
            </div>
          </div>
        </Card>
        <Card>
          <SectionTitle title="Insights" subtitle="Auto-generated recommendations and anomalies." />
          <div className="space-y-4">
            {data.insights.map((insight) => (
              <div key={insight.title} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <p className="font-medium text-white">{insight.title}</p>
                <p className="mt-1 text-sm text-slate-400">{insight.description}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
}
