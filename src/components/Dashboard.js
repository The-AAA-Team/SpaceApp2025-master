import React, { useEffect, useState, useMemo } from 'react';
import './dashboard.css';

export default function Dashboard() {
  const [publications, setPublications] = useState([]);
  const [q, setQ] = useState('');
  const [topicFilter, setTopicFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch('/data')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => setPublications(Array.isArray(data) ? data : []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  // available topics for simple filtering (if sections/keywords exist)
  const topics = useMemo(() => {
    const s = new Set();
    publications.forEach((p) => {
      // attempt to pull keys from sections or from summary text
      if (p.sections && typeof p.sections === 'object') {
        Object.keys(p.sections).forEach((k) => s.add(k));
      }
    });
    return Array.from(s).sort();
  }, [publications]);

  const filtered = useMemo(() => {
    const qLower = q.trim().toLowerCase();
    return publications.filter((p) => {
      if (topicFilter) {
        const hasTopic = p.sections && p.sections[topicFilter];
        if (!hasTopic) return false;
      }
      if (!qLower) return true;
      const hay = `${p.title || ''} ${p.summary || ''} ${Object.values(p.sections || {}).join(' ')}`.toLowerCase();
      return hay.includes(qLower);
    });
  }, [publications, q, topicFilter]);

  const stats = useMemo(() => ({
    total: publications.length,
    shown: filtered.length,
  }), [publications, filtered]);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Publications</h1>
        <div className="controls">
          <input placeholder="Search titles, summaries, sections..." value={q} onChange={(e) => setQ(e.target.value)} />
          <select value={topicFilter} onChange={(e) => setTopicFilter(e.target.value)}>
            <option value="">All topics</option>
            {topics.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
        <div className="stats">Total: {stats.total} · Shown: {stats.shown}</div>
      </header>

      <main>
        {loading && <div className="info">Loading…</div>}
        {error && <div className="error">Error: {error}</div>}
        {!loading && !error && filtered.length === 0 && <div className="info">No publications found.</div>}

        <ul className="pub-list">
          {filtered.map((p) => (
            <li key={p.id || p.url} className="pub">
              <h2 className="pub-title">{p.title || 'Untitled'}</h2>
              {p.author && <div className="pub-author">by {p.author}</div>}
              <div className="pub-summary">{p.summary}</div>
              {p.sections && typeof p.sections === 'object' && (
                <details>
                  <summary>Sections</summary>
                  <div className="sections">
                    {Object.entries(p.sections).map(([k, v]) => (
                      <div key={k} className="section">
                        <strong>{k}</strong>
                        <p>{v}</p>
                      </div>
                    ))}
                  </div>
                </details>
              )}
              {p.url && <a className="pub-link" href={p.url} target="_blank" rel="noreferrer">Source</a>}
            </li>
          ))}
        </ul>
      </main>
    </div>
  );
}
