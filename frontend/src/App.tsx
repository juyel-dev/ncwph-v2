import React, { useState } from 'react';
import { Upload, User, Shield, Camera } from 'lucide-react';
import axios from 'axios';

const API_BASE = 'https://your-render-url.onrender.com'; // পরে পরিবর্তন করবে

function App() {
  const [userId, setUserId] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>('');
  const [result, setResult] = useState<any>(null);
  const [mode, setMode] = useState<'enroll' | 'verify'>('enroll');
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async () => {
    if (!image || !userId) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('file', image);

    try {
      const endpoint = mode === 'enroll' 
        ? `/enroll/${userId}` 
        : `/verify/${userId}`;
      
      const res = await axios.post(`\( {API_BASE} \){endpoint}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(res.data);
    } catch (err) {
      alert('Error: ' + (err as any).message);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-950 flex items-center justify-center p-6 overflow-hidden relative">
      {/* Background effects */}
      <div className="absolute inset-0 bg-[radial-gradient(at_center,#ffffff15_0%,transparent_70%)]"></div>
      
      <div className="max-w-2xl w-full">
        <div className="text-center mb-10">
          <h1 className="text-6xl font-bold text-white mb-3 tracking-tighter">NCWPH</h1>
          <p className="text-xl text-white/70">Neural Context Wavelet Phase Hashing v2.0</p>
        </div>

        {/* Glass Card */}
        <div className="backdrop-blur-3xl bg-white/10 border border-white/20 rounded-3xl shadow-2xl p-10 text-white">
          <div className="flex gap-4 mb-8 justify-center">
            <button 
              onClick={() => setMode('enroll')}
              className={`px-8 py-3 rounded-2xl transition-all ${mode === 'enroll' ? 'bg-white text-black shadow-lg' : 'bg-white/10 hover:bg-white/20'}`}
            >
              Enroll
            </button>
            <button 
              onClick={() => setMode('verify')}
              className={`px-8 py-3 rounded-2xl transition-all ${mode === 'verify' ? 'bg-white text-black shadow-lg' : 'bg-white/10 hover:bg-white/20'}`}
            >
              Verify
            </button>
          </div>

          <div className="space-y-8">
            <input
              type="text"
              placeholder="User ID / Email"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              className="w-full bg-white/10 border border-white/30 rounded-2xl px-6 py-4 text-lg focus:outline-none focus:border-white/60 transition"
            />

            <div className="border-2 border-dashed border-white/30 rounded-3xl p-12 text-center hover:border-white/60 transition cursor-pointer"
                 onClick={() => document.getElementById('file')?.click()}>
              {preview ? (
                <img src={preview} alt="preview" className="mx-auto max-h-64 rounded-2xl" />
              ) : (
                <div>
                  <Camera className="mx-auto w-16 h-16 mb-4 opacity-70" />
                  <p className="text-xl">Upload Face Photo</p>
                </div>
              )}
              <input id="file" type="file" accept="image/*" className="hidden" onChange={handleImageChange} />
            </div>

            <button
              onClick={handleSubmit}
              disabled={loading || !image || !userId}
              className="w-full py-5 rounded-2xl bg-gradient-to-r from-violet-500 to-indigo-500 font-semibold text-xl disabled:opacity-50 hover:scale-105 transition transform"
            >
              {loading ? 'Processing...' : mode === 'enroll' ? 'Enroll User' : 'Verify Identity'}
            </button>
          </div>

          {result && (
            <div className={`mt-8 p-6 rounded-2xl text-center text-2xl font-medium transition-all ${result.match ? 'bg-green-500/20 border border-green-400' : 'bg-red-500/20 border border-red-400'}`}>
              {result.decision || (result.match ? '✅ Verified Successfully' : '❌ Not Matched')}
              <p className="text-sm mt-2 opacity-75">Confidence: {(result.confidence * 100).toFixed(1)}%</p>
            </div>
          )}
        </div>

        <p className="text-center text-white/40 mt-8 text-sm">Production Grade • Zero Backend on Client • Render.com Deployed</p>
      </div>
    </div>
  );
}

export default App;
