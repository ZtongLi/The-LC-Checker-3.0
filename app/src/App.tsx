import { Header } from '@/sections/Header';
import { StatusBar } from '@/sections/StatusBar';
import { FileUploadSection } from '@/sections/FileUploadSection';
import { AuditControls } from '@/sections/AuditControls';
import { AuditProgress } from '@/sections/AuditProgress';
import { EmptyState } from '@/sections/EmptyState';
import { AuditingState } from '@/sections/AuditingState';
import { ResultSummary } from '@/sections/ResultSummary';
import { DiscrepancyList } from '@/sections/DiscrepancyList';
import { ComplianceList } from '@/sections/ComplianceList';
import { DocumentFieldsSection } from '@/sections/DocumentFields';
import { DownloadButtons } from '@/sections/DownloadButtons';
import { Footer } from '@/sections/Footer';
import { useAuditState } from '@/hooks/useAuditState';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';

function App() {
  const {
    uploads,
    presentationDate,
    auditStatus,
    auditSteps,
    result,
    canStartAudit,
    uploadFile,
    removeFile,
    setDate,
    startAudit,
  } = useAuditState();

  const handleStartAudit = async () => {
    if (!canStartAudit) {
      toast.error('请先上传所有必需文件并填写交单日期');
      return;
    }
    await startAudit();
  };

  const renderRightPanel = () => {
    switch (auditStatus) {
      case 'idle':
      case 'ready':
        return <EmptyState />;
      case 'auditing':
        return <AuditingState />;
      case 'completed':
        if (!result) return <EmptyState />;
        return (
          <div className="space-y-6">
            <ResultSummary result={result} />
            <DiscrepancyList discrepancies={result.discrepancies} />
            <ComplianceList items={result.complianceItems} />
            <DocumentFieldsSection documents={result.documentFields} />
            <DownloadButtons />
          </div>
        );
      default:
        return <EmptyState />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-finance-bg">
      <Toaster position="top-center" />
      
      {/* Header */}
      <Header />
      
      {/* Status Bar */}
      <StatusBar status="ready" />

      {/* Main Content */}
      <main className="flex-1 py-6 px-4 sm:px-6">
        <div className="max-w-page mx-auto">
          <div className="flex flex-col lg:flex-row gap-6">
            {/* Left Panel - Upload Area */}
            <div className="w-full lg:w-[400px] flex-shrink-0 space-y-4">
              <FileUploadSection
                uploads={uploads}
                onUpload={uploadFile}
                onRemove={removeFile}
              />
              
              <div className="finance-card">
                <AuditControls
                  presentationDate={presentationDate}
                  onDateChange={setDate}
                  auditStatus={auditStatus}
                  canStartAudit={canStartAudit}
                  onStartAudit={handleStartAudit}
                />
                
                {auditStatus === 'auditing' && (
                  <AuditProgress steps={auditSteps} />
                )}
              </div>
            </div>

            {/* Right Panel - Results */}
            <div className="flex-1 min-w-0">
              {renderRightPanel()}
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;
