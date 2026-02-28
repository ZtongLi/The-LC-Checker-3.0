import { Check, ChevronDown } from 'lucide-react';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import type { ComplianceItem } from '@/types';

interface ComplianceListProps {
  items: ComplianceItem[];
}

export function ComplianceList({ items }: ComplianceListProps) {
  if (items.length === 0) return null;

  return (
    <Collapsible defaultOpen={false}>
      <CollapsibleTrigger className="w-full">
        <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
          <h3 className="text-base font-bold text-finance-success flex items-center gap-2">
            <Check className="w-5 h-5" />
            相符项目
            <span className="text-sm font-normal text-finance-text-muted">
              ({items.length} 项)
            </span>
          </h3>
          <ChevronDown className="w-5 h-5 text-finance-success transition-transform data-[state=open]:rotate-180" />
        </div>
      </CollapsibleTrigger>
      
      <CollapsibleContent>
        <div className="mt-3 bg-green-50/50 rounded-lg p-4">
          <div className="space-y-2">
            {items.map((item) => (
              <div
                key={item.id}
                className="flex items-start gap-2 text-sm text-finance-success"
              >
                <Check className="w-4 h-4 mt-0.5 flex-shrink-0" />
                <span>
                  <span className="font-medium">{item.document}</span>
                  {' — '}
                  {item.description}
                </span>
              </div>
            ))}
          </div>
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}
