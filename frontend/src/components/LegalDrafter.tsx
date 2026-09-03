import React, { useState, useEffect } from 'react';
import {
  FileEdit,
  Download,
  Copy,
  Check,
  Printer,
  Sparkles,
  BookOpen,
} from 'lucide-react';
import api from '../api/client';

export const LegalDrafter: React.FC = () => {
  const [templates, setTemplates] = useState<any[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState('regular_bail');
  const [formData, setFormData] = useState<any>({
    court_name: 'IN THE COURT OF SESSIONS JUDGE, PATIALA HOUSE COURTS, NEW DELHI',
    applicant_name: 'Rajesh Sharma',
    applicant_details: 'S/o Sh. Ramesh Sharma, R/o B-42, Vasant Kunj, New Delhi',
    fir_no: '142/2026',
    police_station: 'Vasant Kunj South',
    sections: 'Section 303 / 318 of Bharatiya Nyaya Sanhita (BNS) 2023',
    custody_date: '15-01-2026',
    case_facts: 'The applicant was falsely implicated on allegations of property dispute. No recovery has been effected from applicant and investigation is substantially concluded.',
  });
  const [loading, setLoading] = useState(false);
  const [generatedDraft, setGeneratedDraft] = useState<string>('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const res = await api.get('/drafts/templates');
        setTemplates(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchTemplates();
  }, []);

  const handleTemplateChange = (tmplId: string) => {
    setSelectedTemplate(tmplId);
    if (tmplId === 'regular_bail') {
      setFormData({
        court_name: 'IN THE COURT OF SESSIONS JUDGE, PATIALA HOUSE COURTS, NEW DELHI',
        applicant_name: 'Rajesh Sharma',
        applicant_details: 'S/o Sh. Ramesh Sharma, R/o B-42, Vasant Kunj, New Delhi',
        fir_no: '142/2026',
        police_station: 'Vasant Kunj South',
        sections: 'Section 303 / 318 of Bharatiya Nyaya Sanhita (BNS) 2023',
        custody_date: '15-01-2026',
        case_facts: 'The applicant was falsely implicated on allegations of property dispute. No recovery has been effected from applicant and investigation is substantially concluded.',
      });
    } else if (tmplId === 'anticipatory_bail') {
      setFormData({
        court_name: 'IN THE HIGH COURT OF JUDICATURE AT DELHI',
        applicant_name: 'Vikram Malhotra',
        fir_no: 'Anticipated Complaint at PS Connaught Place',
        sections: 'Section 318 BNS 2023 (Cheating)',
        grounds: 'The dispute is entirely of a commercial nature arising out of non-fulfillment of supply contract due to market conditions.',
      });
    } else if (tmplId === 'legal_notice') {
      setFormData({
        sender_name: 'Apex Infotech Solutions Pvt. Ltd.',
        recipient_name: 'Blue Star Logistics Ltd.',
        due_amount: '₹14,20,000/- (Rupees Fourteen Lakh Twenty Thousand Only)',
        invoice_date: '10-10-2025',
        notice_days: '15',
      });
    } else if (tmplId === 'rti_application') {
      setFormData({
        pio_address: 'Central Public Information Officer, Department of Legal Affairs, New Delhi',
        applicant_name: 'Sunita Verma',
        applicant_address: '402, Lotus Towers, Andheri East, Mumbai - 400069',
        info_requested: '1. Certified status of e-filing portal integration across district courts.\n2. Date of release of operational guidelines.',
      });
    } else if (tmplId === 'consumer_complaint') {
      setFormData({
        commission: 'BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION AT SOUTH DELHI',
        complainant_name: 'Anil Kumar, R/o Saket, New Delhi',
        opposite_party: 'FastTrack Motors Pvt. Ltd.',
        complaint_facts: 'Vehicle manufactured with defective steering assembly delivered on 12-08-2025; breakdown occurred twice within first month; dealership refused replacement.',
        claim_amount: '₹12,50,000/- full refund plus ₹1,00,000/- compensation for harassment',
      });
    }
  };

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await api.post('/drafts/generate', {
        template_type: selectedTemplate,
        form_data: formData,
      });
      setGeneratedDraft(res.data.generated_content);
    } catch (err: any) {
      console.error(err);
      alert('Draft generation failed. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(generatedDraft);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([generatedDraft], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `${selectedTemplate}_draft.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>Court Legal Draft</title>
            <style>
              body { font-family: 'Times New Roman', serif; padding: 40px; font-size: 13pt; line-height: 1.6; }
              pre { white-space: pre-wrap; font-family: inherit; }
            </style>
          </head>
          <body>
            <pre>${generatedDraft}</pre>
          </body>
        </html>
      `);
      printWindow.document.close();
      printWindow.print();
    }
  };

  return (
    <div className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <FileEdit className="w-5 h-5 text-amber-400" />
          Structured Legal Document Drafter
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Generates court-compliant petitions, statutory notices, RTIs, and complaints adhering to Bharatiya Nagarik Suraksha Sanhita (BNSS) and Indian procedural law.
        </p>
      </div>

      <div className="grid lg:grid-cols-12 gap-6">
        {/* Form Panel (5 cols) */}
        <div className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-lg">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Select Legal Template:
            </label>
            <select
              value={selectedTemplate}
              onChange={(e) => handleTemplateChange(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 text-slate-100 rounded-xl p-2.5 text-xs focus:outline-none focus:border-amber-400 font-medium"
            >
              {templates.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name} ({t.statute})
                </option>
              ))}
            </select>
          </div>

          {/* Dynamic Form Inputs */}
          <div className="space-y-3 pt-2 border-t border-slate-800/80 text-xs">
            {Object.keys(formData).map((key) => {
              const label = key
                .replace(/_/g, ' ')
                .replace(/\b\w/g, (l) => l.toUpperCase());

              const isTextArea = key.includes('facts') || key.includes('grounds') || key.includes('info') || key.includes('statements');

              return (
                <div key={key}>
                  <label className="block text-slate-400 mb-1 font-medium">{label}:</label>
                  {isTextArea ? (
                    <textarea
                      rows={3}
                      value={formData[key]}
                      onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-amber-400"
                    />
                  ) : (
                    <input
                      type="text"
                      value={formData[key]}
                      onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-amber-400"
                    />
                  )}
                </div>
              );
            })}
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 text-slate-950 font-bold text-xs rounded-xl flex items-center justify-center gap-2 transition-all shadow-md shadow-yellow-500/20"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? 'Drafting...' : 'Generate Court Draft'}</span>
          </button>
        </div>

        {/* Output Document Preview Panel (7 cols) */}
        <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col shadow-lg">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-amber-400" />
              Court Ready Document Preview
            </span>

            {generatedDraft && (
              <div className="flex items-center gap-2">
                <button
                  onClick={handleCopy}
                  className="flex items-center gap-1 px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs transition-colors"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
                  <span>{copied ? 'Copied' : 'Copy'}</span>
                </button>
                <button
                  onClick={handleDownload}
                  className="flex items-center gap-1 px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs transition-colors"
                >
                  <Download className="w-3.5 h-3.5 text-slate-400" />
                  <span>Download</span>
                </button>
                <button
                  onClick={handlePrint}
                  className="flex items-center gap-1 px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs transition-colors"
                >
                  <Printer className="w-3.5 h-3.5 text-slate-400" />
                  <span>Print</span>
                </button>
              </div>
            )}
          </div>

          <div className="flex-1 bg-slate-950 border border-slate-800/80 rounded-xl p-5 overflow-y-auto max-h-[600px]">
            {generatedDraft ? (
              <pre className="font-mono text-xs text-slate-200 leading-relaxed whitespace-pre-wrap selection:bg-amber-500/30">
                {generatedDraft}
              </pre>
            ) : (
              <div className="h-full min-h-[300px] flex flex-col items-center justify-center text-center text-slate-500 space-y-2">
                <FileEdit className="w-8 h-8 text-slate-600" />
                <p className="text-xs">Fill the case particulars and click "Generate Court Draft".</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
