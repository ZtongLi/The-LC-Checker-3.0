import { useState, useCallback, useMemo, useRef } from 'react';
import type {
  DocumentType,
  DocumentUpload,
  FileUpload,
  AuditStep,
  AuditResult,
  AuditStatus,
  Severity,
} from '@/types';

// 初始上传状态
const initialUploads: Record<DocumentType, DocumentUpload> = {
  lc: {
    type: 'lc',
    label: '信用证',
    labelEn: 'Letter of Credit',
    required: true,
    file: null,
  },
  invoice: {
    type: 'invoice',
    label: '商业发票',
    labelEn: 'Commercial Invoice',
    required: true,
    file: null,
  },
  bl: {
    type: 'bl',
    label: '提单',
    labelEn: 'Bill of Lading',
    required: true,
    file: null,
  },
  insurance: {
    type: 'insurance',
    label: '保险单',
    labelEn: 'Insurance Policy',
    required: true,
    file: null,
  },
};

// 审核步骤
const initialAuditSteps: AuditStep[] = [
  { id: 1, name: '解析信用证', status: 'pending' },
  { id: 2, name: '解析商业发票', status: 'pending' },
  { id: 3, name: '解析提单', status: 'pending' },
  { id: 4, name: '解析保险单', status: 'pending' },
  { id: 5, name: '规则引擎审核', status: 'pending' },
  { id: 6, name: 'AI 全面审核', status: 'pending' },
  { id: 7, name: '生成审核报告', status: 'pending' },
];

// 后端 API 地址
const API_BASE = '/api';

// 映射后端严重程度到前端类型
function mapSeverity(severity: string): Severity {
  if (severity.includes('严重')) return 'severe';
  if (severity.includes('一般')) return 'normal';
  return 'minor';
}

// 将后端返回的字段对象转换为前端 { key, value } 数组
function objectToFields(obj: Record<string, unknown>): { key: string; value: string }[] {
  const keyLabels: Record<string, string> = {
    lc_number: '信用证号',
    issuing_bank: '开证行',
    advising_bank: '通知行',
    currency: '币种',
    amount: '金额',
    amount_tolerance: '金额容差',
    goods_description: '货物描述',
    latest_shipment_date: '最迟装运日',
    expiry_date: '有效期',
    expiry_place: '到期地点',
    presentation_period: '交单期限',
    loading_port: '装货港',
    discharge_port: '卸货港',
    trade_terms: '贸易术语',
    partial_shipment: '分批装运',
    transhipment: '转运',
    invoice_number: '发票号',
    invoice_date: '发票日期',
    issued_by: '出票人',
    issued_to: '抬头',
    total_amount: '总金额',
    bl_number: '提单号',
    shipper: '托运人',
    consignee: '收货人',
    notify_party: '通知方',
    vessel: '船名',
    voyage: '航次',
    port_of_loading: '装货港',
    port_of_discharge: '卸货港',
    onboard_date: '装船日期',
    issue_date: '签发日期',
    number_of_packages: '件数',
    gross_weight: '毛重',
    freight: '运费',
    number_of_originals: '正本份数',
    clean_onboard: '清洁已装船',
    policy_number: '保单号',
    insured: '被保险人',
    insurance_amount: '保险金额',
    coverage: '险别',
    from: '起运地',
    to: '目的地',
    claims_payable_at: '赔付地',
  };

  return Object.entries(obj)
    .filter(([key]) => !['raw_text', 'goods', 'applicant', 'beneficiary', 'required_documents', 'additional_conditions'].includes(key))
    .map(([key, value]) => ({
      key: keyLabels[key] || key,
      value: value === null || value === undefined ? 'N/A' :
             typeof value === 'object' ? JSON.stringify(value) :
             typeof value === 'number' ? value.toLocaleString() :
             String(value),
    }));
}

