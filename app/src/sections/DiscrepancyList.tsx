import { AlertCircle } from 'lucide-react';
import type { Discrepancy, Severity } from '@/types';

interface DiscrepancyListProps {
  discrepancies: Discrepancy[];
}

const severityConfig: Record<
  Severity,
  { label: string; color: string; bgColor: string }
> = {
  severe: {
    label: '严重',
    color: 'text-finance-error',
    bgColor: 'bg-finance-error',
  },
  normal: {
    label: '一般',
    color: 'text-finance-warning',
    bgColor: 'bg-finance-warning',
  },
  minor: {
    label: '轻微',
    color: 'text-finance-minor',
    bgColor: 'bg-finance-minor',
  },
};

export function DiscrepancyList({ discrepancies }: DiscrepancyListProps) {
  if (discrepancies.length === 0) return null;

  return (
    <div className="space-y-4">
      {/* Title */}
      <h3 className="text-base font-bold text-finance-primary flex items-center gap-2">
        <AlertCircle className="w-5 h-5" />
        不符点详情
      </h3>

      {/* Discrepancy Cards */}
      <div className="space-y-3">
        {discrepancies.map((item) => {
          const config = severityConfig[item.severity];
          return (
            <div
              key={item.id}
              className={`finance-card border-l-4 ${
                item.severity === 'severe'
                  ? 'border-l-finance-error'
                  : item.severity === 'normal'
                  ? 'border-l-finance-warning'
                  : 'border-l-finance-minor'
              }`}
            >
              {/* Header */}
              <div className="flex items-center justify-between mb-3">
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium text-white ${config.bgColor}`}
                >
                  #{item.id} {config.label}
                </span>
                <span className="text-xs text-finance-text-muted bg-gray-100 px-2 py-0.5 rounded">
                  {item.document}
                </span>
              </div>

              {/* Field */}
              <div className="mb-3">
                <span className="text-sm font-medium text-finance-text">
                  不符字段：{item.field}
                </span>
              </div>

              {/* Comparison */}
              <div className="space-y-2 mb-3">
                <div className="flex items-start gap-2">
                  <span className="text-xs bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded flex-shrink-0">
                    信用证要求
                  </span>
                  <span className="text-sm text-finance-text">{item.lcRequirement}</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded flex-shrink-0">
                    单据显示
                  </span>
                  <span className="text-sm text-finance-text">{item.documentValue}</span>
                </div>
              </div>

              {/* Description */}
              <p className="text-sm text-finance-text mb-2">{item.description}</p>

              {/* UCP Article */}
              <div className="flex items-center gap-1">
                <span className="text-xs text-finance-text-muted">依据条款：</span>
                <button className="text-xs text-finance-primary underline hover:no-underline">
                  {item.ucpArticle}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
