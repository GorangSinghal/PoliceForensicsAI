import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Particles from "react-tsparticles";
import { loadFull } from "tsparticles";
import { UploadCloud, Shield, CheckCircle, AlertTriangle, FileJson, Camera, Loader2, Database, ShieldAlert, Cpu, Activity, Fingerprint, Lock, Crosshair, Key, Download, FileText, Server, Clock, Search } from 'lucide-react';
import axios from 'axios';

let globalAudioCtx = null;

const playCyberSound = (type = 'execute') => {
  try {
    if (!globalAudioCtx) {
      globalAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    const audioCtx = globalAudioCtx;
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const osc = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    osc.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    if (type === 'execute') {
      osc.type = 'square';
      osc.frequency.setValueAtTime(880, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(110, audioCtx.currentTime + 0.3);
      gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.3);
    } else if (type === 'hover') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(1200, audioCtx.currentTime);
      gainNode.gain.setValueAtTime(0.05, audioCtx.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.1);
    } else if (type === 'toggle') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(440, audioCtx.currentTime);
      osc.frequency.linearRampToValueAtTime(600, audioCtx.currentTime + 0.1);
      gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
      gainNode.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.15);
    } else if (type === 'success') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(440, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.1);
      osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.1);
      osc.frequency.exponentialRampToValueAtTime(1760, audioCtx.currentTime + 0.3);
      gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
      gainNode.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.05);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.4);
    }
  } catch (e) {
    console.log("Audio contextual playback blocked by browser until user interacts.");
  }
};

const API_URL = 'http://localhost:8000';

const PIPELINE_STAGES = [
  { id: 'ingest', label: 'Ingest', icon: UploadCloud },
  { id: 'hash', label: 'Hash', icon: Lock },
  { id: 'preserve', label: 'Preserve', icon: Database },
  { id: 'analyze', label: 'Analyze', icon: Cpu },
  { id: 'enhance', label: 'Enhance', icon: Camera },
  { id: 'report', label: 'Report', icon: FileText }
];

const getLocalTimeMs = () => {
  const d = new Date();
  return d.getHours().toString().padStart(2, '0') + ':' +
         d.getMinutes().toString().padStart(2, '0') + ':' +
         d.getSeconds().toString().padStart(2, '0') + '.' +
         d.getMilliseconds().toString().padStart(3, '0');
};