export function useAuditState() {
  const [uploads, setUploads] = useState<Record<DocumentType, DocumentUpload>>(initialUploads);
  const [presentationDate, setPresentationDate] = useState<string>('');
  const [auditStatus, setAuditStatus] = useState<AuditStatus>('idle');
  const [auditSteps, setAuditSteps] = useState<AuditStep[]>(initialAuditSteps);
  const [result, setResult] = useState<AuditResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // 保存原始 File 对象，用于后续上传到后端
  const rawFiles = useRef<Record<DocumentType, File | null>>({
    lc: null,
    invoice: null,
    bl: null,
    insurance: null,
  });

  // 检查是否可以开始审核
  const canStartAudit = useMemo(() => {
    const allFilesUploaded = Object.values(uploads).every(
      (doc) => doc.file?.status === 'success'
    );
    const hasPresentationDate = presentationDate.trim() !== '';
    return allFilesUploaded && hasPresentationDate;
  }, [uploads, presentationDate]);

  // 上传文件（保存 File 对象 + 更新 UI 状态）
  const uploadFile = useCallback((type: DocumentType, file: File) => {
    // 保存原始 File 对象
    rawFiles.current[type] = file;

    const fileUpload: FileUpload = {
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      status: 'uploading',
      progress: 0,
    };

    setUploads((prev) => ({
      ...prev,
      [type]: { ...prev[type], file: fileUpload },
    }));

    // 模拟上传进度动画（文件实际在 startAudit 时才发给后端）
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 30;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
        setUploads((prev) => ({
          ...prev,
          [type]: {
            ...prev[type],
            file: { ...fileUpload, status: 'success', progress: 100 },
          },
        }));
      } else {
        setUploads((prev) => ({
          ...prev,
          [type]: {
            ...prev[type],
            file: { ...fileUpload, progress },
          },
        }));
      }
    }, 200);
  }, []);

  // 移除���件
  const removeFile = useCallback((type: DocumentType) => {
    rawFiles.current[type] = null;
    setUploads((prev) => ({
      ...prev,
      [type]: { ...prev[type], file: null },
    }));
    setResult(null);
    setAuditStatus('idle');
  }, []);

  // 设置交单日期
  const setDate = useCallback((date: string) => {
    setPresentationDate(date);
  }, []);

  // 更新某个步骤的状态
  const updateStep = (stepIndex: number, status: AuditStep['status']) => {
    setAuditSteps((prev) =>
      prev.map((step, idx) =>
        idx === stepIndex ? { ...step, status } : step
      )
    );
  };

  // 开始审核 — 调用真实后端 API
  const startAudit = useCallback(async () => {
    if (!canStartAudit) return;

    const lcFile = rawFiles.current.lc;
    const invoiceFile = rawFiles.current.invoice;
    const blFile = rawFiles.current.bl;
    const insuranceFile = rawFiles.current.insurance;

    if (!lcFile || !invoiceFile || !blFile || !insuranceFile) {
      setError('文件缺失，请重新上传');
      return;
    }

    setAuditStatus('auditing');
    setError(null);
    setResult(null);
    setAuditSteps(initialAuditSteps.map((step) => ({ ...step, status: 'pending' })));

    // 模拟前 4 步进度（因为后端是一次性返回，无法实时推送进度）
    for (let i = 0; i < 4; i++) {
      updateStep(i, 'processing');
      await new Promise((resolve) => setTimeout(resolve, 500));
      updateStep(i, 'completed');
    }

    // 第 5-6 步：调用后端 API
    updateStep(4, 'processing');
    updateStep(5, 'processing');

    try {
      const formData = new FormData();
      formData.append('lc_file', lcFile);
      formData.append('invoice_file', invoiceFile);
      formData.append('bl_file', blFile);
      formData.append('insurance_file', insuranceFile);
      formData.append('presentation_date', presentationDate || new Date().toISOString().split('T')[0]);

      const response = await fetch(`${API_BASE}/review`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || `服务器错误 (${response.status})`);
      }

      const data = await response.json();

      updateStep(4, 'completed');
      updateStep(5, 'completed');

      // 第 7 步：生成报告
      updateStep(6, 'processing');
      await new Promise((resolve) => setTimeout(resolve, 300));
      updateStep(6, 'completed');

      // 映射后端数据到前端类型
      const discrepancies = (data.discrepancies || []).map(
        (d: Record<string, string>, index: number) => ({
          id: index + 1,
          severity: mapSeverity(d.severity || '一般'),
          document: d.document || '',
          field: d.field || '',
          lcRequirement: d.lc_requirement || '',
          documentValue: d.doc_shows || '',
          description: d.description || '',
          ucpArticle: d.ucp_reference || '',
        })
      );

      const complianceItems = (data.compliant_items || []).map(
        (item: string, index: number) => {
          const parts = item.split(' — ');
          return {
            id: index + 1,
            document: parts[0] || '',
            description: parts[1] || item,
          };
        }
      );

      const extractedFields = data.extracted_fields || {};
      const documentFields = [
        {
          type: 'lc' as DocumentType,
          name: '信用证字段',
          nameEn: 'Letter of Credit',
          fields: objectToFields(extractedFields.letter_of_credit || {}),
        },
        {
          type: 'invoice' as DocumentType,
          name: '商业发票字段',
          nameEn: 'Commercial Invoice',
          fields: objectToFields(extractedFields.commercial_invoice || {}),
        },
        {
          type: 'bl' as DocumentType,
          name: '提单字段',
          nameEn: 'Bill of Lading',
          fields: objectToFields(extractedFields.bill_of_lading || {}),
        },
        {
          type: 'insurance' as DocumentType,
          name: '保险单字段',
          nameEn: 'Insurance Policy',
          fields: objectToFields(extractedFields.insurance_policy || {}),
        },
      ];

      const severeCount = discrepancies.filter(
        (d: { severity: string }) => d.severity === 'severe'
      ).length;
      const normalCount = discrepancies.filter(
        (d: { severity: string }) => d.severity === 'normal'
      ).length;
      const minorCount = discrepancies.filter(
        (d: { severity: string }) => d.severity === 'minor'
      ).length;

      const auditResult: AuditResult = {
        hasDiscrepancies: discrepancies.length > 0,
        severeCount,
        normalCount,
        minorCount,
        recommendation: data.summary?.conclusion || '',
        discrepancies,
        complianceItems,
        documentFields,
      };

      setResult(auditResult);
      setAuditStatus('completed');

    } catch (err) {
      const message = err instanceof Error ? err.message : '审核过程中出错';
      setError(message);
      setAuditStatus('error');

      // 标记失败的步骤
      setAuditSteps((prev) =>
        prev.map((step) =>
          step.status === 'processing' ? { ...step, status: 'pending' } : step
        )
      );
    }
  }, [canStartAudit, presentationDate]);

  // 重置审核
  const resetAudit = useCallback(() => {
    setAuditStatus('idle');
    setAuditSteps(initialAuditSteps);
    setResult(null);
    setError(null);
  }, []);

  return {
    uploads,
    presentationDate,
    auditStatus,
    auditSteps,
    result,
    error,
    canStartAudit,
    uploadFile,
    removeFile,
    setDate,
    startAudit,
    resetAudit,
  };
}