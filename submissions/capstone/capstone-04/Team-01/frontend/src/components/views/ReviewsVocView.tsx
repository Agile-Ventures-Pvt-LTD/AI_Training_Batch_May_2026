import React from 'react';
import {
  Star,
  MessageSquare,
  ThumbsUp,
  ThumbsDown,
  AlertTriangle,
  Sparkles,
  Filter
} from 'lucide-react';
import { VOCFeedback, MarketplaceId } from '../../types';
import { useData } from '../../context/DataContext';

export const ReviewsVocView: React.FC = () => {
  const { skus } = useData();
  const [filterSentiment, setFilterSentiment] = React.useState<'all' | 'Positive' | 'Negative' | 'Neutral'>('all');

  const dynamicFeedback: VOCFeedback[] = React.useMemo(() => {
    const list: VOCFeedback[] = [];
    skus.forEach((sku, idx) => {
      list.push({
        id: `voc-${sku.sku}-1`,
        sku: sku.sku,
        productName: sku.name,
        marketplace: (idx % 3 === 0 ? 'amazon' : idx % 3 === 1 ? 'blinkit' : 'zepto') as MarketplaceId,
        rating: 5,
        reviewTitle: `Outstanding quality & authentic ${sku.name}`,
        reviewBody: `Received in pristine condition via quick commerce. The packaging was sealed with batch barcode verification. Genuine quality product!`,
        sentiment: 'Positive',
        categoryTag: 'Quality & Authenticity',
        customerName: `Verified Buyer (${sku.brand || 'Customer'})`,
        date: '2 days ago',
        defectReported: false
      });

      if (idx % 2 === 0) {
        list.push({
          id: `voc-${sku.sku}-2`,
          sku: sku.sku,
          productName: sku.name,
          marketplace: 'flipkart',
          rating: 2,
          reviewTitle: `Outer tamper seal slightly pressed during transit`,
          reviewBody: `Product contents inside were intact, but secondary courier transit cardboard was crushed at the corner. Need better transit protective buffer for ${sku.sku}.`,
          sentiment: 'Negative',
          categoryTag: 'Packaging Transit Buffer',
          customerName: 'Verified Customer',
          date: 'Yesterday',
          defectReported: true
        });
      }
    });
    return list;
  }, [skus]);

  const filtered = dynamicFeedback.filter((item) => {
    if (filterSentiment !== 'all' && item.sentiment !== filterSentiment) return false;
    return true;
  });

  return (
    <div id="reviews-voc-view" className="space-y-6">
      {/* Header */}
      <div className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Voice of Customer (VOC) & Review Intelligence</h2>
          <p className="text-xs text-slate-500 mt-1">
            Automated customer sentiment clustering, packaging defect detection, and quality feedback loops
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-center">
            <span className="text-[10px] uppercase font-bold text-emerald-800 block">Catalog CSAT</span>
            <span className="text-base font-bold text-emerald-700">88% Positive</span>
          </div>
        </div>
      </div>

      {/* Filter Chips */}
      <div className="flex items-center space-x-2 bg-white p-3.5 border border-slate-200 rounded-xl shadow-xs text-xs">
        <span className="font-semibold text-slate-600">Sentiment:</span>
        {(['all', 'Positive', 'Negative', 'Neutral'] as const).map((st) => (
          <button
            key={st}
            onClick={() => setFilterSentiment(st)}
            className={`px-3 py-1 rounded-md font-medium transition-all ${
              filterSentiment === st
                ? 'bg-blue-600 text-white shadow-2xs'
                : 'bg-slate-100 border border-slate-200 text-slate-700 hover:bg-slate-200'
            }`}
          >
            {st === 'all' ? 'All Reviews' : st}
          </button>
        ))}
      </div>

      {/* Review Feed */}
      <div className="space-y-3">
        {filtered.map((item) => {
          const isNegative = item.sentiment === 'Negative';

          return (
            <div
              key={item.id}
              className={`p-4 bg-white rounded-xl border shadow-xs space-y-2.5 ${
                isNegative ? 'border-rose-200' : 'border-slate-200'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-xs text-slate-900">{item.productName}</span>
                  <span className="text-[10px] uppercase font-bold text-slate-600 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded">
                    {item.channel}
                  </span>
                </div>
                <div className="flex items-center space-x-1 text-amber-500 text-xs font-bold">
                  <span>★</span>
                  <span>{item.rating}.0</span>
                </div>
              </div>

              <p className="text-xs text-slate-700 italic">"{item.reviewText}"</p>

              <div className="flex items-center justify-between text-[11px] pt-2 border-t border-slate-100">
                <div className="flex items-center space-x-1.5">
                  <span className="text-slate-500">Extracted Topic:</span>
                  <span className="font-semibold text-slate-800 bg-slate-50 border border-slate-200 px-2 py-0.5 rounded">
                    {item.extractedTopic}
                  </span>
                </div>

                {item.defectCategory && (
                  <span className="text-rose-700 font-bold bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                    Defect: {item.defectCategory}
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