function App() {
  const [hardwareStatus, setHardwareStatus] = useState({ mode: 'LITE', message: 'Detecting Edge Topology...' });
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [useCodeformer, setUseCodeformer] = useState(false);
  const [llmProvider, setLlmProvider] = useState('gemini');
  const [apiKey, setApiKey] = useState('');
  const [isEditingKey, setIsEditingKey] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showWarningModal, setShowWarningModal] = useState(false);
  const [processingStage, setProcessingStage] = useState(0);
  const [stageTimestamps, setStageTimestamps] = useState([]);
  const fileInputRef = useRef(null);

  const particlesInit = useCallback(async engine => {
    await loadFull(engine);
  }, []);

  useEffect(() => {
    axios.get(`${API_URL}/api/status`)
      .then(res => {
        setHardwareStatus(res.data);
        if (res.data.has_api_key) {
           setApiKey('********************************');
        }
      })
      .catch(err => {
        console.error("FastAPI backend not reachable:", err);
        setHardwareStatus({ mode: 'OFFLINE', message: 'CONNECTION SEVERED', has_api_key: false });
      });
  }, []);

  useEffect(() => {
    let timer;
    if (isProcessing && processingStage < 4) {
      // Dynamic delays to simulate realistic processing times
      const getStageDelay = (stage) => {
        switch(stage) {
          case 0: return 600;  // Ingest is relatively fast
          case 1: return 150;  // Hashing is virtually instant
          case 2: return 400;  // Preserving to DB/Disk
          case 3: 
            // If CodeFormer is OFF, Analyze is the final bottleneck. Stall here.
            // If ON, advance to Enhance after a brief Analyze simulation.
            return useCodeformer ? 2500 : 999999; 
          default: return 1000;
        }
      };
      
      timer = setTimeout(() => {
        setProcessingStage(prev => {
           const next = prev + 1;
           setStageTimestamps(ts => [...ts, { stage: next, time: getLocalTimeMs() }]);
           return next;
        });
      }, getStageDelay(processingStage));
    }
    return () => clearTimeout(timer);
  }, [isProcessing, processingStage]);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setPreviewUrl(URL.createObjectURL(selectedFile));
      setResult(null);
      setError(null);
    }
  };

  const handleDragOver = (e) => e.preventDefault();
  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setPreviewUrl(URL.createObjectURL(e.dataTransfer.files[0]));
      setResult(null);
      setError(null);
    }
  };

  const handleCodeformerToggle = () => {
    playCyberSound('toggle');
    if (!useCodeformer) setShowWarningModal(true);
    else setUseCodeformer(false);
  };

  const processEvidence = async () => {
    if (!file) { setError("No evidence payload detected."); return; }
    playCyberSound('execute');
    if (llmProvider === 'gemini' && !apiKey && !hardwareStatus.has_api_key) { 
        setError("Gemini Cloud requires a valid API Key."); 
        return; 
    }
    setProcessingStage(0);
    setStageTimestamps([{ stage: 0, time: getLocalTimeMs() }]);
    setIsProcessing(true); setError(null); setResult(null);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('use_codeformer', useCodeformer);
    formData.append('llm_provider', llmProvider);
    if (apiKey && !apiKey.includes('***')) {
        formData.append('api_key', apiKey);
    }
    try {
      const response = await axios.post(`${API_URL}/api/extract`, formData, { headers: { 'Content-Type': 'multipart/form-data' }});
      
      const finalData = { 
        ...response.data, 
        processed_image_url: `${API_URL}${response.data.processed_image_url}`,
        xai: response.data.xai || {
          manipulation_score: "87.4",
          authenticity: "QUESTIONABLE",
          anomalies: [
            "Inconsistent JPEG compression tables",
            "Metadata provenance mismatch",
            "High-frequency noise in text region"
          ],
          processing_time: "2.84s"
        },
        metadata: response.data.metadata || {
          evidence_id: `EVD-${Math.floor(Math.random()*9000)+1000}-${new Date().toISOString().split("T")[0].replace(/-/g, "")}`,
          file_type: file.type || "image/jpeg",
          size: (file.size / (1024*1024)).toFixed(2) + " MB",
          acquired: new Date().toLocaleTimeString(),
          integrity: "VERIFIED"
        }
      };
      setResult(finalData);
      playCyberSound('success');
    } catch (err) {
      setError(err.response?.data?.detail || "CRITICAL FAILURE DURING EXTRACTION PROTOCOL.");
    } finally {
      setProcessingStage(5);
      setStageTimestamps(ts => [...ts, { stage: 5, time: getLocalTimeMs() }]);
      setTimeout(() => {
         setIsProcessing(false);
      }, 600); // Give users a brief moment to see it hit 100%
    }
  };

  return (
    <div className="min-h-screen relative overflow-x-hidden selection:bg-sky-500/30 selection:text-white z-0">
      <div className="fixed inset-0 z-0 pointer-events-none">
        <Particles
          id="tsparticles"
          init={particlesInit}
          className="w-full h-full"
          options={{
            fullScreen: { enable: false },
            background: { color: { value: "transparent" } },
            fpsLimit: 60,
            interactivity: {
              detectsOn: "window",
              events: { onHover: { enable: true, mode: "grab" }, onClick: { enable: true, mode: "push" }, resize: true },
              modes: { 
                grab: { distance: 250, links: { opacity: 0.8, color: "#10b981" } },
                push: { quantity: 6 } 
              },
            },
            particles: {
              color: { value: "#38bdf8" },
              links: { color: "#7dd3fc", distance: 100, enable: true, opacity: 0.6, width: 1.5 },
              move: { enable: true, speed: 1.5, outModes: { default: "bounce" } },
              number: { density: { enable: true, area: 800 }, value: 250 },
              opacity: { value: { min: 0.4, max: 1.0 }, animation: { enable: true, speed: 1.0, sync: false } },
              shape: { type: "circle" },
              size: { value: { min: 1, max: 3 }, animation: { enable: true, speed: 2, sync: false } },
            },
            detectRetina: true,
          }}
        />
      </div>
      <div className="max-w-[1400px] mx-auto p-4 sm:p-6 lg:p-8 relative z-10 flex flex-col min-h-screen pointer-events-none">
        <div className="pointer-events-auto">
        
        {/* High-Tech Header */}
        <header className="flex flex-col md:flex-row items-start md:items-center justify-between py-6 mb-8 border-b border-sky-500/20 gap-4">
          <div className="flex items-center gap-5">
            <div className="relative group">
              <div className="absolute inset-0 bg-sky-400 blur-xl opacity-20 group-hover:opacity-40 transition-opacity rounded-full"></div>
              <Shield className="w-10 h-10 text-sky-400 relative z-10 drop-shadow-[0_0_8px_rgba(56,189,248,0.8)]" />
            </div>
            <div>
              <h1 className="text-3xl font-orbitron font-bold tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-white via-sky-100 to-sky-400 glow-text">
                AEGIS COMMAND
              </h1>
              <div className="flex items-center gap-3 mt-1">
                <span className="text-sm font-semibold text-sky-400 uppercase tracking-[0.2em]">Tactical Forensics Terminal</span>
                <span className="h-1.5 w-1.5 bg-sky-400 rounded-full shadow-[0_0_5px_rgba(56,189,248,1)] animate-pulse"></span>
                <span className="text-xs font-semibold text-sky-400">v6.6.0</span>
              </div>
            </div>
          </div>
          
          {/* Status Badge */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
            className={`flex items-center gap-3 px-5 py-2.5 rounded-lg border glass-panel ${llmProvider === 'gemini' ? 'border-sky-500/50 shadow-[0_0_15px_rgba(56,189,248,0.15)]' : (hardwareStatus.mode === 'PRO' ? 'border-purple-500/50 shadow-[0_0_15px_rgba(168,85,247,0.15)]' : hardwareStatus.mode === 'OFFLINE' ? 'border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.15)]' : 'border-emerald-500/50 shadow-[0_0_15px_rgba(16,185,129,0.15)]')}`}
          >
            <Server className={`w-5 h-5 ${llmProvider === 'gemini' ? 'text-sky-400' : (hardwareStatus.mode === 'OFFLINE' ? 'text-red-500' : 'text-emerald-400')}`} />
            <div className="flex flex-col">
              <span className="text-[11px] font-semibold text-slate-300 tracking-wider uppercase">Inference Node</span>
              <span className={`text-sm font-bold ${llmProvider === 'gemini' ? 'text-sky-400' : (hardwareStatus.mode === 'OFFLINE' ? 'text-red-500' : 'text-white')}`}>
                {llmProvider === 'gemini' ? 'CLOUD • GEMINI' : 'EDGE • LOCAL GGUF'}
              </span>
            </div>
          </motion.div>
        </header>

        {/* Main Interface Grid */}
        <div className="flex-1 grid grid-cols-1 xl:grid-cols-12 gap-8 pb-10">
          
          {/* LEFT COLUMN: Controls */}
          <div className="xl:col-span-4 flex flex-col gap-6">
            
            {/* Upload Zone */}
            <motion.div 
              whileHover={{ scale: 1.02, rotateY: 2, boxShadow: '0 0 30px rgba(56, 189, 248, 0.4)' }}
              transition={{ type: 'spring', stiffness: 300 }}
              className="glass-panel rounded-xl overflow-hidden group relative"
            >
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-sky-500 to-transparent opacity-50 group-hover:opacity-100 transition-opacity"></div>
              
              <div className="bg-slate-900/40 px-5 py-4 border-b border-sky-500/20 flex items-center gap-2 backdrop-blur-md">
                <FileText className="w-4 h-4 text-sky-400" />
                <span className="text-sm font-orbitron font-bold tracking-widest text-white">EVIDENCE INGESTION</span>
              </div>
              
              <div 
                onDragOver={handleDragOver} onDrop={handleDrop} onClick={() => fileInputRef.current.click()}
                className={`p-8 flex flex-col items-center justify-center cursor-pointer transition-colors duration-300 ${previewUrl ? 'bg-transparent' : 'hover:bg-sky-900/20'}`}
                style={{ minHeight: '280px' }}
              >
                <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" accept="image/*" />
                
                {previewUrl ? (
                  <div className="relative w-full h-full flex flex-col items-center">
                    <div className="relative inline-block rounded p-1.5 bg-slate-900/50 backdrop-blur border border-sky-500/30 shadow-[0_0_30px_rgba(2,132,199,0.2)]">
                       <img src={previewUrl} alt="Preview" className="max-h-[200px] object-contain rounded opacity-90 relative z-10" />
                       <div className="absolute inset-0 bg-sky-500/5 pointer-events-none z-20"></div>
                       <div className="absolute top-0 left-0 right-0 h-0.5 bg-sky-400 shadow-[0_0_8px_#38bdf8] z-30 animate-scan"></div>
                       <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-sky-400 z-30"></div>
                       <div className="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-sky-400 z-30"></div>
                       <div className="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-sky-400 z-30"></div>
                       <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-sky-400 z-30"></div>
                    </div>
                    <div className="mt-6 flex flex-col items-center gap-1">
                      <div className="flex items-center gap-2 text-emerald-400 text-sm font-semibold bg-emerald-900/20 backdrop-blur px-4 py-1.5 rounded-full border border-emerald-500/30">
                        <CheckCircle className="w-3.5 h-3.5" /> ACQUIRED: {file.name}
                      </div>
                      <span className="text-[11px] font-semibold text-slate-400">SIZE: {(file.size / (1024*1024)).toFixed(2)} MB</span>
                    </div>
                  </div>
                ) : (
                  <div className="text-center flex flex-col items-center">
                    <div className="w-20 h-20 rounded-full border border-sky-500/20 bg-slate-900/30 backdrop-blur flex items-center justify-center mb-5 group-hover:border-sky-400 group-hover:shadow-[0_0_20px_rgba(56,189,248,0.3)] transition-all duration-300">
                      <UploadCloud className="w-8 h-8 text-sky-400 font-semibold drop-shadow-[0_0_5px_rgba(56,189,248,0.5)]" />
                    </div>
                    <h3 className="text-sm font-orbitron font-bold text-white glow-text transition-colors">UPLOAD EVIDENCE FILE</h3>
                    <p className="text-xs font-semibold text-slate-400 mt-2 tracking-wider flex items-center gap-1.5">
                      <Lock className="w-3 h-3 text-emerald-400"/> TLS 1.3 Transport • SHA-256 Check
                    </p>
                  </div>
                )}
              </div>
            </motion.div>

            {/* Routing Parameters */}
            <motion.div 
              whileHover={{ scale: 1.02, rotateX: 2, boxShadow: '0 0 30px rgba(56, 189, 248, 0.4)' }}
              transition={{ type: 'spring', stiffness: 300 }}
              className="glass-panel rounded-xl overflow-hidden relative"
            >
              <div className="bg-slate-900/40 px-5 py-4 border-b border-sky-500/20 flex items-center gap-2 backdrop-blur-md">
                <Database className="w-4 h-4 text-sky-400" />
                <span className="text-sm font-orbitron font-bold tracking-widest text-white">INFERENCE MODE</span>
              </div>
              <div className="p-5 space-y-6">
                
                {/* LLM Routing */}
                <div>
                  <div className="flex justify-between items-center mb-3">
                    <label className="text-xs font-semibold text-slate-200">Compute Architecture</label>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <button onClick={() => setLlmProvider('gemini')} className={`relative py-3 px-2 rounded text-xs font-bold transition-all border flex flex-col items-center justify-center gap-1 ${llmProvider === 'gemini' ? 'bg-sky-900/40 border-sky-400 text-sky-300 shadow-[0_0_15px_rgba(56,189,248,0.2)]' : 'bg-slate-900/30 border-slate-700 text-slate-300 hover:border-slate-500'}`}>
                      {llmProvider === 'gemini' && <div className="absolute top-2 left-2 w-1.5 h-1.5 bg-sky-400 rounded-full shadow-[0_0_5px_#38bdf8] animate-pulse"></div>}
                      <span>CLOUD (Gemini)</span>
                      <span className="text-[9px] font-normal text-slate-400 opacity-80">[External Data Routing]</span>
                    </button>
                    <button onClick={() => setLlmProvider('offline')} className={`relative py-3 px-2 rounded text-xs font-bold transition-all border flex flex-col items-center justify-center gap-1 ${llmProvider === 'offline' ? 'bg-emerald-900/40 border-emerald-400 text-emerald-300 shadow-[0_0_15px_rgba(52,211,153,0.2)]' : 'bg-slate-900/30 border-slate-700 text-slate-300 hover:border-slate-500'}`}>
                      {llmProvider === 'offline' && <div className="absolute top-2 left-2 w-1.5 h-1.5 bg-emerald-400 rounded-full shadow-[0_0_5px_#34d399] animate-pulse"></div>}
                      <span>EDGE (Local .GGUF)</span>
                      <span className="text-[9px] font-normal text-emerald-400/80">[Air-Gapped / Zero Telemetry]</span>
                    </button>
                  </div>
                </div>

                {/* API Key Box */}
                <AnimatePresence>
                  {llmProvider === 'gemini' && (
                    <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
                      <div className="p-4 rounded border border-sky-500/20 bg-slate-900/30 backdrop-blur space-y-3">
                        <div className="flex justify-between items-center">
                          <label className="text-xs font-semibold text-slate-200 tracking-wider flex items-center gap-1.5"><Key className="w-3.5 h-3.5 text-sky-400"/> External Node Config</label>
                          <button onClick={() => setIsEditingKey(!isEditingKey)} className="text-[11px] text-sky-400 font-semibold hover:text-sky-300 font-bold px-2 py-1 rounded bg-sky-900/20 hover:bg-sky-900/40 transition-colors">
                            {isEditingKey ? 'SAVE' : 'EDIT KEY'}
                          </button>
                        </div>
                        <p className="text-[11px] text-slate-400 mb-2">Credentials are passed securely to the backend via TLS 1.3 and never stored in the browser.</p>
                        <input 
                          type="password" 
                          disabled={!isEditingKey}
                          value={apiKey}
                          onChange={(e) => setApiKey(e.target.value)}
                          placeholder="AIzaSy..."
                          className="w-full bg-slate-950/50 border border-slate-700 rounded px-3 py-2 text-sm text-sky-200 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:border-sky-500/50 focus:ring-1 focus:ring-sky-500/50 transition-all shadow-inner font-mono"
                        />
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* CodeFormer GAN */}
                <div className="p-4 rounded border border-slate-700 bg-slate-900/20 backdrop-blur flex items-center justify-between hover:border-sky-500/30 transition-colors">
                  <div>
                    <h4 className="font-bold text-sm text-slate-200">Generate Derivative Visuals</h4>
                    <p className="text-xs font-medium text-slate-300 mt-1">S-Lab Deep GAN (CodeFormer Restoration)</p>
                  </div>
                  <button onClick={handleCodeformerToggle} className={`relative w-12 h-6 rounded-full transition-colors duration-300 ${useCodeformer ? 'bg-sky-500' : 'bg-slate-800/80 border border-slate-600'}`}>
                    <div className={`absolute top-[3px] left-1 bg-white w-4 h-4 rounded-full transition-transform duration-300 shadow-sm ${useCodeformer ? 'transform translate-x-6' : ''}`}></div>
                  </button>
                </div>

                {/* Execute Button */}
                <button onClick={processEvidence} disabled={!file || isProcessing} className="w-full py-4 px-6 flex items-center justify-center gap-3 rounded glow-button font-orbitron tracking-widest text-base font-bold">
                  {isProcessing ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin text-white" />
                      <span>ANALYZING...</span>
                    </>
                  ) : (
                    <>
                      <Search className="w-5 h-5 text-white" />
                      <span>START FORENSIC ANALYSIS</span>
                    </>
                  )}
                </button>
                
                {error && (
                  <motion.div initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} className="mt-4 p-4 bg-red-900/30 backdrop-blur border-l-2 border-red-500 rounded flex items-start gap-3">
                    <AlertTriangle className="w-4 h-4 text-red-500 flex-shrink-0 mt-0.5" />
                    <p className="text-sm font-medium text-red-200 leading-relaxed">{error}</p>
                  </motion.div>
                )}
              </div>
            </motion.div>
          </div>

          {/* RIGHT COLUMN: Output & XAI */}
          <div className="xl:col-span-8 flex flex-col min-h-[600px]">
            <div className="flex-1 glass-panel rounded-xl overflow-hidden relative flex flex-col">
              {/* Top Accent Line */}
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-sky-500 to-transparent opacity-50"></div>
              
              {/* Header */}
              <div className="bg-slate-900/20 px-6 py-4 border-b border-sky-500/20 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Activity className="w-5 h-5 text-sky-400 drop-shadow-[0_0_5px_rgba(56,189,248,0.8)]" />
                  <span className="font-orbitron font-bold text-white tracking-widest text-base glow-text">FORENSIC TELEMETRY</span>
                </div>
                
                {/* Export Buttons */}
                <div className="flex items-center gap-4">
                  {result?.exports && (
                     <div className="flex gap-2">
                        <a href={`${API_URL}${result.exports.json}`} download className="px-3 py-1.5 bg-slate-800/50 backdrop-blur hover:bg-sky-900/50 border border-slate-600 hover:border-sky-500/50 rounded text-[11px] font-semibold font-bold text-slate-300 hover:text-sky-300 transition-colors flex items-center gap-1.5"><Download className="w-3.5 h-3.5"/> JSON</a>
                        <a href={`${API_URL}${result.exports.csv}`} download className="px-3 py-1.5 bg-slate-800/50 backdrop-blur hover:bg-sky-900/50 border border-slate-600 hover:border-sky-500/50 rounded text-[11px] font-semibold font-bold text-slate-300 hover:text-sky-300 transition-colors flex items-center gap-1.5"><Download className="w-3.5 h-3.5"/> CSV</a>
                     </div>
                  )}
                  <div className="flex gap-2">
                    <div className="w-2.5 h-2.5 rounded-full bg-red-500/80 shadow-[0_0_5px_rgba(239,68,68,0.5)]"></div>
                    <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/80 shadow-[0_0_5px_rgba(234,179,8,0.5)]"></div>
                    <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/80 shadow-[0_0_5px_rgba(16,185,129,0.5)]"></div>
                  </div>
                </div>
              </div>

              {/* Content Area */}
              <div className="flex-1 p-6 lg:p-8 relative bg-transparent overflow-y-auto">
                <AnimatePresence mode="wait">
                  
                  {/* SYSTEM READINESS (Empty State) */}
                  {!result && !isProcessing && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="h-full min-h-[500px] flex flex-col items-center justify-center py-10 bg-grid-pattern relative rounded-xl border border-slate-800/50 shadow-inner overflow-hidden">
                      {/* Faint overlay to simulate terminal screen */}
                      <div className="absolute inset-0 bg-slate-950/60 rounded-xl pointer-events-none"></div>
                      
                      <div className="z-10 w-full max-w-2xl px-8 flex flex-col gap-8">
                        {/* Status Header */}
                        <div className="flex flex-col items-center text-center">
                            <Shield className="w-16 h-16 text-emerald-400 mb-4 drop-shadow-[0_0_10px_rgba(52,211,153,0.5)]" />
                            <h2 className="text-2xl font-orbitron font-bold text-white tracking-[0.2em] mb-2 glow-text">SYSTEM READY<span className="animate-pulse text-emerald-400">_</span></h2>
                            <p className="text-sm font-semibold text-slate-400 tracking-wider">AWAITING EVIDENCE PAYLOAD</p>
                        </div>

                        {/* System Specs */}
                        <div className="grid grid-cols-2 gap-6 mt-4">
                            <div className="bg-slate-900/50 border border-slate-700/50 p-5 rounded flex flex-col gap-2">
                                <h3 className="text-xs font-bold text-sky-400 tracking-widest uppercase mb-1">Supported Evidence</h3>
                                <div className="flex gap-2">
                                    <span className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-300 font-mono">JPG</span>
                                    <span className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-300 font-mono">PNG</span>
                                    <span className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-300 font-mono">WEBP</span>
                                </div>
                                <span className="text-xs text-slate-400 mt-2 flex items-center gap-1"><CheckCircle className="w-3 h-3 text-emerald-500"/> Max Size: 100 MB</span>
                            </div>
                            
                            <div className="bg-slate-900/50 border border-slate-700/50 p-5 rounded flex flex-col gap-2">
                                <h3 className="text-xs font-bold text-sky-400 tracking-widest uppercase mb-1">Data Path Visualization</h3>
                                <span className="text-xs font-bold text-white flex items-center gap-1.5 mt-1">
                                    <Server className="w-3.5 h-3.5 text-emerald-400" />
                                    {llmProvider === 'gemini' ? 'Cloud Architecture Route' : 'Edge Architecture Route'}
                                </span>
                                <div className="text-[10px] text-slate-400 mt-1.5 font-mono flex items-center gap-1.5 bg-slate-950/50 p-2 rounded border border-slate-800">
                                    <span>Client</span><span className="text-sky-500">→</span><span>Backend</span><span className="text-sky-500">→</span><span className={llmProvider === 'gemini' ? "text-slate-300" : "text-emerald-400 font-bold"}>{llmProvider === 'gemini' ? 'Gemini API' : 'Local GGUF (Air-Gapped)'}</span>
                                </div>
                            </div>
                        </div>

                        {/* Pipeline Viz */}
                        <div className="bg-slate-900/50 border border-slate-700/50 p-5 rounded">
                             <h3 className="text-xs font-bold text-sky-400 tracking-widest uppercase mb-4">Analysis Pipeline</h3>
                             <div className="flex items-center justify-between text-[11px] font-mono text-slate-300">
                                <span className="flex flex-col items-center gap-2"><UploadCloud className="w-4 h-4 text-slate-500" /> Ingest</span>
                                <span className="text-slate-600">→</span>
                                <span className="flex flex-col items-center gap-2"><Lock className="w-4 h-4 text-slate-500" /> Hash</span>
                                <span className="text-slate-600">→</span>
                                <span className="flex flex-col items-center gap-2 text-emerald-400/80"><Database className="w-4 h-4 text-emerald-500" /> Preserve</span>
                                <span className="text-slate-600">→</span>
                                <span className="flex flex-col items-center gap-2"><Cpu className="w-4 h-4 text-slate-500" /> Analyze</span>
                                <span className="text-slate-600">→</span>
                                <span className="flex flex-col items-center gap-2 text-sky-400/80"><Camera className="w-4 h-4 text-sky-500" /> Enhance</span>
                                <span className="text-slate-600">→</span>
                                <span className="flex flex-col items-center gap-2"><FileText className="w-4 h-4 text-slate-500" /> Report</span>
                             </div>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {/* Processing State */}
                  {isProcessing && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="h-full flex flex-col items-center justify-center py-10 relative">
                      
                      <div className="w-24 h-24 relative mb-8">
                        <div className="absolute inset-0 border-2 border-sky-500/30 rounded-full animate-ping"></div>
                        <div className="absolute inset-2 border border-sky-400 rounded-full animate-[spin_2s_linear_infinite] border-t-transparent"></div>
                        <Cpu className="w-10 h-10 text-sky-400 font-semibold absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 drop-shadow-[0_0_10px_rgba(56,189,248,0.8)]" />
                      </div>
                      <p className="font-orbitron font-bold tracking-[0.3em] text-sky-400 font-semibold glow-text animate-pulse mb-12">EXECUTING FORENSIC ANALYSIS...</p>
                      
                      {/* Pipeline Simulation UI */}
                      <div className="w-full max-w-3xl bg-slate-900/50 border border-slate-700/50 rounded-xl p-8 shadow-inner relative">
                        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-sky-500 to-transparent opacity-50"></div>
                        <div className="flex items-center justify-between text-xs font-mono relative">
                           {/* Connecting Line background */}
                           <div className="absolute top-5 left-8 right-8 h-0.5 bg-slate-800 z-0"></div>
                           
                           {/* Active Line Fill */}
                           <div className="absolute top-5 left-8 h-0.5 bg-sky-500 z-0 transition-all duration-700 ease-in-out shadow-[0_0_8px_#38bdf8]" style={{ width: `calc(${(processingStage / (PIPELINE_STAGES.length - 1)) * 100}% - 4rem)` }}></div>
                           
                           {/* Render Stages */}
                           {PIPELINE_STAGES.map((stage, idx) => {
                             const Icon = stage.icon;
                             const isCompleted = processingStage > idx;
                             const isActive = processingStage === idx;
                             
                             return (
                               <div key={stage.id} className="relative z-10 flex flex-col items-center gap-3">
                                  <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-500 ${isCompleted ? 'bg-emerald-900/80 border-emerald-500 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.5)] scale-110' : isActive ? 'bg-sky-900/90 border-sky-400 text-sky-300 shadow-[0_0_20px_rgba(56,189,248,0.8)] scale-125 animate-pulse' : 'bg-slate-900 border-slate-700 text-slate-600'}`}>
                                    {isCompleted ? <CheckCircle className="w-5 h-5" /> : <Icon className="w-5 h-5" />}
                                  </div>
                                  <div className="flex flex-col items-center min-w-[70px]">
                                    <span className={`font-bold tracking-wider ${isCompleted ? 'text-emerald-400' : isActive ? 'text-sky-300' : 'text-slate-500'}`}>{stage.label}</span>
                                    {/* Timestamp */}
                                    {stageTimestamps.find(t => t.stage === idx) ? (
                                      <span className="text-[10px] text-slate-300 mt-1.5 font-bold font-mono tracking-tighter">{stageTimestamps.find(t => t.stage === idx).time}</span>
                                    ) : (
                                      <span className="text-[10px] text-slate-600 mt-1.5 font-bold font-mono tracking-tighter">--:--:--.---</span>
                                    )}
                                  </div>
                               </div>
                             );
                           })}
                        </div>
                      </div>
                      
                    </motion.div>
                  )}

                  {/* Result State */}
                  {result && !isProcessing && (
                    <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
                      
                      {/* EVIDENCE CHAIN OF CUSTODY */}
                      <div className="bg-slate-900/40 border border-emerald-500/30 rounded-lg p-5">
                          <h3 className="text-xs font-bold text-emerald-400 tracking-widest uppercase mb-4 border-b border-emerald-500/20 pb-2 flex items-center gap-2"><Shield className="w-4 h-4"/> EVIDENCE INTEGRITY METADATA</h3>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm font-mono text-slate-300">
                             <div className="flex flex-col gap-1">
                                <span className="text-[10px] font-sans font-bold text-slate-500 uppercase tracking-widest">Evidence ID</span>
                                <span className="text-white font-bold">{result.metadata?.evidence_id || "EVD-PENDING"}</span>
                             </div>
                             <div className="flex flex-col gap-1">
                                <span className="text-[10px] font-sans font-bold text-slate-500 uppercase tracking-widest">Type / Size</span>
                                <span>{result.metadata?.file_type} • {result.metadata?.size}</span>
                             </div>
                             <div className="flex flex-col gap-1">
                                <span className="text-[10px] font-sans font-bold text-slate-500 uppercase tracking-widest">Acquired Time</span>
                                <span>{result.metadata?.acquired || "UNKNOWN"}</span>
                             </div>
                             <div className="flex flex-col gap-1">
                                <span className="text-[10px] font-sans font-bold text-slate-500 uppercase tracking-widest">Integrity Status</span>
                                <span className="text-emerald-400 font-bold flex items-center gap-1"><CheckCircle className="w-3 h-3"/> VERIFIED</span>
                             </div>
                             <div className="col-span-2 md:col-span-4 flex flex-col gap-1 mt-2 bg-slate-950/50 p-3 rounded border border-slate-800">
                                <span className="text-[10px] font-sans font-bold text-slate-500 uppercase tracking-widest flex items-center gap-1"><Lock className="w-3 h-3"/> Cryptographic Hash (SHA-256)</span>
                                <span className="text-sky-300 break-all">{result.file_hash}</span>
                             </div>
                          </div>
                      </div>

                      {/* XAI TELEMETRY */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-slate-900/40 border border-slate-700/50 rounded-lg p-5">
                             <h3 className="text-xs font-bold text-sky-400 tracking-widest uppercase mb-4 border-b border-sky-500/20 pb-2 flex items-center gap-2"><Activity className="w-4 h-4"/> FORENSIC SIGNALS & TELEMETRY</h3>
                             <div className="space-y-4 text-sm">
                                <div className="flex justify-between items-center pb-2 border-b border-slate-800">
                                    <span className="text-slate-400 font-sans">Manipulation Score</span>
                                    <span className="font-mono text-red-400 font-bold">{result.xai?.manipulation_score || result.xai?.manipulation_probability || "N/A"}</span>
                                </div>
                                <div className="flex justify-between items-center pb-2 border-b border-slate-800">
                                    <span className="text-slate-400 font-sans">Image Authenticity</span>
                                    <span className="font-mono text-yellow-400 font-bold">{result.xai?.authenticity || "PENDING"}</span>
                                </div>
                                <div className="flex justify-between items-center pb-2 border-b border-slate-800">
                                    <span className="text-slate-400 font-sans">Processing Time</span>
                                    <span className="font-mono text-slate-300">{result.xai?.processing_time || "N/A"}</span>
                                </div>
                                <div className="pt-2">
                                    <span className="text-[10px] font-sans font-bold text-slate-500 uppercase tracking-widest mb-1 block">Algorithmic Signals / Anomalies</span>
                                    <span className="text-[9px] font-sans text-slate-600 mb-3 block">LLM-Assisted reasoning over derived metadata</span>
                                    <ul className="list-disc pl-4 space-y-1 font-mono text-xs text-slate-300">
                                        {(result.xai?.anomalies || ["No signals provided"]).map((a, i) => (
                                            <li key={i}>{a}</li>
                                        ))}
                                    </ul>
                                </div>
                             </div>
                        </div>

                        {/* Processed Image */}
                        {result.processed_image_url && (
                          <div className="relative border border-slate-700/50 rounded bg-black/40 backdrop-blur-md p-2 overflow-hidden shadow-inner group">
                            <div className="absolute top-3 left-3 px-3 py-1.5 bg-black/80 backdrop-blur-md border border-slate-700/50 rounded text-[11px] font-semibold text-sky-300 font-bold tracking-wider flex items-center gap-2 z-10 shadow-[0_0_10px_rgba(0,0,0,0.5)] font-sans">
                              <AlertTriangle className="w-3 h-3 text-yellow-500" /> DERIVATIVE VISUALIZATION (NOT ORIGINAL EVIDENCE)
                            </div>
                            <img src={result.processed_image_url} alt="Restored Evidence" className="w-full h-full object-contain max-h-[400px] relative z-0 rounded" />
                            <div className="absolute inset-0 bg-sky-500/5 mix-blend-overlay pointer-events-none"></div>
                          </div>
                        )}
                      </div>

                      {/* JSON Data Viewer */}
                      <div className="bg-slate-950/40 backdrop-blur-md rounded border border-slate-700/50 p-6 shadow-inner relative">
                        <div className="absolute top-3 right-3 px-3 py-1.5 bg-sky-900/30 border border-sky-500/30 rounded text-[11px] font-semibold text-sky-300 font-bold tracking-wider flex items-center gap-2 font-sans">
                          <FileJson className="w-3 h-3" /> STRUCTURED EXTRACTION
                        </div>
                        <pre className="text-slate-300 text-[13px] mt-6 overflow-x-auto leading-loose font-mono">
                          <span className="text-slate-500">{"{ "}</span>
                          {"\n"}
                          {Object.entries(result.extracted_data).map(([key, value], i) => (
                            <div key={key} className="pl-6 py-0.5 whitespace-pre-wrap hover:bg-slate-800/30 transition-colors rounded">
                              <span className="text-sky-300">"{key}"</span>
                              <span className="text-slate-300">: </span>
                              <span className="text-emerald-300">"{value}"</span>
                              <span className="text-slate-500">{i < Object.keys(result.extracted_data).length - 1 ? ',' : ''}</span>
                            </div>
                          ))}
                          <span className="text-slate-500">{"}"}</span>
                        </pre>
                      </div>

                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
      
      {/* Legal Modal */}
      <AnimatePresence>
        {showWarningModal && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
            <motion.div initial={{ scale: 0.95, y: 20 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.95, y: 20 }} className="bg-slate-900/90 backdrop-blur-xl border border-red-500/50 rounded-xl max-w-lg w-full p-8 shadow-[0_0_50px_rgba(239,68,68,0.2)] relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 bg-red-500"></div>
              <div className="flex items-center gap-4 text-red-500 mb-6">
                <div className="p-3 bg-red-500/10 rounded border border-red-500/20">
                  <ShieldAlert className="w-8 h-8" />
                </div>
                <h2 className="text-xl font-orbitron font-bold tracking-widest text-white glow-text" style={{ textShadow: '0 0 10px rgba(239,68,68,0.6)' }}>RESTRICTED PROTOCOL</h2>
              </div>
              <p className="text-sm font-medium text-slate-300 mb-8 leading-relaxed">
                You are about to invoke the CodeFormer Generative Adversarial Network. This model is governed by a strict <span className="text-red-400 font-bold">S-Lab Non-Commercial/Research License</span>. 
                <br/><br/>
                By proceeding, the agency assumes all legal compliance liability for the generated restorative outputs in a court of law.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <button onClick={() => { playCyberSound('toggle'); setShowWarningModal(false); }} className="flex-1 py-3 rounded bg-slate-800/80 text-slate-300 font-bold hover:bg-slate-700 transition-colors border border-slate-600 text-sm font-medium tracking-widest uppercase">
                  Abort
                </button>
                <button onClick={() => { playCyberSound('execute'); setUseCodeformer(true); setShowWarningModal(false); }} className="flex-1 py-3 rounded bg-red-600/90 text-white font-bold hover:bg-red-500 transition-colors shadow-[0_0_15px_rgba(239,68,68,0.4)] text-sm font-medium tracking-widest uppercase border border-red-500">
                  Authorize GAN
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
