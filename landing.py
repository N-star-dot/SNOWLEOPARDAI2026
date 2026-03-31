import streamlit as st
import time

# Page config
st.set_page_config(
    page_title="Asteralyze* | AI-Powered Data Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ============================================
# NAVBAR
# ============================================
def render_navbar():
    st.markdown("""
    <nav class="navbar">
        <div class="nav-content">
            <a href="#" class="logo">
                <div class="logo-icon">
                    <div class="logo-dot"></div>
                </div>
                <span class="logo-text">Asteralyze<span class="logo-accent">*</span></span>
            </a>
            <div class="nav-links">
                <a href="#features" class="nav-link">Features</a>
                <a href="#personas" class="nav-link">Personas</a>
                <a href="#formats" class="nav-link">File Support</a>
                <a href="#technology" class="nav-link">Technology</a>
            </div>
            <div class="nav-cta">
                <a href="#" class="btn-ghost">Documentation</a>
                <a href="#" class="btn-primary">Get Started</a>
            </div>
        </div>
    </nav>
    """, unsafe_allow_html=True)

# ============================================
# HERO SECTION
# ============================================
def render_hero():
    st.markdown("""
    <section class="hero">
        <div class="hero-grid">
            <div class="hero-content">
                <div class="badge">
                    <svg class="badge-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 3l1.912 5.813a2 2 0 001.272 1.272L21 12l-5.813 1.912a2 2 0 00-1.272 1.272L12 21l-1.912-5.813a2 2 0 00-1.272-1.272L3 12l5.813-1.912a2 2 0 001.272-1.272L12 3z"/>
                    </svg>
                    <span>Powered by Groq Llama 3.3</span>
                </div>

                <h1 class="hero-title">
                    <span class="title-white">Talk to your data.</span><br>
                    <span class="title-glow">No code required.</span>
                </h1>

                <p class="hero-description">
                    Asteralyze* is an AI-powered data intelligence platform that lets researchers,
                    analysts, and business owners have natural language conversations with any dataset.
                </p>

                <div class="hero-buttons">
                    <a href="#" class="btn-primary btn-lg">
                        Start Analyzing
                        <svg class="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M5 12h14M12 5l7 7-7 7"/>
                        </svg>
                    </a>
                    <a href="#" class="btn-outline btn-lg">Watch Demo</a>
                </div>

                <div class="hero-stats">
                    <div class="stat">
                        <div class="stat-value stat-primary">10+</div>
                        <div class="stat-label">File formats</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value stat-accent">5</div>
                        <div class="stat-label">AI personas</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">99.9%</div>
                        <div class="stat-label">Query accuracy</div>
                    </div>
                </div>
            </div>

            <div class="hero-terminal-wrapper">
                <div class="terminal-glow"></div>
                <div class="terminal">
                    <div class="terminal-header">
                        <div class="terminal-dots">
                            <span class="dot dot-red"></span>
                            <span class="dot dot-yellow"></span>
                            <span class="dot dot-green"></span>
                        </div>
                        <span class="terminal-title">asteralyze — data intelligence</span>
                    </div>
                    <div class="terminal-body">
                        <div class="terminal-line system">
                            <svg class="line-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                                <path d="M14 2v6h6M8 13h8M8 17h8M8 9h2"/>
                            </svg>
                            <span>Dataset loaded: Q4_sales_data.csv</span>
                        </div>
                        <div class="terminal-line user">
                            <svg class="line-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
                            </svg>
                            <span>What were our top 3 performing products last quarter?</span>
                        </div>
                        <div class="terminal-line ai">
                            <svg class="line-icon sparkle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 3l1.912 5.813a2 2 0 001.272 1.272L21 12l-5.813 1.912a2 2 0 00-1.272 1.272L12 21l-1.912-5.813a2 2 0 00-1.272-1.272L3 12l5.813-1.912a2 2 0 001.272-1.272L12 3z"/>
                            </svg>
                            <span>Analyzing 12,847 transactions...</span>
                        </div>
                        <div class="terminal-line ai-response">
                            <svg class="line-icon sparkle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 3l1.912 5.813a2 2 0 001.272 1.272L21 12l-5.813 1.912a2 2 0 00-1.272 1.272L12 21l-1.912-5.813a2 2 0 00-1.272-1.272L3 12l5.813-1.912a2 2 0 001.272-1.272L12 3z"/>
                            </svg>
                            <div class="response-content">
                                Based on Q4 revenue:<br><br>
                                1. <strong>Enterprise Suite</strong> — $2.4M (+34% YoY)<br>
                                2. <strong>Pro Analytics</strong> — $1.8M (+28% YoY)<br>
                                3. <strong>Team Starter</strong> — $890K (+45% YoY)<br><br>
                                <span class="response-note">Notably, Team Starter showed the highest growth rate, suggesting strong demand in the SMB segment.</span>
                            </div>
                        </div>
                        <div class="terminal-cursor">
                            <span class="cursor-prompt">›</span>
                            <span class="cursor-blink"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)

# ============================================
# FEATURES SECTION
# ============================================
def render_features():
    st.markdown("""
    <section id="features" class="section">
        <div class="section-bg-gradient"></div>
        <div class="section-header">
            <p class="section-label">Core Capabilities</p>
            <h2 class="section-title">Your data, finally understood</h2>
            <p class="section-description">
                Built on Snow Leopard AI's live query engine, Asteralyze* brings enterprise-grade data intelligence to everyone.
            </p>
        </div>

        <div class="features-grid">
            <div class="feature-card feature-highlight">
                <div class="feature-icon feature-icon-highlight">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2a10 10 0 1010 10A10 10 0 0012 2zM12 8v4l3 3"/>
                        <circle cx="12" cy="12" r="3"/>
                    </svg>
                </div>
                <h3 class="feature-title">Intelligent Query Routing</h3>
                <p class="feature-description">Automatically routes questions to remote databases, local datasets, image/video analysis, or direct response — all via natural language.</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/>
                    </svg>
                </div>
                <h3 class="feature-title">Self-Healing SQL</h3>
                <p class="feature-description">Our engine automatically detects and repairs broken queries in real-time, ensuring you always get accurate results.</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
                    </svg>
                </div>
                <h3 class="feature-title">Streaming Synthesis</h3>
                <p class="feature-description">Watch raw database results transform into actionable insights as the AI synthesizes information in real-time.</p>
            </div>

            <div class="feature-card feature-highlight">
                <div class="feature-icon feature-icon-highlight">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
                    </svg>
                </div>
                <h3 class="feature-title">Proactive EDA Briefings</h3>
                <p class="feature-description">Upload a dataset and receive immediate observations, anomaly alerts, and suggested questions to explore.</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                    </svg>
                </div>
                <h3 class="feature-title">Multi-Modal Analysis</h3>
                <p class="feature-description">Analyze images, videos, documents, and structured data — all through the same conversational interface.</p>
            </div>

            <div class="feature-card">
                <div class="feature-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                    </svg>
                </div>
                <h3 class="feature-title">Lightning Fast</h3>
                <p class="feature-description">Powered by Groq's Llama 3.3 for near-instant responses, even on complex analytical queries.</p>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)

# ============================================
# PERSONA SYSTEM SECTION
# ============================================
def render_personas():
    st.markdown('<section id="personas" class="section">', unsafe_allow_html=True)
    st.markdown("""
        <div class="section-header">
            <p class="section-label section-label-accent">Dynamic Persona System</p>
            <h2 class="section-title">An AI that adapts to your context</h2>
            <p class="section-description">
                Upload your data and watch the agent automatically shift its voice, expertise, and approach based on what it discovers.
            </p>
        </div>
    """, unsafe_allow_html=True)

    personas = {
        "Patient Tutor": {
            "trigger": "Lecture notes, study materials",
            "description": "Explains concepts step-by-step, asks clarifying questions, and adapts to your learning pace.",
            "example": "Can you walk me through how linear regression works using my class notes?",
            "icon": "graduation-cap",
            "color": "primary"
        },
        "Strategic Consultant": {
            "trigger": "Sales data, business metrics",
            "description": "Focuses on actionable insights, competitive positioning, and revenue opportunities.",
            "example": "Which customer segments should we prioritize for Q2 based on LTV trends?",
            "icon": "trending-up",
            "color": "accent"
        },
        "Research Lens": {
            "trigger": "Research datasets, academic papers",
            "description": "Becomes an opinionated analyst that filters, connects, and frames data to support your thesis.",
            "example": "Find correlations that support my hypothesis about urban density and pollution.",
            "icon": "microscope",
            "color": "primary"
        },
        "Data Journalist": {
            "trigger": "Public records, survey data",
            "description": "Surfaces stories in the data, identifies outliers, and helps craft compelling narratives.",
            "example": "What's the most surprising trend in this census data that readers would care about?",
            "icon": "newspaper",
            "color": "accent"
        },
        "Business Analyst": {
            "trigger": "Operations data, KPIs",
            "description": "Tracks metrics against goals, identifies bottlenecks, and suggests process improvements.",
            "example": "Why did our fulfillment rate drop 12% last month and what can we do about it?",
            "icon": "building",
            "color": "primary"
        }
    }

    col1, col2 = st.columns([2, 3], gap="large")

    with col1:
        selected_persona = st.radio(
            "Select a persona",
            list(personas.keys()),
            label_visibility="collapsed"
        )

    with col2:
        persona = personas[selected_persona]
        color_class = "persona-card-primary" if persona["color"] == "primary" else "persona-card-accent"
        icon_html = get_persona_icon(persona["icon"])
        st.markdown(f"""
        <div class="persona-detail {color_class}">
            <div class="persona-header">
                <div class="persona-icon">{icon_html}</div>
                <div>
                    <h3 class="persona-name">{selected_persona}</h3>
                    <p class="persona-trigger">Activated by: {persona["trigger"]}</p>
                </div>
            </div>
            <p class="persona-description">{persona["description"]}</p>
            <div class="persona-example">
                <p class="example-label">EXAMPLE QUERY</p>
                <p class="example-text">"{persona["example"]}"</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</section>', unsafe_allow_html=True)


def get_persona_icon(icon_name):
    icons = {
        "graduation-cap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
        "trending-up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
        "microscope": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 100-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 01-2-2V6h6v4a2 2 0 01-2 2z"/><path d="M12 6V3a1 1 0 00-1-1H9a1 1 0 00-1 1v3"/></svg>',
        "newspaper": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h16a2 2 0 002-2V4a2 2 0 00-2-2H8a2 2 0 00-2 2v16a2 2 0 01-2 2zm0 0a2 2 0 01-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-8"/><path d="M15 18h-5"/><path d="M10 6h8v4h-8z"/></svg>',
        "building": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/></svg>'
    }
    return icons.get(icon_name, '')

# ============================================
# FILE SUPPORT SECTION
# ============================================
def render_file_support():
    st.markdown("""
    <section id="formats" class="section">
        <div class="section-bg-gradient-accent"></div>
        <div class="section-header">
            <p class="section-label section-label-accent">Universal File Support</p>
            <h2 class="section-title">The first data analyst for every file type</h2>
            <p class="section-description">
                From spreadsheets to videos, Asteralyze* works with virtually any file a researcher or professional might have.
            </p>
        </div>

        <div class="file-grid">
            <div class="file-card">
                <div class="file-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                        <path d="M14 2v6h6M8 13h8M8 17h8M8 9h2"/>
                    </svg>
                </div>
                <span class="file-status"></span>
                <h4 class="file-name">CSV</h4>
                <p class="file-desc">Spreadsheets &amp; tabular data</p>
            </div>

            <div class="file-card">
                <div class="file-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                        <path d="M14 2v6h6"/>
                        <path d="M8 16l2-2 2 2M12 14l2 2 2-2"/>
                    </svg>
                </div>
                <span class="file-status"></span>
                <h4 class="file-name">JSON</h4>
                <p class="file-desc">Structured data &amp; APIs</p>
            </div>

            <div class="file-card">
                <div class="file-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                        <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>
                    </svg>
                </div>
                <span class="file-status"></span>
                <h4 class="file-name">PDF</h4>
                <p class="file-desc">Reports &amp; documents</p>
            </div>

            <div class="file-card">
                <div class="file-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="2" y="3" width="20" height="14" rx="2"/>
                        <path d="M8 21h8M12 17v4"/>
                    </svg>
                </div>
                <span class="file-status"></span>
                <h4 class="file-name">PPTX</h4>
                <p class="file-desc">Presentations</p>
            </div>

            <div class="file-card">
                <div class="file-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                        <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>
                    </svg>
                </div>
                <span class="file-status"></span>
                <h4 class="file-name">DOCX</h4>
                <p class="file-desc">Word documents</p>
            </div>

            <div class="file-card">
                <div class="file-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2"/>
                        <circle cx="8.5" cy="8.5" r="1.5"/>
                        <path d="M21 15l-5-5L5 21"/>
                    </svg>
                </div>
                <span class="file-status"></span>
                <h4 class="file-name">Images</h4>
                <p class="file-desc">JPG, PNG, WebP</p>
            </div>

            <div class="file-card">
                <div class="file-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="2" y="2" width="20" height="20" rx="2.18"/>
                        <path d="M10 8l6 4-6 4V8z"/>
                    </svg>
                </div>
                <span class="file-status"></span>
                <h4 class="file-name">Video</h4>
                <p class="file-desc">MP4, MOV, WebM</p>
            </div>
        </div>

        <p class="file-footer">
            <strong>Drag and drop</strong> or upload via URL — analysis begins instantly
        </p>
    </section>
    """, unsafe_allow_html=True)

# ============================================
# TECH STACK SECTION
# ============================================
def render_tech_stack():
    st.markdown("""
    <section id="technology" class="section">
        <div class="section-header">
            <p class="section-label">Technology</p>
            <h2 class="section-title">Built on cutting-edge infrastructure</h2>
            <p class="section-description">
                Enterprise-grade performance meets developer-friendly design.
            </p>
        </div>

        <div class="tech-grid">
            <div class="tech-card tech-card-primary">
                <div class="tech-glow tech-glow-primary"></div>
                <div class="tech-content">
                    <div class="tech-header">
                        <div class="tech-icon tech-icon-primary">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                            </svg>
                        </div>
                        <div>
                            <h3 class="tech-name">Snow Leopard AI</h3>
                            <p class="tech-type">Live Query Engine</p>
                        </div>
                    </div>
                    <p class="tech-description">
                        Intelligent query routing that seamlessly connects to remote cloud databases, local datasets, and multi-modal inputs through a unified interface.
                    </p>
                </div>
            </div>

            <div class="tech-card tech-card-accent">
                <div class="tech-glow tech-glow-accent"></div>
                <div class="tech-content">
                    <div class="tech-header">
                        <div class="tech-icon tech-icon-accent">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                            </svg>
                        </div>
                        <div>
                            <h3 class="tech-name">Groq Llama 3.3</h3>
                            <p class="tech-type">Inference Engine</p>
                        </div>
                    </div>
                    <p class="tech-description">
                        Near-instant responses powered by Groq's LPU architecture, delivering enterprise-scale performance with minimal latency.
                    </p>
                </div>
            </div>
        </div>

        <div class="architecture">
            <div class="arch-flow">
                <div class="arch-node">
                    <span class="arch-dot arch-dot-default"></span>
                    <span>User Query</span>
                </div>
                <span class="arch-arrow">→</span>
                <div class="arch-node arch-node-primary">
                    <span class="arch-dot arch-dot-primary"></span>
                    <span>Intelligent Router</span>
                </div>
                <span class="arch-arrow">→</span>
                <div class="arch-targets">
                    <span class="arch-target">Remote DB</span>
                    <span class="arch-target">Local Data</span>
                    <span class="arch-target">Multi-Modal</span>
                </div>
                <span class="arch-arrow">→</span>
                <div class="arch-node arch-node-accent">
                    <span class="arch-dot arch-dot-accent"></span>
                    <span>Synthesis</span>
                </div>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)

# ============================================
# CTA SECTION
# ============================================
def render_cta():
    st.markdown("""
    <section class="cta-section">
        <div class="cta-bg"></div>
        <div class="cta-glow"></div>
        <div class="cta-content">
            <h2 class="cta-title">Ready to talk to your data?</h2>
            <p class="cta-description">
                Join researchers, analysts, and business owners who are already having conversations with their data — no SQL, no Python, no barriers.
            </p>
            <div class="cta-buttons">
                <a href="#" class="btn-primary btn-lg">
                    Start Free Trial
                    <svg class="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M5 12h14M12 5l7 7-7 7"/>
                    </svg>
                </a>
                <a href="#" class="btn-outline btn-lg">Schedule Demo</a>
            </div>
            <p class="cta-note">No credit card required • 14-day free trial • Cancel anytime</p>
        </div>
    </section>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
def render_footer():
    st.markdown("""
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="#" class="logo">
                        <div class="logo-icon logo-icon-sm">
                            <div class="logo-dot logo-dot-sm"></div>
                        </div>
                        <span class="logo-text logo-text-sm">Asteralyze<span class="logo-accent">*</span></span>
                    </a>
                    <p class="footer-tagline">AI-powered data intelligence for everyone.</p>
                </div>

                <div class="footer-links">
                    <h4>Product</h4>
                    <a href="#features">Features</a>
                    <a href="#personas">Personas</a>
                    <a href="#formats">File Support</a>
                    <a href="#">Pricing</a>
                </div>

                <div class="footer-links">
                    <h4>Resources</h4>
                    <a href="#">Documentation</a>
                    <a href="#">API Reference</a>
                    <a href="#">Tutorials</a>
                    <a href="#">Blog</a>
                </div>

                <div class="footer-links">
                    <h4>Company</h4>
                    <a href="#">About</a>
                    <a href="#">Careers</a>
                    <a href="#">Contact</a>
                    <a href="#">Press Kit</a>
                </div>

                <div class="footer-links">
                    <h4>Legal</h4>
                    <a href="#">Privacy</a>
                    <a href="#">Terms</a>
                    <a href="#">Security</a>
                </div>
            </div>

            <div class="footer-bottom">
                <p>© 2026 Asteralyze. All rights reserved.</p>
                <div class="footer-socials">
                    <a href="#" aria-label="Twitter">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                        </svg>
                    </a>
                    <a href="#" aria-label="GitHub">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"/>
                        </svg>
                    </a>
                    <a href="#" aria-label="LinkedIn">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
    </footer>
    """, unsafe_allow_html=True)


# ============================================
# MAIN APP
# ============================================
def main():
    # HUD Grid Background + Scan Line
    st.markdown("""
    <div class="hud-grid"></div>
    <div class="scan-line"></div>
    """, unsafe_allow_html=True)

    render_navbar()
    render_hero()
    render_features()
    render_personas()
    render_file_support()
    render_tech_stack()
    render_cta()
    render_footer()

if __name__ == "__main__":
    main()
