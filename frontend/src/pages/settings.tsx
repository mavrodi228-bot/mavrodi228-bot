import { Card, SectionTitle } from '@/components/ui'

export const SettingsPage = () => {
  return (
    <div className="space-y-6">
      <SectionTitle title="Bank settings" subtitle="Official T-Bank Business API connection plus resilient CSV fallback." />
      <Card className="space-y-4 text-sm text-slate-400">
        <p>Provider mode A: configure <span className="font-medium text-white">TBankBusinessProvider</span> with env-backed credentials stored encrypted in the backend.</p>
        <p>Provider mode B: import T-Bank CSV/XLSX statements through the Import page when personal banking API access is not available.</p>
        <ul className="space-y-2">
          <li>• <code className="rounded bg-white/5 px-2 py-1">POST /api/integrations/tbank-business/sync</code> for business statements.</li>
          <li>• <code className="rounded bg-white/5 px-2 py-1">POST /api/transactions/import/csv</code> or <code className="rounded bg-white/5 px-2 py-1">/xlsx</code> for fallback uploads.</li>
        </ul>
      </Card>
    </div>
  )
}
