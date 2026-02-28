import { Shield, Search } from 'lucide-react';

export function Header() {
  return (
    <header className="h-16 bg-finance-primary flex items-center justify-between px-6">
      {/* Logo and Title */}
      <div className="flex items-center gap-3">
        <div className="relative w-10 h-10 flex items-center justify-center">
          <Shield className="w-10 h-10 text-white" strokeWidth={1.5} />
          <Search className="w-5 h-5 text-finance-gold absolute" strokeWidth={2.5} />
        </div>
        <div className="flex flex-col">
          <h1 className="text-white text-lg font-bold leading-tight">
            信用证智能审单辅助系统
          </h1>
          <span className="text-white/70 text-xs">
            LC Document Examination Assistant
          </span>
        </div>
      </div>

      {/* Version */}
      <div className="flex items-center">
        <span className="text-finance-gold text-xs font-medium">
          V2.0 — AI 驱动
        </span>
      </div>
    </header>
  );
}
