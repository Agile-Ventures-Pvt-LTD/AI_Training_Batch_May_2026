/**
 * Safe formatting utilities that guarantee zero runtime TypeError on undefined or null values.
 */

export function formatCurrency(value?: number | null): string {
  if (value === undefined || value === null || isNaN(Number(value))) {
    return '₹0';
  }
  return `₹${Math.round(Number(value)).toLocaleString('en-IN')}`;
}

export function formatNumber(value?: number | null): string {
  if (value === undefined || value === null || isNaN(Number(value))) {
    return '0';
  }
  return Number(value).toLocaleString('en-IN');
}

export function formatPercent(value?: number | null, decimals = 1): string {
  if (value === undefined || value === null || isNaN(Number(value))) {
    return '0%';
  }
  return `${Number(value).toFixed(decimals)}%`;
}
