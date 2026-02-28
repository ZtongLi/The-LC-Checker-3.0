import { CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import type { SystemStatus } from '@/types';

interface StatusBarProps {
  status?: SystemStatus;
}

export function StatusBar({ status = 'ready' }: StatusBarProps) {
  const isReady = status === 'ready';
  const isError = status === 'error';
  const isProcessing = status === 'processing';

  return (
    <div
      className={`h-10 flex items-center justify-center gap-2 text-xs ${
        isError
          ? 'bg-finance-status-error text-finance-error'
          : 'bg-finance-status-ok text-finance-success'
      }`}
    >
      {isReady && <CheckCircle2 className="w-4 h-4" />}
      {isError && <AlertCircle className="w-4 h-4" />}
      {isProcessing && <Loader2 className="w-4 h-4 animate-spin" />}
      
      <span className="font-medium">
        {isReady && '🟢 系统就绪'}
        {isError && '🔴 系统异常'}
        {isProcessing && '⏳ 系统处理中'}
        {' | '}
      </span>
      
      <span>
        模型：Qwen2.5-14B | 知识库：UCP600 (10条) | GPU：RTX 4090
      </span>
    </div>
  );
}
