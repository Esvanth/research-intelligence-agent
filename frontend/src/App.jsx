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
  { id: 'search',    name: 'Search Agent',    icon: '🔍', desc: 'Discovers relevant sources',          keyword: 'Search'    },
  { id: 'reader',    name: 'Reader Agent',    icon: '📖', desc: 'Extracts key information',            keyword: 'Reader'    },
  { id: 'factcheck', name: 'Fact-Check Agent',icon: '🔎', desc: 'Cross-references & flags conflicts',  keyword: 'Fact'      },
  { id: 'synthesis', name: 'Synthesis Agent', icon: '📝', desc: 'Builds confidence-scored report',     keyword: 'Synthesis' },
]

function agentState(steps, keyword) {
  if (steps.some(s => s.includes('✅') && s.includes(keyword))) return 'done'
  if (steps.some(s => !s.includes('✅') && s.includes(keyword))) return 'running'
  return 'idle'
}

// ── Header ────────────────────────────────────────────────────────────────────
function Header() {
  return (
    <header className="header">
      <div className="header-glow" />
      <div className="header-inner">
        <div className="brand">
          <div className="brand-logo"><span>🧠</span></div>
          <div>
            <div className="brand-name">Research Intelligence</div>
            <div className="brand-sub">Multi-Agent · Azure Foundry IQ · Agents League 2026</div>
          </div>
        </div>
        <div className="header-tags">
          <span className="tag tag-blue">Foundry IQ</span>
          <span className="tag tag-purple">Reasoning Agents</span>
          <span className="tag tag-teal">5 Agents</span>
        </div>
      </div>
    </header>
  )
}

// ── Search ────────────────────────────────────────────────────────────────────
function SearchPanel({ onSubmit, loading }) {
  const [query, setQuery]     = useState('')
  const [phIdx, setPhIdx]     = useState(0)
  const inputRef              = useRef()

  useEffect(() => {
    const id = setInterval(() => setPhIdx(i => (i + 1) % EXAMPLES.length), 3500)
    return () => clearInterval(id)
  }, [])

  const submit = () => { if (query.trim() && !loading) onSubmit(query.trim()) }

  return (
    <section className="search-section">
      <div className="search-hero">
        <h2 className="search-title">
          Ask anything. Get <span className="gradient-text">verified answers</span>.
        </h2>
        <p className="search-desc">
          5 specialised AI agents search, read, fact-check, and synthesise
          a confidence-scored research report — in seconds.
        </p>
      </div>

      <div className="search-box">
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
        <button className="search-btn" onClick={submit} disabled={loading || !query.trim()}>
          {loading ? <span className="spin" /> : '→'}
        </button>
      </div>

      <div className="example-row">
        <span className="example-label">Try:</span>
        {EXAMPLES.map(ex => (
          <button
            key={ex}
            className="example-pill"
            onClick={() => { setQuery(ex); inputRef.current?.focus() }}
            disabled={loading}
          >{ex}</button>
        ))}
      </div>
    </section>
  )
}

// ── How It Works (idle state) ─────────────────────────────────────────────────
function HowItWorks() {
  return (
    <div className="how-grid">
      {AGENTS.map((a, i) => (
        <div key={a.id} className="how-card">
          <div className="how-step">Step {i + 1}</div>
          <div className="how-icon">{a.icon}</div>
          <h4>{a.name}</h4>
          <p>{a.desc}</p>
        </div>
      ))}
    </div>
  )
}

