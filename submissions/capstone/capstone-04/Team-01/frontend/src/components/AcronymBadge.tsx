import React from 'react';
import { ACRONYMS_DICTIONARY } from '../utils/acronyms';
import { HelpCircle, Info } from 'lucide-react';

interface AcronymBadgeProps {
  term: string;
  showIcon?: boolean;
  className?: string;
}

export const AcronymBadge: React.FC<AcronymBadgeProps> = ({
  term,
  showIcon = false,
  className = ''
}) => {
  const def = ACRONYMS_DICTIONARY[term.toUpperCase()];
  const [isOpen, setIsOpen] = React.useState(false);

  if (!def) {
    return <span className={className}>{term}</span>;
  }

  return (
    <span
      className="relative inline-block group"
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
      onClick={(e) => {
        e.stopPropagation();
        setIsOpen(!isOpen);
      }}
    >
      <span
        className={`cursor-help inline-flex items-center underline decoration-dotted decoration-blue-400 underline-offset-2 hover:text-blue-600 transition-colors font-medium ${className}`}
      >
        <span>{def.short}</span>
        {showIcon && <Info className="w-3 h-3 ml-0.5 text-blue-500 inline" />}
      </span>

      {/* Interactive Tooltip Popover */}
      {isOpen && (
        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 p-3 bg-slate-900 text-white rounded-lg shadow-xl z-50 text-xs pointer-events-none animate-in fade-in zoom-in-95 duration-100">
          <div className="flex items-center justify-between pb-1.5 mb-1.5 border-b border-slate-800">
            <span className="font-bold text-emerald-400 font-mono text-[11px]">{def.short}</span>
            <span className="text-[9px] uppercase tracking-wider text-slate-400 font-semibold">{def.category}</span>
          </div>
          <p className="font-bold text-slate-100 text-xs mb-1">{def.full}</p>
          <p className="text-[11px] text-slate-300 leading-snug">{def.description}</p>
          <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-slate-900" />
        </div>
      )}
    </span>
  );
};
