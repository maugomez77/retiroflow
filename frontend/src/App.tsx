import { Routes, Route, NavLink } from 'react-router-dom';
import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import Centers from './pages/Centers';
import Retreats from './pages/Retreats';
import Participants from './pages/Participants';
import Facilitators from './pages/Facilitators';
import Bookings from './pages/Bookings';
import Services from './pages/Services';
import Reviews from './pages/Reviews';
import AITools from './pages/AITools';

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊', section: 'Overview' },
  { path: '/centers', label: 'Retreat Centers', icon: '🏡', section: 'Management' },
  { path: '/retreats', label: 'Retreats Calendar', icon: '🧘', section: 'Management' },
  { path: '/participants', label: 'Participants', icon: '👤', section: 'Management' },
  { path: '/facilitators', label: 'Facilitators', icon: '🎓', section: 'Management' },
  { path: '/bookings', label: 'Bookings', icon: '📋', section: 'Operations' },
  { path: '/services', label: 'Local Services', icon: '🚐', section: 'Operations' },
  { path: '/reviews', label: 'Reviews', icon: '⭐', section: 'Operations' },
  { path: '/ai', label: 'AI Tools', icon: '🤖', section: 'Intelligence' },
];

export default function App() {
  const [lang, setLang] = useState<'en' | 'es'>('en');
  let lastSection = '';

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">
          RetiroFlow
          <small>{lang === 'en' ? 'Oaxaca Wellness Retreats' : 'Retiros de Bienestar Oaxaca'}</small>
        </div>
        <nav>
          {navItems.map((item) => {
            const showSection = item.section !== lastSection;
            lastSection = item.section;
            return (
              <div key={item.path}>
                {showSection && <div className="nav-section">{item.section}</div>}
                <NavLink to={item.path} end={item.path === '/'} className={({ isActive }) => isActive ? 'active' : ''}>
                  <span>{item.icon}</span> {item.label}
                </NavLink>
              </div>
            );
          })}
        </nav>
        <div className="sidebar-footer">
          <div className="lang-toggle">
            <button className={lang === 'en' ? 'active' : ''} onClick={() => setLang('en')}>EN</button>
            <button className={lang === 'es' ? 'active' : ''} onClick={() => setLang('es')}>ES</button>
          </div>
          <div style={{ marginTop: 8 }}>RetiroFlow v0.1.0</div>
        </div>
      </aside>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard lang={lang} />} />
          <Route path="/centers" element={<Centers lang={lang} />} />
          <Route path="/retreats" element={<Retreats lang={lang} />} />
          <Route path="/participants" element={<Participants lang={lang} />} />
          <Route path="/facilitators" element={<Facilitators lang={lang} />} />
          <Route path="/bookings" element={<Bookings lang={lang} />} />
          <Route path="/services" element={<Services lang={lang} />} />
          <Route path="/reviews" element={<Reviews lang={lang} />} />
          <Route path="/ai" element={<AITools lang={lang} />} />
        </Routes>
      </main>
    </div>
  );
}
