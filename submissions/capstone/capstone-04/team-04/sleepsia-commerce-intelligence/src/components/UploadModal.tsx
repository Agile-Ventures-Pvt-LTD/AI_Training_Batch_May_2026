import React, { useState, useRef } from 'react';
import {
  FileSpreadsheet,
  Upload,
  X,
  CheckCircle2,
  AlertTriangle,
  FileCheck,
  Loader2,
} from 'lucide-react';
import { parseSleepsiaWorkbook, setActiveDataset } from '../services/datasetService';
import { SleepsiaWorkbookData } from '../types/commerce';

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess: (metadata: any, parsedData?: SleepsiaWorkbookData) => void;
}

export const UploadModal: React.FC<UploadModalProps> = ({
  isOpen,
  onClose,
  onUploadSuccess,
}) => {
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [warnings, setWarnings] = useState<string[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleFile = (file: File) => {
    if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
      setErrorMessage('Please upload a valid Excel workbook (.xlsx or .xls)');
      return;
    }
    setSelectedFile(file);
    setErrorMessage(null);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleUploadSubmit = async () => {
    if (!selectedFile) return;
    setIsUploading(true);
    setErrorMessage(null);
    setWarnings([]);

    try {
      // 1. Read array buffer for immediate local browser parsing
      const arrayBuffer = await selectedFile.arrayBuffer();
      const localResult = parseSleepsiaWorkbook(arrayBuffer, selectedFile.name);

      if (!localResult.success || !localResult.data) {
        setErrorMessage(localResult.errors?.join('\n') || 'Failed to parse workbook spreadsheet.');
        setIsUploading(false);
        return;
      }

      // Update in-memory active dataset on client
      setActiveDataset(localResult.data);

      // 2. Also send base64 to server API to keep backend in sync
      const reader = new FileReader();
      reader.onload = async (e) => {
        try {
          const base64 = (e.target?.result as string).split(',')[1];
          const res = await fetch('/api/dataset/upload', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              fileBase64: base64,
              fileName: selectedFile.name,
            }),
          });

          const json = await res.json();
          if (json.warnings && json.warnings.length > 0) {
            setWarnings(json.warnings);
          }
        } catch (serverErr) {
          console.warn('Backend sync warning (local parsed data active):', serverErr);
        }

        onUploadSuccess(localResult.data!.metadata, localResult.data!);
        if (localResult.warnings && localResult.warnings.length > 0) {
          setWarnings(localResult.warnings);
        } else {
          onClose();
        }
        setIsUploading(false);
      };
      reader.readAsDataURL(selectedFile);
    } catch (err: any) {
      setErrorMessage(err?.message || 'Error processing spreadsheet file');
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white border border-slate-200 rounded-2xl p-6 max-w-lg w-full shadow-2xl space-y-5">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-blue-50 text-blue-600 border border-blue-100">
              <FileSpreadsheet className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">Upload Sleepsia Excel Dataset</h3>
              <p className="text-[11px] text-slate-500">Unified 11-sheet workbook ingestion &amp; validation</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Drag & Drop Area */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
            dragOver
              ? 'border-blue-500 bg-blue-50/50'
              : selectedFile
              ? 'border-blue-500 bg-blue-50/30'
              : 'border-slate-300 hover:border-slate-400 bg-slate-50/50'
          }`}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
            accept=".xlsx, .xls"
            className="hidden"
          />

          {selectedFile ? (
            <div className="space-y-2">
              <FileCheck className="w-10 h-10 text-emerald-600 mx-auto" />
              <div className="text-xs font-bold text-slate-900">{selectedFile.name}</div>
              <div className="text-[10px] text-slate-500">{(selectedFile.size / 1024).toFixed(1)} KB • Click or drop to replace</div>
            </div>
          ) : (
            <div className="space-y-2">
              <Upload className="w-10 h-10 text-slate-400 mx-auto" />
              <div className="text-xs font-bold text-slate-800">
                Drag and drop your Sleepsia Excel file here
              </div>
              <div className="text-[11px] text-slate-500">or click to browse your files (.xlsx)</div>
            </div>
          )}
        </div>

        {/* Schema Information Box */}
        <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 text-[11px] text-slate-600 space-y-1.5">
          <div className="font-bold text-slate-800">Expected Sheets in Unified Schema:</div>
          <div className="grid grid-cols-2 gap-1 text-[10px] text-slate-500 font-mono font-medium">
            <span>• Data_Dictionary</span>
            <span>• Product_Master</span>
            <span>• Marketplace_Master</span>
            <span>• Internal_Sales</span>
            <span>• Marketplace_Data</span>
            <span>• Advertising_Data</span>
            <span>• Inventory_Data</span>
            <span>• Shipping_Data</span>
            <span>• Cost_Data</span>
            <span>• Competitor_Data</span>
            <span>• Customer_Data</span>
          </div>
        </div>

        {errorMessage && (
          <div className="bg-rose-50 border border-rose-200 text-rose-700 p-3 rounded-xl text-xs flex items-start gap-2 whitespace-pre-wrap">
            <AlertTriangle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
            <span>{errorMessage}</span>
          </div>
        )}

        {warnings.length > 0 && (
          <div className="bg-amber-50 border border-amber-200 text-amber-800 p-3 rounded-xl text-xs space-y-1">
            <div className="font-bold flex items-center gap-1.5 text-amber-900">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
              <span>Parsed with Schema Warnings:</span>
            </div>
            {warnings.map((w, i) => (
              <div key={i} className="text-[11px] text-amber-700 font-medium">• {w}</div>
            ))}
          </div>
        )}

        <div className="flex justify-end gap-2 text-xs pt-2">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-lg text-slate-600 hover:text-slate-900 border border-slate-200"
          >
            Cancel
          </button>
          <button
            onClick={handleUploadSubmit}
            disabled={!selectedFile || isUploading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-5 py-2 rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2 shadow-xs"
          >
            {isUploading ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                <span>Validating &amp; Ingesting...</span>
              </>
            ) : (
              <span>Load &amp; Process Workbook</span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
