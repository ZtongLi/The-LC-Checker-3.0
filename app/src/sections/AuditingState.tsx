import { Loader2 } from 'lucide-react';

export function AuditingState() {
  return (
    <div className="finance-card h-full flex flex-col items-center justify-center py-20">
      <Loader2 className="w-16 h-16 animate-spin text-finance-primary mb-6" />
      <h3 className="text-xl text-finance-text font-medium mb-2">
        正在审核，请稍候...
      </h3>
      <p className="text-sm text-finance-text-muted">
        AI 正在分析单据内容并比对信用证条款
      </p>
    </div>
  );
}
