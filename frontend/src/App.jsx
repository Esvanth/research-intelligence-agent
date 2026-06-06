import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

const API = '/api'

const EXAMPLES = [
  'Is intermittent fasting effective for weight loss?',
  'Does AI cause job losses?',
  'Is coffee good or bad for health?',
  'Are electric vehicles better for the environment?',
]

const AGENTS = [
  { id: 'search',    name: 'Search Agent',     keyword: 'Search',    desc: 'Discovers relevant sources' },
  { id: 'reader',    name: 'Reader Agent',     keyword: 'Reader',    desc: 'Extracts key information'   },
  { id: 'factcheck', name: 'Fact-Check Agent', keyword: 'Fact',      desc: 'Cross-references sources'   },
  { id: 'synthesis', name: 'Synthesis Agent',  keyword: 'Synthesis', desc: 'Writes the final report'    },
]

function agentState(steps, keyword) {
  if (steps.some(s => s.includes('✅') && s.includes(keyword))) return 'done'
  if (steps.some(s => !s.includes('✅') && s.includes(keyword))) return 'active'
  return 'idle'
}

function agentDetail(steps, keyword) {
  const done = steps.find(s => s.includes('✅') && s.includes(keyword))
  if (done) return done.replace(/✅\s*/,'').replace(/\w+ Agent:\s*/,'').trim()
  const active = steps.find(s => !s.includes('✅') && s.includes(keyword))
  if (active) return active.replace(/[🔍📖🔎📝]\s*/,'').replace(/\w+ Agent:\s*/,'').trim()
  return null
}

// ── Header ─────────────────────────────────────────────────────────────────────
function Header() {
  return (
    <header className="header">
      <div className="header-inner">
        <a className="brand" href="/">
          <div className="brand-mark">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="2.5" fill="currentColor"/>
              <circle cx="3"  cy="3"  r="1.5" fill="currentColor" opacity="0.5"/>
              <circle cx="17" cy="3"  r="1.5" fill="currentColor" opacity="0.5"/>
              <circle cx="3"  cy="17" r="1.5" fill="currentColor" opacity="0.5"/>
              <circle cx="17" cy="17" r="1.5" fill="currentColor" opacity="0.5"/>
              <line x1="10" y1="10" x2="3"  y2="3"  stroke="currentColor" strokeWidth="1" opacity="0.35"/>
              <line x1="10" y1="10" x2="17" y2="3"  stroke="currentColor" strokeWidth="1" opacity="0.35"/>
              <line x1="10" y1="10" x2="3"  y2="17" stroke="currentColor" strokeWidth="1" opacity="0.35"/>
              <line x1="10" y1="10" x2="17" y2="17" stroke="currentColor" strokeWidth="1" opacity="0.35"/>
            </svg>
          </div>
          <span className="brand-name">Research Intelligence</span>
        </a>

        <div className="header-right">
          <span className="header-badge">Foundry IQ</span>
          <span className="header-badge">Agents League 2026</span>
        </div>
      </div>
    </header>
  )
}

// ── Search ─────────────────────────────────────────────────────────────────────
function Search({ onSubmit, loading }) {
  const [query, setQuery] = useState('')
  const [phIdx, setPhIdx] = useState(0)
  const inputRef          = useRef()

  useEffect(() => {
    const t = setInterval(() => setPhIdx(i => (i + 1) % EXAMPLES.length), 3200)
    return () => clearInterval(t)
  }, [])

  const submit = () => { if (query.trim() && !loading) onSubmit(query.trim()) }

  return (
    <section className="search-wrap">
      <div className="search-hero">
        <h1 className="search-heading">
          What do you want to research?
        </h1>
        <p className="search-sub">
          4 AI agents work together to search the web, read sources,
          fact-check claims, and write you a verified research report.
        </p>
      </div>

      <div className={`search-field ${loading ? 'disabled' : ''}`}>
        <svg className="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none">
          <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2"/>
          <path d="M16.5 16.5L21 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
        </svg>
        <input
          ref={inputRef}
          className="search-input"
          type="text"
          placeholder={EXAMPLES[phIdx]}
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && submit()}
          disabled={loading}
          autoFocus
        />
        <button
          className="search-submit"
          onClick={submit}
          disabled={loading || !query.trim()}
          aria-label="Search"
        >
          {loading
            ? <span className="spinner" />
            : <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
          }
        </button>
      </div>

      <div className="suggestions">
        <span className="suggestions-label">Try asking</span>
        {EXAMPLES.map(ex => (
          <button
            key={ex}
            className="suggestion"
            disabled={loading}
            onClick={() => { setQuery(ex); inputRef.current?.focus() }}
          >
            {ex}
          </button>
        ))}
      </div>
    </section>
  )
}

