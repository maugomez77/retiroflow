import { useApi } from '../hooks/useApi';

interface Stats {
  total_centers: number;
  total_retreats_active: number;
  total_participants: number;
  monthly_revenue_usd: number;
  avg_occupancy_pct: number;
  top_retreat_types: { type: string; count: number }[];
  upcoming_retreats: { id: string; name: string; start_date: string }[];
}

const labels: Record<string, Record<string, string>> = {
  en: { title: 'Dashboard', sub: 'Oaxaca wellness retreat operations at a glance', centers: 'Retreat Centers', active: 'Active Retreats', participants: 'Participants', revenue: 'Monthly Revenue', occupancy: 'Avg Occupancy', top: 'Top Retreat Types', upcoming: 'Upcoming Retreats' },
  es: { title: 'Panel', sub: 'Operaciones de retiros de bienestar en Oaxaca', centers: 'Centros de Retiro', active: 'Retiros Activos', participants: 'Participantes', revenue: 'Ingresos Mensuales', occupancy: 'Ocupacion Prom.', top: 'Tipos Populares', upcoming: 'Proximos Retiros' },
};

export default function Dashboard({ lang }: { lang: string }) {
  const t = labels[lang] || labels.en;
  const { data, loading } = useApi<Stats>('/stats', { total_centers: 0, total_retreats_active: 0, total_participants: 0, monthly_revenue_usd: 0, avg_occupancy_pct: 0, top_retreat_types: [], upcoming_retreats: [] });

  if (loading) return <div className="page-header"><h1>{t.title}</h1><p>Loading...</p></div>;

  return (
    <div>
      <div className="page-header">
        <h1>{t.title}</h1>
        <p>{t.sub}</p>
      </div>

      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-value">{data.total_centers}</div>
          <div className="stat-label">{t.centers}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.total_retreats_active}</div>
          <div className="stat-label">{t.active}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.total_participants}</div>
          <div className="stat-label">{t.participants}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">${data.monthly_revenue_usd.toLocaleString()}</div>
          <div className="stat-label">{t.revenue}</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{data.avg_occupancy_pct}%</div>
          <div className="stat-label">{t.occupancy}</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div className="card">
          <h3 style={{ marginBottom: 12 }}>{t.top}</h3>
          {data.top_retreat_types.map((tt) => (
            <div key={tt.type} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid var(--border)' }}>
              <span style={{ textTransform: 'capitalize' }}>{tt.type.replace('_', ' ')}</span>
              <strong>{tt.count}</strong>
            </div>
          ))}
        </div>
        <div className="card">
          <h3 style={{ marginBottom: 12 }}>{t.upcoming}</h3>
          {data.upcoming_retreats.slice(0, 8).map((r) => (
            <div key={r.id} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid var(--border)' }}>
              <span>{r.name.length > 35 ? r.name.slice(0, 35) + '...' : r.name}</span>
              <span style={{ color: 'var(--text-light)', fontSize: '0.85rem' }}>{r.start_date}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
