import { useCallback, useRef } from 'react';
import { FileText, Check, X, Loader2, Upload } from 'lucide-react';
import { formatFileSize } from '@/lib/utils';
import type { DocumentType, DocumentUpload } from '@/types';

interface FileUploadSectionProps {
  uploads: Record<DocumentType, DocumentUpload>;
  onUpload: (type: DocumentType, file: File) => void;
  onRemove: (type: DocumentType) => void;
}

interface UploadBoxProps {
  document: DocumentUpload;
  onUpload: (file: File) => void;
  onRemove: () => void;
}

function UploadBox({ document, onUpload, onRemove }: UploadBoxProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onUpload(file);
    }
  };

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      const file = e.dataTransfer.files?.[0];
      if (file) {
        onUpload(file);
      }
    },
    [onUpload]
  );

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const file = document.file;
  const isUploading = file?.status === 'uploading';
  const isSuccess = file?.status === 'success';
  const isError = file?.status === 'error';

  return (
    <div className="space-y-2">
      {/* Label */}
      <div className="flex items-center gap-1.5">
        <FileText className="w-4 h-4 text-finance-primary" />
        <span className="text-sm font-medium text-finance-text">
          {document.label}
        </span>
        <span className="text-xs text-finance-text-muted">
          ({document.labelEn})
        </span>
        {document.required && <span className="text-finance-error">*</span>}
      </div>

      {/* Upload Zone */}
      <div
        onClick={handleClick}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        className={`
          relative border-2 rounded-lg p-4 cursor-pointer transition-all duration-200
          ${
            isSuccess
              ? 'border-finance-success bg-green-50'
              : isError
              ? 'border-finance-error bg-red-50'
              : 'border-dashed border-finance-border hover:border-finance-primary'
          }
        `}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={handleFileChange}
          className="hidden"
        />

        {!file && (
          <div className="text-center py-2">
            <Upload className="w-8 h-8 mx-auto mb-2 text-finance-text-muted" />
            <p className="text-sm text-finance-text-muted">
              将文件拖拽到此处
            </p>
            <p className="text-sm text-finance-text-muted mt-1">
              或 <span className="text-finance-primary">点击选择文件</span>
            </p>
            <p className="text-xs text-finance-text-light mt-2">
              支持 PDF / PNG / JPG
            </p>
          </div>
        )}

        {isUploading && (
          <div className="flex items-center gap-3 py-2">
            <Loader2 className="w-5 h-5 animate-spin text-finance-primary" />
            <div className="flex-1">
              <div className="flex justify-between text-xs mb-1">
                <span className="text-finance-text">{file.name}</span>
                <span className="text-finance-text-muted">
                  {Math.round(file.progress)}%
                </span>
              </div>
              <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-finance-primary transition-all duration-200"
                  style={{ width: `${file.progress}%` }}
                />
              </div>
            </div>
          </div>
        )}

        {isSuccess && (
          <div className="flex items-center justify-between py-1">
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-finance-success" />
              <span className="text-sm text-finance-text truncate max-w-[200px]">
                {file.name}
              </span>
              <span className="text-xs text-finance-text-muted">
                ({formatFileSize(file.size)})
              </span>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onRemove();
              }}
              className="p-1 hover:bg-red-100 rounded transition-colors"
            >
              <X className="w-4 h-4 text-finance-text-muted hover:text-finance-error" />
            </button>
          </div>
        )}

        {isError && (
          <div className="flex items-center gap-2 py-2">
            <X className="w-5 h-5 text-finance-error" />
            <span className="text-sm text-finance-error">{file.errorMessage}</span>
          </div>
        )}
      </div>
    </div>
  );
}

export function FileUploadSection({ uploads, onUpload, onRemove }: FileUploadSectionProps) {
  return (
    <div className="finance-card">
      {/* Title */}
      <div className="mb-4">
        <h2 className="text-base font-bold text-finance-primary flex items-center gap-2">
          <span>📁</span> 单据上传
        </h2>
        <div className="h-0.5 bg-finance-gold mt-2" />
      </div>

      {/* Upload Boxes */}
      <div className="space-y-3">
        {(Object.values(uploads) as DocumentUpload[]).map((doc) => (
          <UploadBox
            key={doc.type}
            document={doc}
            onUpload={(file) => onUpload(doc.type, file)}
            onRemove={() => onRemove(doc.type)}
          />
        ))}
      </div>
    </div>
  );
}
