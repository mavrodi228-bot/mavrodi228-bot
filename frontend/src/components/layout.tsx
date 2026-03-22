import { Link, NavLink } from 'react-router-dom'
import { Badge } from '@/components/ui'
import type { PropsWithChildren } from 'react'

const navItems = [
  ['Dashboard', '/dashboard'],
  ['Transactions', '/transactions'],
  ['Import', '/import'],
  ['Analytics', '/analytics'],
  ['Goals', '/goals'],
  ['Recommendations', '/recommendations'],
  ['Settings', '/settings'],
]

export const AppLayout = ({ children }: PropsWithChildren) => (
  <div className="min-h-screen bg-slate-950 text-slate-100">
    <header className="sticky top-0 z-10 border-b border-white/10 bg-slate-950/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link to="/dashboard" className="flex items-center gap-3 text-lg font-semibold text-white">
          <div className="h-10 w-10 rounded-2xl bg-emerald-500/20 p-2 text-center text-emerald-300">₽</div>
          CashLens
        </Link>
        <Badge>Single-user MVP</Badge>
      </div>
    </header>
    <div className="mx-auto grid max-w-7xl grid-cols-1 gap-8 px-6 py-8 lg:grid-cols-[220px_1fr]">
      <aside className="rounded-3xl border border-white/10 bg-slate-900/70 p-4">
        <nav className="space-y-2">
          {navItems.map(([label, href]) => (
            <NavLink
              key={href}
              to={href}
              className={({ isActive }) =>
                `block rounded-2xl px-4 py-3 text-sm transition ${isActive ? 'bg-emerald-500/15 text-white' : 'text-slate-400 hover:bg-white/5 hover:text-white'}`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="space-y-8">{children}</main>
    </div>
  </div>
)
