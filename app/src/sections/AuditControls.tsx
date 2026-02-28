import { Calendar, Search, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import type { AuditStatus } from '@/types';

interface AuditControlsProps {
  presentationDate: string;
  onDateChange: (date: string) => void;
  auditStatus: AuditStatus;
  canStartAudit: boolean;
  onStartAudit: () => void;
}

export function AuditControls({
  presentationDate,
  onDateChange,
  auditStatus,
  canStartAudit,
  onStartAudit,
}: AuditControlsProps) {
  const isAuditing = auditStatus === 'auditing';

  return (
    <div className="space-y-6 mt-4">
      {/* Date Input */}
      <div className="space-y-2">
        <label className="flex items-center gap-1.5 text-sm font-medium text-finance-text">
          <Calendar className="w-4 h-4 text-finance-primary" />
          交单日期 (Presentation Date)
          <span className="text-finance-error">*</span>
        </label>
        <Input
          type="date"
          value={presentationDate}
          onChange={(e) => onDateChange(e.target.value)}
          className="h-10 border-finance-border focus:border-finance-primary focus:ring-finance-primary"
        />
      </div>

      {/* Audit Button */}
      <Button
        onClick={onStartAudit}
        disabled={!canStartAudit || isAuditing}
        className={`
          w-full h-12 text-base font-bold rounded-lg transition-all duration-200
          ${
            canStartAudit && !isAuditing
              ? 'bg-finance-primary hover:bg-finance-primary-light hover:shadow-lg'
              : 'bg-finance-text-muted cursor-not-allowed'
          }
        `}
      >
        {isAuditing ? (
          <>
            <Loader2 className="w-5 h-5 mr-2 animate-spin" />
            正在审核中...
          </>
        ) : (
          <>
            <Search className="w-5 h-5 mr-2" />
            开始审核
          </>
        )}
      </Button>
    </div>
  );
}
