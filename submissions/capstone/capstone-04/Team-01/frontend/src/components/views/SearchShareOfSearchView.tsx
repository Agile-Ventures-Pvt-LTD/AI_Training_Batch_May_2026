import React from 'react';
import {
  Search,
  TrendingUp,
  TrendingDown,
  Sparkles,
  ArrowUpRight,
  ArrowDownRight,
  Target,
  ExternalLink
} from 'lucide-react';
import { MarketplaceId, SearchKeywordItem } from '../../types';
import { useData } from '../../context/DataContext';

interface SearchShareOfSearchViewProps {
  selectedChannel: MarketplaceId | 'all';
}

export const SearchShareOfSearchView: React.FC<SearchShareOfSearchViewProps> = ({
  selectedChannel
}) => {
  const { skus } = useData();
  const [searchFilter, setSearchFilter] = React.useState('');

  const dynamicKeywords: SearchKeywordItem[] = skus.flatMap((s, idx) => {
    const rawTitle = s.name.replace(/\(.*?\)/g, '').trim();
    const shortName = rawTitle.length > 30 ? rawTitle.slice(0, 30) : rawTitle;
    const type = s.productType || 'Ergonomic Support';
    
    return [
      {
        id: `KW-${s.sku}-1`,
        keyword: `${shortName.toLowerCase()}`,
        category: type,
        matchedSku: `${s.sku} - ${s.name.slice(0, 24)}...`,
        marketplace: (s.activeMarketplaces?.[0] || 'amazon') as MarketplaceId,
        searchVolume: 12500 + Math.round((s.sellingPrice || 1000) * 8),
        organicRank: Math.max(1, Math.min(12, Math.round(14 - (s.shareOfSearchPercent || 25) / 3))),
        sponsoredRank: Math.max(1, Math.min(5, Math.round(6 - (s.shareOfSearchPercent || 25) / 5))),
        shareOfSearch: s.shareOfSearchPercent || 26,
        topCompetitor: 'SleepyCat / The Sleep Company',
        rankChange7d: 1
      },
      {
        id: `KW-${s.sku}-2`,
        keyword: `best ${type.toLowerCase()} online`,
        category: type,
        matchedSku: `${s.sku} - ${s.name.slice(0, 24)}...`,
        marketplace: (s.activeMarketplaces?.[1] || 'blinkit') as MarketplaceId,
        searchVolume: 8200 + Math.round((s.sellingPrice || 1000) * 5),
        organicRank: Math.max(2, Math.min(18, Math.round(16 - (s.shareOfSearchPercent || 25) / 3))),
        sponsoredRank: 2,
        shareOfSearch: Math.round((s.shareOfSearchPercent || 26) * 0.8),
        topCompetitor: 'Wakefit Ortho / Emma',
        rankChange7d: -1
      }
    ];
  });

  const filteredKeywords = dynamicKeywords.filter((k) => {
    if (selectedChannel !== 'all' && k.marketplace !== selectedChannel) return false;
    if (searchFilter && !k.keyword.toLowerCase().includes(searchFilter.toLowerCase())) return false;
    return true;
  });

  const avgSos = skus.length > 0
    ? (skus.reduce((sum, s) => sum + (s.shareOfSearchPercent || 24), 0) / skus.length).toFixed(1)
    : '24.8';

  return (
    <div id="search-share-view" className="space-y-6">
      {/* Header */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Search & Share of Search Intelligence</h2>
          <p className="text-xs text-slate-500 mt-1">
            Tracking organic vs sponsored ranks across Amazon, Flipkart, Blinkit, and Zepto for live catalog keywords
          </p>
        </div>

        <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-center">
          <span className="text-[10px] uppercase font-bold text-blue-700 block">Avg Share of Search</span>
          <span className="text-base font-bold text-blue-700">{avgSos}%</span>
        </div>
      </div>

      {/* Keywords Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">Core Keyword Rank Matrix</h3>
          <input
            type="text"
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            placeholder="Filter keywords..."
            className="px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 text-slate-900 placeholder:text-slate-400 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 w-60"
          />
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 text-[11px] uppercase font-bold">
                <th className="py-3 px-4">Search Keyword</th>
                <th className="py-3 px-4">Marketplace</th>
                <th className="py-3 px-4">Monthly Searches</th>
                <th className="py-3 px-4">Organic Rank</th>
                <th className="py-3 px-4">Sponsored Rank</th>
                <th className="py-3 px-4">Share of Search</th>
                <th className="py-3 px-4">Top Competitor</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredKeywords.map((kw) => (
                <tr key={kw.id} className="hover:bg-slate-50 transition-colors">
                  <td className="py-3 px-4">
                    <span className="font-bold text-slate-900">{kw.keyword}</span>
                    <div className="text-[10px] text-slate-500 font-mono">{kw.matchedSku}</div>
                  </td>
                  <td className="py-3 px-4 uppercase font-bold text-[10px] text-slate-600">
                    {kw.marketplace}
                  </td>
                  <td className="py-3 px-4 font-semibold text-slate-800">
                    {kw.searchVolume.toLocaleString()} / mo
                  </td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-200 font-bold rounded">
                      #{kw.organicRank}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 bg-amber-50 text-amber-800 border border-amber-200 font-bold rounded">
                      #{kw.sponsoredRank}
                    </span>
                  </td>
                  <td className="py-3 px-4 font-bold text-slate-900">
                    {kw.shareOfSearch}%
                  </td>
                  <td className="py-3 px-4 text-slate-700 font-medium">
                    {kw.topCompetitor}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
