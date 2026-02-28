import { FileText, ChevronDown } from 'lucide-react';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import type { DocumentFields as DocumentFieldsType } from '@/types';

interface DocumentFieldsProps {
  documents: DocumentFieldsType[];
}

export function DocumentFieldsSection({ documents }: DocumentFieldsProps) {
  if (documents.length === 0) return null;

  return (
    <Collapsible defaultOpen={false}>
      <CollapsibleTrigger className="w-full">
        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
          <h3 className="text-base font-bold text-finance-primary flex items-center gap-2">
            <FileText className="w-5 h-5" />
            单据字段详情
          </h3>
          <ChevronDown className="w-5 h-5 text-finance-primary transition-transform data-[state=open]:rotate-180" />
        </div>
      </CollapsibleTrigger>

      <CollapsibleContent>
        <div className="mt-3 space-y-3">
          {documents.map((doc) => (
            <Collapsible key={doc.type} defaultOpen={false}>
              <CollapsibleTrigger className="w-full">
                <div className="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-finance-text">
                      {doc.name}
                    </span>
                    <span className="text-xs text-finance-text-muted">
                      ({doc.nameEn})
                    </span>
                  </div>
                  <ChevronDown className="w-4 h-4 text-finance-text-muted transition-transform data-[state=open]:rotate-180" />
                </div>
              </CollapsibleTrigger>

              <CollapsibleContent>
                <div className="mt-2 border border-gray-200 rounded-lg overflow-hidden">
                  <table className="w-full text-sm">
                    <tbody>
                      {doc.fields.map((field, index) => (
                        <tr
                          key={field.key}
                          className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}
                        >
                          <td className="py-2.5 px-4 text-right text-finance-text-muted w-36">
                            {field.key}
                          </td>
                          <td className="py-2.5 px-4 text-finance-text">
                            {field.key.includes('金额') || field.key.includes('Amount') ? (
                              <span className="font-mono">{field.value}</span>
                            ) : (
                              field.value
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CollapsibleContent>
            </Collapsible>
          ))}
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}
