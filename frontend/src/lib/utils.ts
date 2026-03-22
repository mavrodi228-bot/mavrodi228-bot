export const formatCurrency = (value: number) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(value)

export const cn = (...classes: Array<string | false | null | undefined>) => classes.filter(Boolean).join(' ')
