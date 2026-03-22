import { ResponsiveContainer, LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, BarChart, Bar } from 'recharts'
import type { ChartPoint, MoneyPoint } from '@/types/api'

export const SpendLineChart = ({ data }: { data: ChartPoint[] }) => (
  <div className="h-72 w-full">
    <ResponsiveContainer>
      <LineChart data={data}>
        <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
        <XAxis dataKey="date" stroke="#64748b" />
        <YAxis stroke="#64748b" />
        <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid rgba(255,255,255,0.08)' }} />
        <Line type="monotone" dataKey="value" stroke="#22c55e" strokeWidth={3} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  </div>
)

const colors = ['#22c55e', '#38bdf8', '#f97316', '#8b5cf6', '#eab308', '#ef4444', '#14b8a6']

export const CategoryPieChart = ({ data }: { data: MoneyPoint[] }) => (
  <div className="h-72 w-full">
    <ResponsiveContainer>
      <PieChart>
        <Pie data={data} dataKey="amount" nameKey="label" innerRadius={72} outerRadius={108} paddingAngle={3}>
          {data.map((entry, index) => (
            <Cell key={entry.label} fill={colors[index % colors.length]} />
          ))}
        </Pie>
        <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid rgba(255,255,255,0.08)' }} />
      </PieChart>
    </ResponsiveContainer>
  </div>
)

export const CategoryBarChart = ({ data }: { data: MoneyPoint[] }) => (
  <div className="h-72 w-full">
    <ResponsiveContainer>
      <BarChart data={data}>
        <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
        <XAxis dataKey="label" stroke="#64748b" />
        <YAxis stroke="#64748b" />
        <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid rgba(255,255,255,0.08)' }} />
        <Bar dataKey="amount" fill="#38bdf8" radius={[10, 10, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  </div>
)