// ── Agent Pipeline (running / done) ───────────────────────────────────────────
function AgentPipeline({ steps, status }) {
  const consoleRef = useRef()

  useEffect(() => {
    if (consoleRef.current) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight
    }
  }, [steps])

  return (
    <div className="pipeline-wrap">
      <div className="pipeline-nodes">
        {AGENTS.map((a, i) => {
          const state = agentState(steps, a.keyword)
          return (
            <div key={a.id} className="pipeline-item">
              <div className={`agent-node ${state}`}>
                <div className="node-icon">
                  {state === 'running' ? <span className="spin" /> : state === 'done' ? '✓' : a.icon}
                </div>
                <div className="node-label">{a.name}</div>
                <div className="node-desc">{a.desc}</div>
              </div>
              {i < AGENTS.length - 1 && (
                <div className={`node-connector ${state === 'done' ? 'active' : ''}`}>
                  <div className="connector-line" />
                </div>
              )}
            </div>
          )
        })}
      </div>

      <div className="console">
        <div className="console-bar">
          <span className="console-dot red" />
          <span className="console-dot yellow" />
          <span className="console-dot green" />
          <span className="console-title">live agent output</span>
        </div>
        <div className="console-body" ref={consoleRef}>
          {steps.length === 0
            ? <span className="console-line muted">Initialising agents...</span>
            : steps.map((s, i) => (
              <div key={i} className="console-line">
                <span className="console-prompt">›</span>
                <span>{s.replace(/^[^\s]+\s/, '')}</span>
              </div>
            ))
          }
          {status === 'running' && (
            <div className="console-line muted">
              <span className="console-prompt">›</span>
              <span className="console-cursor" />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ── Report ────────────────────────────────────────────────────────────────────
function ReportViewer({ report, query }) {
  const copy = () => navigator.clipboard.writeText(report)
  const dl   = () => {
    const a = Object.assign(document.createElement('a'), {
      href:     URL.createObjectURL(new Blob([report], { type: 'text/markdown' })),
      download: `research-${Date.now()}.md`,
    })
    a.click()
  }

  return (
    <div className="report-wrap">
      <div className="report-top">
        <div>
          <div className="report-title">Research Report</div>
          <div className="report-query">"{query}"</div>
        </div>
        <div className="report-btns">
          <button className="btn-ghost" onClick={copy}>Copy</button>
          <button className="btn-ghost" onClick={dl}>Download .md</button>
        </div>
      </div>
      <div className="report-body">
        <ReactMarkdown>{report}</ReactMarkdown>
      </div>
    </div>
  )
}

// ── App ───────────────────────────────────────────────────────────────────────
export default function App() {
  const [phase, setPhase]   = useState('idle')
  const [steps, setSteps]   = useState([])
  const [report, setReport] = useState('')
  const [query, setQuery]   = useState('')
  const [error, setError]   = useState('')
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
        if (job.status === 'done')  { stop(); setReport(job.report); setPhase('done') }
        if (job.status === 'error') { stop(); setError(job.error || 'Unknown error'); setPhase('error') }
      }, 2000)
    } catch (e) {
      setError(e.message)
      setPhase('error')
    }
  }

  const reset = () => { stop(); setPhase('idle'); setSteps([]); setReport(''); setQuery(''); setError('') }

  useEffect(() => () => stop(), [])

  return (
    <div className="app">
      <Header />
      <main className="main">
        <SearchPanel onSubmit={startResearch} loading={phase === 'running'} />

        {phase === 'idle' && <HowItWorks />}

        {(phase === 'running' || phase === 'done') && (
          <AgentPipeline steps={steps} status={phase} />
        )}

        {phase === 'error' && (
          <div className="error-card">
            <div className="error-icon">⚠</div>
            <h3>Something went wrong</h3>
            <p>{error}</p>
            <button className="btn-primary" onClick={reset}>Try Again</button>
          </div>
        )}

        {phase === 'done' && report && (
          <>
            <ReportViewer report={report} query={query} />
            <div className="center-btn">
              <button className="btn-ghost" onClick={reset}>Research another topic →</button>
            </div>
          </>
        )}
      </main>

      <footer className="footer">
        Agents League Hackathon 2026 · Reasoning Agents Track · Powered by Azure AI Foundry
      </footer>
    </div>
  )
}
