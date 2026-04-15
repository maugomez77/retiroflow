import { useApi } from '../hooks/useApi';

export default function Bookings({ lang }: { lang: string }) {
  const { data: bookingsData, loading: bLoading } = useApi<{ bookings: any[]; total: number }>('/bookings', { bookings: [], total: 0 });
  const { data: retreatsData } = useApi<{ retreats: any[] }>('/retreats', { retreats: [] });
  const { data: partsData } = useApi<{ participants: any[] }>('/participants', { participants: [] });

  const retreatMap = Object.fromEntries((retreatsData.retreats || []).map((r: any) => [r.id, r.name]));
  const partMap = Object.fromEntries((partsData.participants || []).map((p: any) => [p.id, p.name]));

  const totalRev = bookingsData.bookings
    .filter((b: any) => ['paid', 'confirmed', 'checked_in', 'completed'].includes(b.status))
    .reduce((s: number, b: any) => s + (b.amount_usd || 0), 0);

  return (
    <div>
      <div className="page-header">
        <h1>{lang === 'es' ? 'Reservaciones' : 'Bookings'}</h1>
        <p>{bookingsData.total} {lang === 'es' ? 'reservaciones' : 'bookings'} &nbsp;|&nbsp; {lang === 'es' ? 'Ingresos' : 'Revenue'}: ${totalRev.toLocaleString()}</p>
      </div>

      {bLoading ? <p>Loading...</p> : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>{lang === 'es' ? 'Retiro' : 'Retreat'}</th>
              <th>{lang === 'es' ? 'Participante' : 'Participant'}</th>
              <th>{lang === 'es' ? 'Monto' : 'Amount'}</th>
              <th>{lang === 'es' ? 'Deposito' : 'Deposit'}</th>
              <th>Status</th>
              <th>{lang === 'es' ? 'Fecha' : 'Date'}</th>
            </tr>
          </thead>
          <tbody>
            {bookingsData.bookings.map((b: any) => (
              <tr key={b.id}>
                <td style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{b.id}</td>
                <td>{(retreatMap[b.retreat_id] || b.retreat_id || '').slice(0, 30)}</td>
                <td>{partMap[b.participant_id] || b.participant_id}</td>
                <td style={{ fontWeight: 600 }}>${(b.amount_usd || 0).toLocaleString()}</td>
                <td>${(b.deposit_usd || 0).toLocaleString()}</td>
                <td><span className={`badge badge-${b.status}`}>{b.status}</span></td>
                <td>{b.booking_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
