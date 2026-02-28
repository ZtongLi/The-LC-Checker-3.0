import { Check, Loader2, Clock } from 'lucide-react';
import type { AuditStep } from '@/types';

interface AuditProgressProps {
  steps: AuditStep[];
}

export function AuditProgress({ steps }: AuditProgressProps) {
  const hasProcessing = steps.some((step) => step.status === 'processing');
  
  if (!hasProcessing && steps.every((step) => step.status === 'pending')) {
    return null;
  }

  return (
    <div className="mt-4 bg-gray-50 rounded-lg p-4">
      <div className="space-y-2">
        {steps.map((step) => (
          <div key={step.id} className="flex items-center gap-2 text-sm">
            {step.status === 'completed' && (
              <>
                <Check className="w-4 h-4 text-finance-success" />
                <span className="text-finance-success">{step.name}完成</span>
              </>
            )}
            {step.status === 'processing' && (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-finance-primary" />
                <span className="text-finance-primary font-medium">
                  正在{step.name}...
                </span>
              </>
            )}
            {step.status === 'pending' && (
              <>
                <Clock className="w-4 h-4 text-finance-text-light" />
                <span className="text-finance-text-light">{step.name}</span>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
