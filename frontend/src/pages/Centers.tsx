import { useApi } from '../hooks/useApi';

const locationEmoji: Record<string, string> = {
  mazunte: '🏖️', zipolite: '🌊', huatulco: '🏝️', oaxaca_city: '🏛️',
  hierve_el_agua: '⛰️', san_jose_del_pacifico: '☁️', monte_alban_area: '🏔️',
};

const typeEmoji: Record<string, string> = {
  yoga: '🧘', meditation: '🧘‍♂️', healing: '🌿', temazcal: '🔥',
  mixed: '✨', ayahuasca: '🌱', wellness_spa: '💆',
};

export default function Centers({ lang }: { lang: string }) {
  const { data, loading } = useApi<{ centers: any[]; total: number }>('/centers', { centers: [], total: 0 });

  return (
    <div>
      <div className="page-header">
        <h1>{lang === 'es' ? 'Centros de Retiro' : 'Retreat Centers'}</h1>
        <p>{lang === 'es' ? `${data.total} centros en Oaxaca` : `${data.total} centers across Oaxaca`}</p>
      </div>

      {loading ? <p>Loading...</p> : (
        <div className="card-grid">
          {data.centers.map((c: any) => (
            <div key={c.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <h3 style={{ fontSize: '1.1rem' }}>{c.name}</h3>
                <span style={{ fontSize: '0.85rem', color: 'var(--accent)' }}>{'⭐'.repeat(Math.round(c.rating))}</span>
              </div>
              <div style={{ margin: '8px 0', fontSize: '0.9rem', color: 'var(--text-light)' }}>
                {locationEmoji[c.location] || '📍'} {c.location?.replace(/_/g, ' ')} &nbsp;|&nbsp; {typeEmoji[c.type] || '📋'} {c.type?.replace(/_/g, ' ')}
              </div>
              <div style={{ fontSize: '0.85rem', margin: '8px 0' }}>
                <strong>{lang === 'es' ? 'Capacidad' : 'Capacity'}:</strong> {c.capacity} &nbsp;|&nbsp;
                <strong>{lang === 'es' ? 'Precio' : 'Price'}:</strong> ${c.price_range_usd?.min}-${c.price_range_usd?.max}/night
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 8 }}>
                {(c.amenities || []).slice(0, 5).map((a: string) => (
                  <span key={a} style={{ background: 'var(--bg)', padding: '2px 8px', borderRadius: 12, fontSize: '0.75rem' }}>{a.replace(/_/g, ' ')}</span>
                ))}
              </div>
              <div style={{ marginTop: 8, fontSize: '0.8rem', color: 'var(--text-light)' }}>
                {lang === 'es' ? 'Idiomas' : 'Languages'}: {(c.languages || []).join(', ')} &nbsp;|&nbsp;
                {lang === 'es' ? 'Contacto' : 'Contact'}: {c.contact}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
