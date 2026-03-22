export type Insight = { title: string; description: string; severity: string }
export type MoneyPoint = { label: string; amount: number }
export type ChartPoint = { date: string; value: number }

export type DashboardSummary = {
  total_income: number
  total_expenses: number
  net_balance: number
  forecast_expenses: number
  forecast_balance: number
  top_expense_categories: MoneyPoint[]
  daily_spend_chart: ChartPoint[]
  category_share_chart: MoneyPoint[]
  insights: Insight[]
  stability_score: {
    score: number
    summary: string
    drivers: string[]
    improvements: string[]
  }
}

export type Transaction = {
  id: number
  date: string
  description: string
  merchant?: string | null
  amount: number
  direction: string
  currency: string
  category_id?: number | null
  category?: { id: number; name: string; color: string } | null
}

export type Goal = {
  id: number
  title: string
  target_amount: number
  current_amount: number
  monthly_target?: number | null
  deadline?: string | null
  status: string
  progress_percent: number
  estimated_completion_date?: string | null
}

export type AnalyticsOverview = {
  total_income: number
  total_expenses: number
  net_balance: number
  average_daily_spending: number
  average_transaction_amount: number
  month_over_month_delta: number
  weekend_vs_weekday_ratio: number
  small_frequent_expenses_total: number
  financial_stability_score: number
}
