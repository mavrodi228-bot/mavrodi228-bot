import { Routes, Route, Navigate } from 'react-router-dom'
import { AppLayout } from '@/components/layout'
import { DashboardPage } from '@/pages/dashboard'
import { TransactionsPage } from '@/pages/transactions'
import { ImportPage } from '@/pages/import'
import { AnalyticsPage } from '@/pages/analytics'
import { GoalsPage } from '@/pages/goals'
import { RecommendationsPage } from '@/pages/recommendations'
import { SettingsPage } from '@/pages/settings'

export const AppRouter = () => (
  <AppLayout>
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/transactions" element={<TransactionsPage />} />
      <Route path="/import" element={<ImportPage />} />
      <Route path="/analytics" element={<AnalyticsPage />} />
      <Route path="/goals" element={<GoalsPage />} />
      <Route path="/recommendations" element={<RecommendationsPage />} />
      <Route path="/settings" element={<SettingsPage />} />
    </Routes>
  </AppLayout>
)
