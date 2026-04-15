import { useApi } from '../hooks/useApi';

const specEmoji: Record<string, string> = {
  yoga: '🧘', meditation: '🧘‍♂️', breathwork: '💨', temazcal: '🔥',
  herbalism: '🌿', massage: '💆', sound_healing: '🔔', reiki: '✨',
};

export default function Facilitators({ lang }: { lang: string }) {
  const { data, loading } = useApi<{ facilitators: any[]; total: number }>('/facilitators', { facilitators: [], total: 0 });

  return (
    <div>
      <div className="page-header">
        <h1>{lang === 'es' ? 'Facilitadores' : 'Facilitators'}</h1>
        <p>{data.total} {lang === 'es' ? 'facilitadores en la red' : 'facilitators in the network'}</p>
      </div>

      {loading ? <p>Loading...</p> : (
        <div className="card-grid">
          {data.facilitators.map((f: any) => (
            <div key={f.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <h3>{f.name}</h3>
                <span className={`badge badge-${f.availability === 'available' ? 'active' : f.availability === 'booked' ? 'pending' : 'cancelled'}`}>
                  {f.availability}
                </span>
              </div>
              <div style={{ margin: '8px 0', display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                {(f.specialties || []).map((s: string) => (
                  <span key={s} style={{ background: 'var(--bg)', padding: '2px 8px', borderRadius: 12, fontSize: '0.8rem' }}>
                    {specEmoji[s] || '📋'} {s.replace(/_/g, ' ')}
                  </span>
                ))}
              </div>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-light)', margin: '8px 0' }}>{f.bio}</p>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginTop: 8 }}>
                <span>⭐ {f.rating}</span>
                <span style={{ fontWeight: 600 }}>${f.hourly_rate_usd}/hr</span>
                <span>{(f.languages || []).join(', ')}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