// ── Features (idle state) ──────────────────────────────────────────────────────
function Features() {
  const items = [
    { n: '01', title: 'Smart Search',     body: 'Searches the web and ranks sources by relevance to your question.' },
    { n: '02', title: 'Deep Reading',     body: 'Opens and reads each source, pulling out the facts that matter.' },
    { n: '03', title: 'Fact Checking',    body: 'Cross-references sources, finds agreements and contradictions.' },
    { n: '04', title: 'Verified Report',  body: 'Synthesises everything into a confidence-scored, cited report.' },
  ]
  return (
    <div className="features">
      <p className="features-label">How it works</p>
      <div className="features-grid">
        {items.map(it => (
          <div key={it.n} className="feature-card">
            <span className="feature-num">{it.n}</span>
            <h3 className="feature-title">{it.title}</h3>
            <p className="feature-body">{it.body}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Research Progress ──────────────────────────────────────────────────────────
function Progress({ query, steps, status }) {
  return (
    <div className="progress-wrap">
      <div className="progress-header">
        <div className="progress-label">
          {status === 'running' ? 'Researching' : 'Researched'}
        </div>
        <div className="progress-query">"{query}"</div>
      </div>

      <div className="progress-steps">
        {AGENTS.map((agent, i) => {
          const state  = agentState(steps, agent.keyword)
          const detail = agentDetail(steps, agent.keyword)

          return (
            <div key={agent.id} className={`step ${state}`}>
              <div className="step-indicator">
                {state === 'done'
                  ? <svg className="step-check" width="13" height="13" viewBox="0 0 14 14" fill="none">
                      <path d="M2.5 7l3.5 3.5 5.5-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  : state === 'active'
                  ? <span className="step-spinner" />
                  : <span className="step-dot" />
                }
              </div>
              <div className="step-content">
                <span className="step-name">{agent.name}</span>
                {detail && <span className="step-detail">{detail}</span>}
                {!detail && state === 'idle' && (
                  <span className="step-waiting">{agent.desc}</span>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {status === 'running' && (
        <div className="progress-note">
          This usually takes 30–60 seconds
        </div>
      )}
    </div>
  )
}

// ── Report ─────────────────────────────────────────────────────────────────────
function Report({ report, query, onReset }) {
  const [copied,       setCopied]       = useState(false)
  const [downloading,  setDownloading]  = useState(false)
  const reportRef = useRef()

  const copy = async () => {
    await navigator.clipboard.writeText(report)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const downloadPdf = async () => {
    if (!reportRef.current || downloading) return
    setDownloading(true)
    const el = reportRef.current
    try {
      const html2pdf = (await import('html2pdf.js')).default
      const slug = query.slice(0, 50).replace(/[^a-z0-9]+/gi, '-').toLowerCase()

      // Switch to PDF-friendly light styles
      el.classList.add('pdf-rendering')
      el.style.maxHeight = 'none'
      el.style.overflow  = 'visible'

      await html2pdf()
        .set({
          margin:      [14, 14, 14, 14],
          filename:    `research-${slug}.pdf`,
          html2canvas: { scale: 2, useCORS: true, backgroundColor: '#ffffff', logging: false },
          jsPDF:       { unit: 'mm', format: 'a4', orientation: 'portrait' },
          pagebreak:   { mode: ['avoid-all', 'css', 'legacy'] },
        })
        .from(el)
        .save()
    } catch (e) {
      console.error('PDF export failed:', e)
    } finally {
      // Restore dark styles
      el.classList.remove('pdf-rendering')
      el.style.maxHeight = ''
      el.style.overflow  = ''
      setDownloading(false)
    }
  }

  return (
    <div className="report-wrap">
      <div className="report-header">
        <div className="report-header-left">
          <div className="report-done-badge">
            <svg width="12" height="12" viewBox="0 0 14 14" fill="none">
              <path d="M2.5 7l3.5 3.5 5.5-6" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Done
          </div>
          <span className="report-header-query">"{query}"</span>
        </div>
        <div className="report-actions">
          <button className="action-btn" onClick={copy}>
            {copied ? 'Copied!' : 'Copy'}
          </button>
          <button className="action-btn" onClick={downloadPdf} disabled={downloading}>
            {downloading ? 'Saving…' : 'Download PDF'}
          </button>
          <button className="action-btn action-btn-subtle" onClick={onReset}>
            New research
          </button>
        </div>
      </div>

      <div className="report-divider" />

      <div className="report-body" ref={reportRef}>
        <div className="pdf-header">
          <div className="pdf-title">Research Intelligence Report</div>
          <div className="pdf-query">{query}</div>
          <div className="pdf-meta">Generated by Research Intelligence Agent · Azure AI Foundry IQ</div>
        </div>
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
    </div>
  )
}

// ── App ────────────────────────────────────────────────────────────────────────
export default function App() {
  const [phase,  setPhase]  = useState('idle')
  const [steps,  setSteps]  = useState([])
  const [report, setReport] = useState('')
  const [query,  setQuery]  = useState('')
  const [error,  setError]  = useState('')
  const pollRef             = useRef(null)

  const stop = () => { if (pollRef.current) clearInterval(pollRef.current) }

  const startResearch = async (q) => {
    setQuery(q); setPhase('running'); setSteps([]); setReport(''); setError('')
    try {
      const { job_id } = await fetch(`${API}/research`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ query: q }),
      }).then(r => r.json())

      pollRef.current = setInterval(async () => {
        const job = await fetch(`${API}/research/${job_id}`).then(r => r.json())
        setSteps(job.progress || [])
        if (job.status === 'done')  { stop(); setReport(job.report); setPhase('done')  }
        if (job.status === 'error') { stop(); setError(job.error  || 'Unknown error'); setPhase('error') }
      }, 2000)
    } catch (e) {
      setError(e.message); setPhase('error')
    }
  }

  const reset = () => {
    stop(); setPhase('idle'); setSteps([]); setReport(''); setQuery(''); setError('')
  }

  useEffect(() => () => stop(), [])

  return (
    <div className="app">
      <Header />

      <main className="main">
        <Search onSubmit={startResearch} loading={phase === 'running'} />

        {phase === 'idle' && <Features />}

        {(phase === 'running' || phase === 'done') && (
          <Progress query={query} steps={steps} status={phase} />
        )}

        {phase === 'error' && (
          <div className="error-box">
            <p className="error-title">Something went wrong</p>
            <p className="error-msg">{error}</p>
            <button className="btn-primary" onClick={reset}>Try again</button>
          </div>
        )}

        {phase === 'done' && report && (
          <Report report={report} query={query} onReset={reset} />
        )}
      </main>

      <footer className="footer">
        Built with Azure AI Foundry IQ · Tavily Search · Agents League Hackathon 2026
      </footer>
    </div>
  )
}
