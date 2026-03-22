import { useState, type ChangeEvent } from 'react'
import { Card, SectionTitle } from '@/components/ui'
import { api } from '@/api/client'

export const ImportPage = () => {
  const [message, setMessage] = useState('Upload a T-Bank CSV or XLSX statement to preview and import it.')

  const handleFile = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    const endpoint = file.name.endsWith('.xlsx') ? '/transactions/import/xlsx' : '/transactions/import/csv'
    const response = await api.post(endpoint, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    setMessage(`Imported ${response.data.imported_rows} rows, skipped ${response.data.skipped_rows}.`)
  }

  return (
    <div className="space-y-6">
      <SectionTitle title="Import statements" subtitle="Official fallback path for T-Bank retail exports (CSV/XLSX)." />
      <Card className="space-y-4">
        <label className="flex cursor-pointer items-center justify-center rounded-3xl border border-dashed border-emerald-500/30 bg-emerald-500/5 p-12 text-center text-slate-300">
          <input type="file" className="hidden" accept=".csv,.xlsx" onChange={handleFile} />
          <span>Select CSV or XLSX statement</span>
        </label>
        <p className="text-sm text-slate-400">{message}</p>
        <ul className="space-y-2 text-sm text-slate-400">
          <li>• Supports preview-friendly structured CSV/XLSX files from T-Bank exports.</li>
          <li>• Deduplicates by external ID or normalized date + amount + description.</li>
          <li>• Runs rule-based categorization after import.</li>
        </ul>
      </Card>
    </div>
  )
}
