import { useApi } from '../hooks/useApi';

const flagEmoji: Record<string, string> = {
  US: '🇺🇸', CA: '🇨🇦', MX: '🇲🇽', UK: '🇬🇧', DE: '🇩🇪', FR: '🇫🇷',
  NL: '🇳🇱', IT: '🇮🇹', JP: '🇯🇵', AU: '🇦🇺', BR: '🇧🇷', CO: '🇨🇴',
  AR: '🇦🇷', SE: '🇸🇪', RO: '🇷🇴', IE: '🇮🇪', PL: '🇵🇱', ES: '🇪🇸',
};

export default function Participants({ lang }: { lang: string }) {
  const { data, loading } = useApi<{ participants: any[]; total: number }>('/participants', { participants: [], total: 0 });

  return (
    <div>
      <div className="page-header">
        <h1>{lang === 'es' ? 'Participantes' : 'Participants'}</h1>
        <p>{data.total} {lang === 'es' ? 'participantes registrados' : 'registered participants'}</p>
      </div>

      {loading ? <p>Loading...</p> : (
        <table className="data-table">
          <thead>
            <tr>
              <th>{lang === 'es' ? 'Nombre' : 'Name'}</th>
              <th>{lang === 'es' ? 'Pais' : 'Country'}</th>
              <th>{lang === 'es' ? 'Nivel' : 'Level'}</th>
              <th>{lang === 'es' ? 'Retiros' : 'Retreats'}</th>
              <th>{lang === 'es' ? 'Total Gastado' : 'Total Spent'}</th>
              <th>{lang === 'es' ? 'Dieta' : 'Dietary'}</th>
            </tr>
          </thead>
          <tbody>
            {data.participants.map((p: any) => (
              <tr key={p.id}>
                <td><strong>{p.name}</strong><br /><span style={{ fontSize: '0.8rem', color: 'var(--text-light)' }}>{p.email}</span></td>
                <td>{flagEmoji[p.country] || '🌍'} {p.country}</td>
                <td><span style={{ textTransform: 'capitalize' }}>{p.experience_level}</span></td>
                <td>{(p.retreat_ids || []).length}</td>
                <td style={{ fontWeight: 600 }}>${(p.total_spent_usd || 0).toLocaleString()}</td>
                <td>{(p.dietary_restrictions || []).join(', ') || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
