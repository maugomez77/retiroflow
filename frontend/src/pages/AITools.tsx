import { useState } from 'react';
import { useApi, postApi } from '../hooks/useApi';

export default function AITools({ lang }: { lang: string }) {
  const { data: partsData } = useApi<{ participants: any[] }>('/participants', { participants: [] });
  const { data: centersData } = useApi<{ centers: any[] }>('/centers', { centers: [] });
  const { data: insightsData } = useApi<{ insights: any[] }>('/insights', { insights: [] });

  const [selectedParticipant, setSelectedParticipant] = useState('');
  const [selectedCenter, setSelectedCenter] = useState('');
  const [selectedSeason, setSelectedSeason] = useState('peak_winter');
  const [retreatType, setRetreatType] = useState('yoga');
  const [retreatDays, setRetreatDays] = useState(7);
  const [retreatLevel, setRetreatLevel] = useState('intermediate');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('recommend');

  const runAI = async (endpoint: string, params: Record<string, string>) => {
    setLoading(true);
    setResult(null);
    try {
      const data = await postApi(endpoint, params);
      setResult(data);
    } catch (e: any) {
      setResult({ error: e.message });
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'recommend', label: lang === 'es' ? 'Recomendar' : 'Recommend', icon: '🎯' },
    { id: 'pricing', label: lang === 'es' ? 'Precios' : 'Pricing', icon: '💰' },
    { id: 'plan', label: lang === 'es' ? 'Planificar' : 'Plan Retreat', icon: '📋' },
    { id: 'insights', label: lang === 'es' ? 'Insights' : 'Insights', icon: '💡' },
  ];

  const priorityColor: Record<string, string> = { high: 'var(--danger)', medium: 'var(--warning)', low: 'var(--success)' };

  return (
    <div>
      <div className="page-header">
        <h1>🤖 {lang === 'es' ? 'Herramientas de IA' : 'AI Tools'}</h1>
        <p>{lang === 'es' ? 'Inteligencia artificial para retiros' : 'AI-powered retreat intelligence'}</p>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
        {tabs.map(tab => (
          <button key={tab.id} className={`btn ${activeTab === tab.id ? 'btn-primary' : ''}`} onClick={() => { setActiveTab(tab.id); setResult(null); }}>
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'recommend' && (
        <div className="card">
          <h3>{lang === 'es' ? 'Recomendar Retiro a Participante' : 'Match Participant to Retreat'}</h3>
          <div style={{ margin: '16px 0', display: 'flex', gap: 12, alignItems: 'center' }}>
            <select value={selectedParticipant} onChange={e => setSelectedParticipant(e.target.value)} style={{ padding: 8, borderRadius: 8, border: '1px solid var(--border)', flex: 1 }}>
              <option value="">{lang === 'es' ? 'Seleccionar participante...' : 'Select participant...'}</option>
              {(partsData.participants || []).map((p: any) => <option key={p.id} value={p.id}>{p.name} ({p.country})</option>)}
            </select>
            <button className="btn btn-accent" disabled={!selectedParticipant || loading} onClick={() => runAI('/ai/recommend', { participant_id: selectedParticipant })}>
              {loading ? '...' : lang === 'es' ? 'Analizar' : 'Analyze'}
            </button>
          </div>
        </div>
      )}

      {activeTab === 'pricing' && (
        <div className="card">
          <h3>{lang === 'es' ? 'Optimizar Precios' : 'Optimize Pricing'}</h3>
          <div style={{ margin: '16px 0', display: 'flex', gap: 12, alignItems: 'center' }}>
            <select value={selectedCenter} onChange={e => setSelectedCenter(e.target.value)} style={{ padding: 8, borderRadius: 8, border: '1px solid var(--border)', flex: 1 }}>
              <option value="">{lang === 'es' ? 'Seleccionar centro...' : 'Select center...'}</option>
              {(centersData.centers || []).map((c: any) => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
            <select value={selectedSeason} onChange={e => setSelectedSeason(e.target.value)} style={{ padding: 8, borderRadius: 8, border: '1px solid var(--border)' }}>
              <option value="peak_winter">Peak Winter</option>
              <option value="shoulder_spring">Shoulder Spring</option>
              <option value="low_summer">Low Summer</option>
              <option value="peak_fall">Peak Fall</option>
            </select>
            <button className="btn btn-accent" disabled={!selectedCenter || loading} onClick={() => runAI('/ai/optimize-pricing', { center_id: selectedCenter, season: selectedSeason })}>
              {loading ? '...' : lang === 'es' ? 'Optimizar' : 'Optimize'}
            </button>
          </div>
        </div>
      )}

      {activeTab === 'plan' && (
        <div className="card">
          <h3>{lang === 'es' ? 'Planificar Curriculum de Retiro' : 'Plan Retreat Curriculum'}</h3>
          <div style={{ margin: '16px 0', display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
            <select value={retreatType} onChange={e => setRetreatType(e.target.value)} style={{ padding: 8, borderRadius: 8, border: '1px solid var(--border)' }}>
              {['yoga', 'meditation', 'healing', 'temazcal', 'mixed', 'wellness_spa'].map(t => <option key={t} value={t}>{t.replace('_', ' ')}</option>)}
            </select>
            <input type="number" value={retreatDays} onChange={e => setRetreatDays(Number(e.target.value))} min={1} max={30} style={{ padding: 8, borderRadius: 8, border: '1px solid var(--border)', width: 80 }} />
            <span>{lang === 'es' ? 'dias' : 'days'}</span>
            <select value={retreatLevel} onChange={e => setRetreatLevel(e.target.value)} style={{ padding: 8, borderRadius: 8, border: '1px solid var(--border)' }}>
              {['beginner', 'intermediate', 'advanced'].map(l => <option key={l} value={l}>{l}</option>)}
            </select>
            <button className="btn btn-accent" disabled={loading} onClick={() => runAI('/ai/plan-retreat', { type: retreatType, duration: String(retreatDays), level: retreatLevel })}>
              {loading ? '...' : lang === 'es' ? 'Generar' : 'Generate'}
            </button>
          </div>
        </div>
      )}

      {activeTab === 'insights' && (
        <div>
          {(insightsData.insights || []).map((ins: any) => (
            <div key={ins.id} className="card" style={{ borderLeft: `4px solid ${priorityColor[ins.priority] || 'var(--border)'}`, marginBottom: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ textTransform: 'uppercase', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-light)' }}>
                  {(ins.insight_type || '').replace(/_/g, ' ')}
                </span>
                <span style={{ fontSize: '0.75rem', fontWeight: 600, color: priorityColor[ins.priority] || '#333', textTransform: 'uppercase' }}>
                  {ins.priority}
                </span>
              </div>
              <h3 style={{ fontSize: '1rem' }}>{ins.title}</h3>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-light)', marginTop: 4 }}>{ins.description}</p>
            </div>
          ))}
        </div>
      )}

      {result && (
        <div className="card" style={{ marginTop: 16, background: '#f5f5f5' }}>
          <h3>{lang === 'es' ? 'Resultado de IA' : 'AI Result'}</h3>
          <pre style={{ whiteSpace: 'pre-wrap', fontSize: '0.85rem', marginTop: 8, maxHeight: 500, overflow: 'auto' }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
