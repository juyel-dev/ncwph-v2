import React, { useState } from 'react';
import { Camera, UserPlus, ShieldCheck, Upload, Loader2 } from 'lucide-react';
import axios from 'axios';

const API_URL = "https://ncwph-v2.onrender.com";

function App() {
  const [mode, setMode] = useState<'enroll' | 'verify'>('enroll');
  const [userId, setUserId] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleImage = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
    }
  };

  const handleSubmit = async () => {
    if (!userId || !image) return;
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", image);

    try {
      const endpoint = mode === 'enroll' 
        ? `/enroll/${userId}` 
        : `/verify/${userId}`;

      const res = await axios.post(`\( {API_URL} \){endpoint}`, formData);
      setResult(res.data);
    } catch (err: any) {
      setResult({ 
        status: "error", 
        message: err.response?.data?.detail || "Something went wrong" 
      });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-950 to-violet-950 flex items-center justify-center p-6">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-6xl font-bold text-white tracking-tighter mb-2">NCWPH v2.0</h1>
          <p className="text-xl text-white/70">Neural Context Wavelet Phase Hashing</p>
        </div>

        {/* Glass Card */}
        <div className="backdrop-blur-3xl bg-white/10 border border-white/20 rounded-3xl shadow-2xl overflow-hidden">
          {/* Tabs */}
          <div className="flex border-b border-white/10">
            <button
              onClick={() => setMode('enroll')}
              className={`flex-1 py-5 text-lg font-medium transition-all ${mode === 'enroll' ? 'text-white border-b-4 border-violet-400' : 'text-white/60'}`}
            >
              <UserPlus className="inline mr-2" /> Enroll
            </button>
            <button
              onClick={() => setMode('verify')}
              className={`flex-1 py-5 text-lg font-medium transition-all ${mode === 'verify' ? 'text-white border-b-4 border-violet-400' : 'text-white/60'}`}
            >
              <ShieldCheck className="inline mr-2" /> Verify
            </button>
          </div>

          <div className="p-10 space-y-8">
            <input
              type="text"
              placeholder="Enter User ID or Email"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              className="w-full bg-white/10 border border-white/30 rounded-2xl px-6 py-4 text-white placeholder:text-white/50 focus:outline-none focus:border-violet-400 transition"
            />

            {/* Image Upload */}
            <div 
              className="border-2 border-dashed border-white/30 rounded-3xl p-12 text-center hover:border-violet-400 transition cursor-pointer"
              onClick={() => document.getElementById('file-input')?.click()}
            >
              {preview ? (
                <img src={preview} alt="preview" className="mx-auto max-h-72 rounded-2xl shadow-lg" />
              ) : (
                <div>
                  <Camera className="mx-auto w-20 h-20 mb-4 text-white/60" />
                  <p className="text-xl text-white/80">Upload Face Photo</p>
                  <p className="text-sm text-white/50 mt-2">JPG, PNG supported</p>
                </div>
              )}
              <input 
                id="file-input" 
                type="file" 
                accept="image/*" 
                className="hidden" 
                onChange={handleImage} 
              />
            </div>

            <button
              onClick={handleSubmit}
              disabled={loading || !userId || !image}
              className="w-full py-5 rounded-2xl bg-gradient-to-r from-violet-600 to-indigo-600 text-xl font-semibold flex items-center justify-center gap-3 hover:scale-105 transition disabled:opacity-50"
            >
              {loading ? (
                <><Loader2 className="animate-spin" /> Processing...</>
              ) : mode === 'enroll' ? (
                'Enroll User'
              ) : (
                'Verify Identity'
              )}
            </button>
          </div>

          {/* Result */}
          {result && (
            <div className={`mx-10 mb-10 p-8 rounded-2xl text-center text-xl font-medium transition-all ${
              result.status === 'error' 
                ? 'bg-red-500/20 border border-red-400' 
                : result.match || result.decision === 'ENROLLED'
                ? 'bg-green-500/20 border border-green-400'
                : 'bg-yellow-500/20 border border-yellow-400'
            }`}>
              <p className="text-3xl mb-2">
                {result.status === 'error' ? '❌' : result.match ? '✅' : '⚠️'}
              </p>
              <p>{result.message}</p>
              {result.confidence && (
                <p className="text-sm mt-3 opacity-75">
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                </p>
              )}
            </div>
          )}
        </div>

        <p className="text-center text-white/40 mt-8 text-sm">
          Production • Render.com • Zero Backend on Client
        </p>
      </div>
    </div>
  );
}

export default App;
