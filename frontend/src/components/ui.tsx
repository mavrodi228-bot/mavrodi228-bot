import { cn } from '@/lib/utils'
import type { PropsWithChildren } from 'react'

export const Card = ({ className, children }: PropsWithChildren<{ className?: string }>) => (
  <div className={cn('rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-glow backdrop-blur', className)}>{children}</div>
)

export const SectionTitle = ({ title, subtitle }: { title: string; subtitle?: string }) => (
  <div className="mb-5 flex items-end justify-between gap-4">
    <div>
      <h2 className="text-xl font-semibold text-white">{title}</h2>
      {subtitle ? <p className="text-sm text-slate-400">{subtitle}</p> : null}
    </div>
  </div>
)

export const Badge = ({ children }: PropsWithChildren) => (
  <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-300">{children}</span>
)

export const Skeleton = ({ className = 'h-16' }: { className?: string }) => <div className={cn('animate-pulse rounded-2xl bg-white/5', className)} />
