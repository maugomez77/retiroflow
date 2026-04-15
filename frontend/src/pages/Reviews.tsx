import { useApi } from '../hooks/useApi';

const aspectLabels: Record<string, Record<string, string>> = {
  en: { instruction: 'Instruction', accommodation: 'Accommodation', food: 'Food', location: 'Location', value: 'Value' },
  es: { instruction: 'Instruccion', accommodation: 'Alojamiento', food: 'Comida', location: 'Ubicacion', value: 'Valor' },
};

export default function Reviews({ lang }: { lang: string }) {
  const { data: reviewsData, loading } = useApi<{ reviews: any[]; total: number }>('/reviews', { reviews: [], total: 0 });
  const { data: retreatsData } = useApi<{ retreats: any[] }>('/retreats', { retreats: [] });
  const { data: partsData } = useApi<{ participants: any[] }>('/participants', { participants: [] });

  const retreatMap = Object.fromEntries((retreatsData.retreats || []).map((r: any) => [r.id, r.name]));
  const partMap = Object.fromEntries((partsData.participants || []).map((p: any) => [p.id, p.name]));
  const aLabels = aspectLabels[lang] || aspectLabels.en;

  const avgRating = reviewsData.reviews.length > 0
    ? (reviewsData.reviews.reduce((s: number, r: any) => s + (r.rating || 0), 0) / reviewsData.reviews.length).toFixed(1)
    : '0.0';

  return (
    <div>
      <div className="page-header">
        <h1>{lang === 'es' ? 'Resenas' : 'Reviews'}</h1>
        <p>{reviewsData.total} {lang === 'es' ? 'resenas' : 'reviews'} &nbsp;|&nbsp; {lang === 'es' ? 'Promedio' : 'Average'}: ⭐ {avgRating}/5</p>
      </div>

      {loading ? <p>Loading...</p> : (
        <div>
          {reviewsData.reviews.map((r: any) => (
            <div key={r.id} className="card" style={{ marginBottom: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                <div>
                  <strong>{partMap[r.participant_id] || 'Anonymous'}</strong>
                  <span style={{ color: 'var(--text-light)', fontSize: '0.85rem', marginLeft: 8 }}>
                    on {retreatMap[r.retreat_id] || r.retreat_id}
                  </span>
                </div>
                <div>
                  <span style={{ color: 'var(--accent)' }}>{'⭐'.repeat(Math.round(r.rating))}</span>
                  <span style={{ marginLeft: 4, fontWeight: 600 }}>{r.rating}/5</span>
                </div>
              </div>
              <p style={{ margin: '8px 0', fontStyle: 'italic' }}>"{r.comment}"</p>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 8, marginTop: 12 }}>
                {Object.entries(r.aspects || {}).map(([key, val]) => (
                  <div key={key}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-light)' }}>{aLabels[key] || key}</div>
                    <div className="sentiment-bar">
                      <div className="bar-bg"><div className="bar-fill" style={{ width: `${((val as number) / 5) * 100}%` }} /></div>
                      <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>{val as number}</span>
                    </div>
                  </div>
                ))}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-light)', marginTop: 8 }}>{r.date}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
