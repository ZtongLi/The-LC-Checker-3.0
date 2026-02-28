import { AlertTriangle, CheckCircle } from 'lucide-react';
import type { AuditResult } from '@/types';

interface ResultSummaryProps {
  result: AuditResult;
}

export function ResultSummary({ result }: ResultSummaryProps) {
  const { hasDiscrepancies, severeCount, normalCount, minorCount, recommendation } = result;

  if (!hasDiscrepancies) {
    return (
      <div className="finance-card border-l-4 border-l-finance-success bg-finance-status-ok animate-flash">
        <div className="flex items-start gap-4">
          <CheckCircle className="w-10 h-10 text-finance-success flex-shrink-0" />
          <div>
            <h3 className="text-2xl font-bold text-finance-success mb-2">
              所有单据相符
            </h3>
            <p className="text-sm text-finance-text">
              经系统审核，所有单据与信用证条款一致，未发现不符点。
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div 
      className="finance-card border-l-4 border-l-finance-warning bg-finance-summary-warning animate-flash"
    >
      <div className="flex items-start gap-4">
        <AlertTriangle className="w-10 h-10 text-finance-warning flex-shrink-0" />
        <div className="flex-1">
          <h3 className="text-2xl font-bold text-finance-warning mb-2">
            发现 {severeCount + normalCount + minorCount} 处不符点
          </h3>
          
          {/* Severity Counts */}
          <div className="flex items-center gap-4 text-sm mb-3">
            <span>
              <span className="text-finance-error font-medium">严重 {severeCount} 处</span>
            </span>
            <span className="text-finance-text-muted">·</span>
            <span>
              <span className="text-finance-warning font-medium">一般 {normalCount} 处</span>
            </span>
            <span className="text-finance-text-muted">·</span>
            <span>
              <span className="text-finance-minor font-medium">轻微 {minorCount} 处</span>
            </span>
          </div>

          {/* Recommendation */}
          <p className="text-sm text-finance-text">
            <span className="font-medium">审核建议：</span>
            {recommendation}
          </p>
        </div>
      </div>
    </div>
  );
}
