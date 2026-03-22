import { Card, SectionTitle, Skeleton } from '@/components/ui'
import { useRecommendations } from '@/hooks/useAnalytics'

export const RecommendationsPage = () => {
  const { data, isLoading } = useRecommendations()
  if (isLoading || !data) return <Skeleton className="h-[360px]" />

  return (
    <div className="space-y-6">
      <SectionTitle title="Recommendations" subtitle="Generated from transaction trends, recurring spend, and monthly forecast." />
      <div className="space-y-4">
        {data.insights.map((insight) => (
          <Card key={insight.title}>
            <p className="text-lg font-semibold text-white">{insight.title}</p>
            <p className="mt-2 text-sm text-slate-400">{insight.description}</p>
          </Card>
        ))}
      </div>
    </div>
  )
}
