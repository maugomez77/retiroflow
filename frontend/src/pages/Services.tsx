import { useApi } from '../hooks/useApi';

const svcEmoji: Record<string, string> = {
  transportation: '🚐', catering: '🍽️', accommodation: '🏠',
  excursion: '🗺️', ceremony: '🔥', photography: '📸',
};

export default function Services({ lang }: { lang: string }) {
  const { data, loading } = useApi<{ services: any[]; total: number }>('/services', { services: [], total: 0 });

  return (
    <div>
      <div className="page-header">
        <h1>{lang === 'es' ? 'Servicios Locales' : 'Local Services'}</h1>
        <p>{data.total} {lang === 'es' ? 'proveedores en Oaxaca' : 'providers across Oaxaca'}</p>
      </div>

      {loading ? <p>Loading...</p> : (
        <div className="card-grid">
          {data.services.map((s: any) => (
            <div key={s.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <h3>{svcEmoji[s.type] || '📋'} {s.name}</h3>
                <span style={{ color: 'var(--accent)', fontWeight: 600 }}>⭐ {s.rating}</span>
              </div>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-light)', margin: '8px 0' }}>{s.description}</p>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginTop: 8 }}>
                <span><strong>{lang === 'es' ? 'Proveedor' : 'Provider'}:</strong> {s.provider}</span>
                <span style={{ fontWeight: 600 }}>${s.price_range_usd?.min}-${s.price_range_usd?.max}</span>
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-light)', marginTop: 4 }}>
                📍 {(s.location || '').replace(/_/g, ' ')} &nbsp;|&nbsp; 📞 {s.contact}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
