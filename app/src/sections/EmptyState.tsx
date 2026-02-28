import { FileSearch, FileText, Brain, ClipboardList } from 'lucide-react';

export function EmptyState() {
  return (
    <div className="finance-card h-full flex flex-col items-center justify-center py-16">
      {/* Main Icon */}
      <div className="relative mb-6">
        <FileSearch className="w-28 h-28 text-finance-border" strokeWidth={1} />
      </div>

      {/* Title */}
      <h3 className="text-xl text-finance-text-muted font-medium mb-2">
        上传单据，开始智能审核
      </h3>

      {/* Subtitle */}
      <p className="text-sm text-finance-text-light text-center max-w-md mb-10">
        系统将自动对比信用证与各单据，识别不符点并引用 UCP600 条款
      </p>

      {/* Features */}
      <div className="flex items-center gap-8 text-sm text-finance-text-muted">
        <div className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-finance-primary" />
          <span>支持 PDF/图片</span>
        </div>
        <div className="w-px h-4 bg-finance-border" />
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-finance-primary" />
          <span>AI 智能分析</span>
        </div>
        <div className="w-px h-4 bg-finance-border" />
        <div className="flex items-center gap-2">
          <ClipboardList className="w-5 h-5 text-finance-primary" />
          <span>自动生成报告</span>
        </div>
      </div>
    </div>
  );
}
