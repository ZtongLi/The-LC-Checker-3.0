import { Download } from 'lucide-react';
import { Button } from '@/components/ui/button';

export function DownloadButtons() {
  const handleDownloadReport = () => {
    // 模拟下载报告
    const content = `信用证审单报告
================

审核时间: ${new Date().toLocaleString()}
审核结果: 发现 6 处不符点

不符点详情:
1. [严重] 提单 - 装船日期晚于信用证要求
2. [严重] 商业发票 - 金额超出信用证金额
3. [严重] 保险单 - 保险金额不足
4. [一般] 提单 - 收货人栏位不符
5. [一般] 商业发票 - 货物描述拼写差异
6. [轻微] 保险单 - 未按要求背书

审核建议: 单据存在严重不符点，建议拒绝承付或联系申请人修改单据。

本报告由 AI 智能审单系统生成，仅供辅助参考。
`;
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `审单报告_${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadJSON = () => {
    // 模拟下载JSON数据
    const data = {
      auditTime: new Date().toISOString(),
      result: {
        hasDiscrepancies: true,
        severeCount: 3,
        normalCount: 2,
        minorCount: 1,
      },
      note: '本数据由 AI 智能审单系统生成',
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `字段数据_${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex gap-4">
      <Button
        variant="outline"
        onClick={handleDownloadReport}
        className="flex-1 h-10 border-finance-primary text-finance-primary hover:bg-finance-primary hover:text-white transition-colors"
      >
        <Download className="w-4 h-4 mr-2" />
        下载完整报告 (TXT)
      </Button>
      <Button
        variant="outline"
        onClick={handleDownloadJSON}
        className="flex-1 h-10 border-finance-primary text-finance-primary hover:bg-finance-primary hover:text-white transition-colors"
      >
        <Download className="w-4 h-4 mr-2" />
        下载字段数据 (JSON)
      </Button>
    </div>
  );
}
