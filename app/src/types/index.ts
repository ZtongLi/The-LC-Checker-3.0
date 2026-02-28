// 文件上传状态
export interface FileUpload {
  id: string;
  name: string;
  size: number;
  status: 'idle' | 'uploading' | 'success' | 'error';
  progress: number;
  errorMessage?: string;
}

// 上传文件类型
export type DocumentType = 'lc' | 'invoice' | 'bl' | 'insurance';

export interface DocumentUpload {
  type: DocumentType;
  label: string;
  labelEn: string;
  required: boolean;
  file: FileUpload | null;
}

// 不符点严重程度
export type Severity = 'severe' | 'normal' | 'minor';

// 不符点详情
export interface Discrepancy {
  id: number;
  severity: Severity;
  document: string;
  field: string;
  lcRequirement: string;
  documentValue: string;
  description: string;
  ucpArticle: string;
}

// 相符项目
export interface ComplianceItem {
  id: number;
  document: string;
  description: string;
}

// 提取的字段
export interface ExtractedField {
  key: string;
  value: string;
}

export interface DocumentFields {
  type: DocumentType;
  name: string;
  nameEn: string;
  fields: ExtractedField[];
}

// 审核进度步骤
export interface AuditStep {
  id: number;
  name: string;
  status: 'pending' | 'processing' | 'completed';
}

// 审核结果
export interface AuditResult {
  hasDiscrepancies: boolean;
  severeCount: number;
  normalCount: number;
  minorCount: number;
  recommendation: string;
  discrepancies: Discrepancy[];
  complianceItems: ComplianceItem[];
  documentFields: DocumentFields[];
}

// 系统状态
export type SystemStatus = 'ready' | 'error' | 'processing';

export interface SystemState {
  status: SystemStatus;
  model: string;
  knowledgeBase: string;
  gpu: string;
}

// 审核状态
export type AuditStatus = 'idle' | 'ready' | 'auditing' | 'completed' | 'error';

export interface AppState {
  auditStatus: AuditStatus;
  presentationDate: string | null;
  uploads: Record<DocumentType, DocumentUpload>;
  auditSteps: AuditStep[];
  result: AuditResult | null;
  error: string | null;
}
