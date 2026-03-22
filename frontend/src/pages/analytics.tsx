import { Card, SectionTitle, Skeleton } from '@/components/ui'
import { CategoryBarChart, SpendLineChart } from '@/components/charts'
import { useAnalyticsOverview, useCategoryAnalytics } from '@/hooks/useAnalytics'
import { formatCurrency } from '@/lib/utils'

export const AnalyticsPage = () => {
  const overview = useAnalyticsOverview()
  const categories = useCategoryAnalytics()
  if (overview.isLoading || categories.isLoading || !overview.data || !categories.data) {
    return <Skeleton className="h-[480px]" />
  }

  return (
    <div className="space-y-6">
      <SectionTitle title="Analytics" subtitle="Deep dive into your spending efficiency and trends." />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <Card><p className="text-sm text-slate-400">Average daily spend</p><p className="mt-3 text-2xl font-semibold">{formatCurrency(overview.data.average_daily_spending)}</p></Card>
        <Card><p className="text-sm text-slate-400">Average transaction</p><p className="mt-3 text-2xl font-semibold">{formatCurrency(overview.data.average_transaction_amount)}</p></Card>
        <Card><p className="text-sm text-slate-400">MoM delta</p><p className="mt-3 text-2xl font-semibold">{formatCurrency(overview.data.month_over_month_delta)}</p></Card>
        <Card><p className="text-sm text-slate-400">Small frequent spend</p><p className="mt-3 text-2xl font-semibold">{formatCurrency(overview.data.small_frequent_expenses_total)}</p></Card>
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        <Card>
          <SectionTitle title="Top categories" />
          <CategoryBarChart data={categories.data.top_expense_categories} />
        </Card>
        <Card>
          <SectionTitle title="Daily trend" />
          <SpendLineChart data={categories.data.daily_spend_chart} />
        </Card>
      </div>
    </div>
  )
}
