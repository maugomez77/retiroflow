import { useState } from 'react';
import { useApi } from '../hooks/useApi';

const typeColors: Record<string, string> = {
  yoga: '#00695c', meditation: '#1565c0', healing: '#2e7d32', temazcal: '#e65100',
  mixed: '#7b1fa2', ayahuasca: '#4e342e', wellness_spa: '#00838f',
};

export default function Retreats({ lang }: { lang: string }) {
  const { data, loading } = useApi<{ retreats: any[]; total: number }>('/retreats', { retreats: [], total: 0 });
  const [view, setView] = useState<'list' | 'calendar'>('list');

  const buildCalendar = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const days: { num: number; retreats: any[] }[] = [];

    for (let i = 0; i < firstDay; i++) days.push({ num: 0, retreats: [] });
    for (let d = 1; d <= daysInMonth; d++) {
      const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      const matching = data.retreats.filter((r: any) => r.start_date <= dateStr && r.end_date >= dateStr);
      days.push({ num: d, retreats: matching });
    }
    return days;
  };

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>{lang === 'es' ? 'Retiros' : 'Retreats'}</h1>
          <p>{data.total} {lang === 'es' ? 'retiros registrados' : 'retreats registered'}</p>
        </div>
        <div>
          <button className={`btn ${view === 'list' ? 'btn-primary' : ''}`} onClick={() => setView('list')} style={{ marginRight: 8 }}>
            {lang === 'es' ? 'Lista' : 'List'}
          </button>
          <button className={`btn ${view === 'calendar' ? 'btn-primary' : ''}`} onClick={() => setView('calendar')}>
            {lang === 'es' ? 'Calendario' : 'Calendar'}
          </button>
        </div>
      </div>

      {loading ? <p>Loading...</p> : view === 'list' ? (
        <table className="data-table">
          <thead>
            <tr>
              <th>{lang === 'es' ? 'Nombre' : 'Name'}</th>
              <th>{lang === 'es' ? 'Tipo' : 'Type'}</th>
              <th>{lang === 'es' ? 'Fechas' : 'Dates'}</th>
              <th>{lang === 'es' ? 'Precio' : 'Price'}</th>
              <th>{lang === 'es' ? 'Ocupacion' : 'Occupancy'}</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.retreats.map((r: any) => {
              const pct = r.max_participants > 0 ? (r.current_participants / r.max_participants) * 100 : 0;
              const barClass = pct < 50 ? 'occupancy-low' : pct < 80 ? 'occupancy-mid' : 'occupancy-high';
              return (
                <tr key={r.id}>
                  <td><strong>{r.name}</strong></td>
                  <td><span style={{ color: typeColors[r.type] || '#333', textTransform: 'capitalize' }}>{r.type?.replace(/_/g, ' ')}</span></td>
                  <td>{r.start_date} — {r.end_date}</td>
                  <td>${r.price_usd?.toLocaleString()}</td>
                  <td>
                    <div>{r.current_participants}/{r.max_participants}</div>
                    <div className="occupancy-bar"><div className={`occupancy-fill ${barClass}`} style={{ width: `${pct}%` }} /></div>
                  </td>
                  <td><span className={`badge badge-${r.status}`}>{r.status}</span></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      ) : (
        <div>
          <div style={{ textAlign: 'center', fontWeight: 600, marginBottom: 8, fontSize: '1.1rem' }}>
            {new Date().toLocaleString(lang === 'es' ? 'es-MX' : 'en-US', { month: 'long', year: 'numeric' })}
          </div>
          <div className="calendar-grid">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(d => (
              <div key={d} style={{ textAlign: 'center', fontWeight: 600, fontSize: '0.8rem', padding: 4 }}>{d}</div>
            ))}
            {buildCalendar().map((day, i) => (
              <div key={i} className={`calendar-day ${day.retreats.length > 0 ? 'has-retreat' : ''}`}>
                {day.num > 0 && (
                  <>
                    <div className="day-num">{day.num}</div>
                    {day.retreats.slice(0, 2).map((r: any) => (
                      <div key={r.id} style={{ fontSize: '0.65rem', color: typeColors[r.type] || '#333', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        <span className="retreat-dot" style={{ background: typeColors[r.type] || 'var(--primary)' }} />
                        {r.name.slice(0, 15)}
                      </div>
                    ))}
                    {day.retreats.length > 2 && <div style={{ fontSize: '0.6rem', color: 'var(--text-light)' }}>+{day.retreats.length - 2} more</div>}
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
