"""
W-CERT Executive Summary Document Generator (Detailed Edition)
Generates in-depth Word (.docx) and PDF versions of the technical documentation.
"""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0, 102, 153)

def add_para(doc, text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(11)
    return p

def build_docx():
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    # Title
    title = doc.add_heading('W-CERT: Women-Centric Cyber Emergency Response & Threat-Analysis Framework', level=0)
    for run in title.runs:
        run.font.color.rgb = RGBColor(0, 51, 102)
    doc.add_paragraph('Detailed Executive Summary & Technical Architecture Documentation\nCapstone Project — April 2026\n')

    # 1. TECHNICAL STACK
    add_heading_styled(doc, '1. Technical Stack & Architecture', level=1)

    add_heading_styled(doc, '1.1 Frontend (Presentation Layer)', level=2)
    add_para(doc, '• Framework: React 18 built with Vite for optimized Hot Module Replacement (HMR) and fast production builds.')
    add_para(doc, '• Styling: Tailwind CSS configured with a custom dark-mode "Cyber" theme, utilizing deep blacks, vibrant neon accents (cyan, orange, red), and glassmorphism effects for a modern forensic look.')
    add_para(doc, '• Routing & State: React Router v6 handles client-side routing. Role-based Protected Routes prevent unauthorized access to Analyst/Admin dashboards.')
    add_para(doc, '• Data Visualization: Chart.js via react-chartjs-2. Implements Doughnut charts for severity distribution and Bar charts for attack type analysis based on real-time backend statistics.')
    add_para(doc, '• HTTP Client: Axios configured with global request/response interceptors to automatically attach JWT Bearer tokens and handle 401 Unauthorized expirations seamlessly.')

    add_heading_styled(doc, '1.2 Backend (Application & Logic Layer)', level=2)
    add_para(doc, '• Framework: Python Flask 3.0 configured with Flask-CORS for secure cross-origin requests from the Vercel frontend.')
    add_para(doc, '• Authentication: Flask-JWT-Extended handling both Access and Refresh tokens for session lifecycle management.')
    add_para(doc, '• AI & RAG Engine: Google Gemini 1.5 Flash (via google-genai SDK). Implements a multimodal Vision AI pipeline to cross-reference victim descriptions with uploaded evidentiary images (screenshots, PDFs). Also implements a lightweight Retrieval-Augmented Generation (RAG) system that injects similar historical cases into the AI prompt context.')
    add_para(doc, '• Production Server: Gunicorn 21.2 serving the WSGI application.')

    add_heading_styled(doc, '1.3 Database & Storage (Data Layer)', level=2)
    add_para(doc, '• Serverless Database: Google Sheets serves as a serverless NoSQL database via the gspread library and Google Service Accounts. A custom in-memory caching mechanism with a 60-second TTL prevents Google API rate limits (HTTP 429).')
    add_para(doc, '• Schema Breakdown:')
    add_para(doc, '    - Incidents: 23 columns storing encrypted PII, AI-generated reasoning, threat scores, IPC sections, and encrypted state locations for dynamic jurisdictional routing.')
    add_para(doc, '    - Users: Stores hashed passwords and Role-Based Access Control (RBAC) definitions.')
    add_para(doc, '    - Evidence_Metadata: Tracks file hashes, MIME types, storage paths, and uploader IDs.')
    add_para(doc, '    - Escalations: Maps incidents to target Indian State Cyber Crime authorities.')
    add_para(doc, '    - Audit_Log: An append-only ledger for all system interactions.')

    # 2. SECURITY
    add_heading_styled(doc, '2. Security, Hashing & Encryption', level=1)

    add_heading_styled(doc, '2.1 Encryption at Rest (AES-128-CBC)', level=2)
    add_para(doc, 'All Personally Identifiable Information (PII) — specifically victim names, contact details, and geolocation data — is encrypted before database insertion using the cryptography library\'s Fernet implementation (AES-128-CBC with HMAC-SHA256 authentication). The decryption key is injected strictly via environment variables.')

    add_heading_styled(doc, '2.2 Forensic SHA-256 Hashing', level=2)
    add_para(doc, 'To ensure legal admissibility, the platform implements forensic hashing:')
    add_para(doc, '• Content Hashing: Every incident description is hashed (SHA-256) at submission. Any subsequent tampering with the database record will trigger an integrity mismatch.')
    add_para(doc, '• Evidence Hashing: Uploaded files are hashed as raw bytes in memory (or chunked via 8192-byte blocks for large files). The hash serves as the immutable digital fingerprint of the evidence.')

    add_heading_styled(doc, '2.3 Chain of Custody & Audit Logging', level=2)
    add_para(doc, 'An append-only Chain of Custody ledger records every access to evidence (UPLOAD, VIEW, DOWNLOAD, VERIFY, INTEGRITY_CHECK). Simultaneously, an Audit Log tracks all system-level actions (LOGIN, STATUS_UPDATED, ESCALATION_CREATED, USER_ROLE_CHANGED). Both logs capture User ID, IP Address (including X-Forwarded-For proxy support), and exact timestamps.')

    add_heading_styled(doc, '2.4 Authentication & RBAC', level=2)
    add_para(doc, 'Passwords use Werkzeug\'s PBKDF2-HMAC-SHA256 hashing with random salting. Access is controlled via JWTs containing Role claims: USER (submit reports), ANALYST (triage/investigate), and ADMIN (full system access). The @role_required decorator enforces endpoint security.')

    # 3. LIBRARIES
    add_heading_styled(doc, '3. Key Libraries & Dependencies', level=1)

    table = doc.add_table(rows=1, cols=3, style='Table Grid')
    hdr = table.rows[0].cells
    hdr[0].text = 'Library'
    hdr[1].text = 'Version'
    hdr[2].text = 'Critical Purpose'

    libs = [
        ('Flask / Werkzeug', '3.0.x', 'REST API framework & PBKDF2 hashing'),
        ('Flask-JWT-Extended', '4.6.0', 'Access/Refresh Token lifecycle & RBAC'),
        ('gspread / oauth2client', '6.0.0', 'Google Sheets interaction and authentication'),
        ('cryptography', '41.0.7', 'Fernet AES encryption for PII protection'),
        ('google-generativeai', '0.8.0', 'Gemini 1.5 Flash Vision AI integration'),
        ('gunicorn', '21.2.0', 'Production WSGI serving on Render.com'),
        ('React / Vite', '18 / 5', 'Component-based UI and HMR build tooling'),
        ('Tailwind CSS', '3.x', 'Utility-first styling for cyber aesthetics'),
    ]
    for lib, ver, purpose in libs:
        row = table.add_row().cells
        row[0].text = lib
        row[1].text = ver
        row[2].text = purpose

    # 4. DEPLOYMENT
    add_heading_styled(doc, '4. Deployment Architecture', level=1)

    add_heading_styled(doc, '4.1 Frontend — Vercel (Edge Network)', level=2)
    add_para(doc, 'The frontend is hosted on Vercel, leveraging its global CDN and serverless edge architecture for sub-100ms load times. The application is built dynamically, picking up the production VITE_API_URL environment variable to communicate with the Render backend.')

    add_heading_styled(doc, '4.2 Backend — Render.com (Persistent Web Service)', level=2)
    add_para(doc, 'Crucially, the Flask backend is deployed on Render as a persistent web service rather than a serverless function. Serverless architectures (like AWS Lambda or Vercel Functions) terminate after each request, which would destroy the W-CERT in-memory Google Sheets cache and immediately trigger Google API Rate Limit bans (HTTP 429). Render keeps the process alive continuously, maintaining the cache and WebSocket connections.')

    add_heading_styled(doc, '4.3 Database Configurations', level=2)
    add_para(doc, 'Instead of uploading sensitive JSON credential files to servers, the Google Service Account JSON is injected securely as the SERVICE_ACCOUNT_JSON environment variable. The application parses this at runtime to authenticate with the Google Sheets API.')

    # 5. UI TABS
    add_heading_styled(doc, '5. Application Interface — Detailed Breakdown', level=1)

    add_para(doc, '• Report Incident: A dynamic multi-step form for victims. It silently queries ipapi.co to determine the victim\'s state (e.g., Karnataka) for future law enforcement routing. This data is encrypted. Victims can upload multiple evidence files, which are instantly hashed.')
    add_para(doc, '• Dashboard Overview: Features four live KPI cards (Total, Critical, Resolved, Escalated). Uses Chart.js to map Severity Distribution (Doughnut) and Attack Types (Bar chart).')
    add_para(doc, '• Incidents List: A searchable, paginated table of cases with color-coded severity badges.')
    add_para(doc, '• Incident Detail (Forensic View): The core of the platform. Displays:\n  - Explainable AI (XAI) Reasoning\n  - Score Breakdown (Evidence Match out of 40, Threat Indicators out of 30, Urgency out of 20, Vulnerability out of 10)\n  - Relevant Indian Penal Code (IPC) and IT Act sections\n  - Evidence Gaps (what the analyst should ask the victim for)\n  - Immutable Evidence Files with SHA-256 hashes\n  - Encrypted PII Vault (click-to-decrypt)')
    add_para(doc, '• Escalations: Shows cases routed to specific Indian State authorities (e.g., "Karnataka CID Cyber Crime"). Contains a custom Modal that dynamically injects correct nodal emails and phone numbers based on the victim\'s decrypted state.')
    add_para(doc, '• User Management: Admin-only view to modify RBAC roles.')
    add_para(doc, '• Audit Logs: Admin-only view of the complete, tamper-proof system ledger.')

    # 6. WORKFLOW
    add_heading_styled(doc, '6. Detailed Algorithmic Workflows', level=1)

    add_heading_styled(doc, '6.1 The 4-Step Forensic AI Framework', level=2)
    add_para(doc, 'When a report is submitted, the Gemini Multimodal Vision AI executes a strict 4-step framework:')
    add_para(doc, '1. Evidence Authenticity: Cross-references the written description against uploaded images/PDFs. Penalizes scores if severe claims lack evidence.')
    add_para(doc, '2. Threat Vector Classification: Categorizes the attack (e.g., Sextortion, Phishing, Deepfake Threat).')
    add_para(doc, '3. Victim Risk Assessment: Classifies the victim\'s physical/digital danger as IMMEDIATE, ACTIVE, SUBSIDED, or HISTORICAL.')
    add_para(doc, '4. Evidence Gaps: Identifies missing forensic artifacts (e.g., "Need original message headers" or "Need UPI transaction ID").')

    add_heading_styled(doc, '6.2 Rule-Based Heuristic Fallback Engine', level=2)
    add_para(doc, 'If the Google Gemini API hits a rate limit (HTTP 429 Resource Exhausted), the system implements an automatic retry mechanism with exponential backoff (40s, 80s). If all retries fail, it falls back to a custom Rule-Based Engine.')
    add_para(doc, 'This fallback engine uses Weighted Keyword Matching across threat dictionaries. Crucially, it includes Negation Guards (e.g., ignoring "hacked" if preceded by "wasn\'t" or "didn\'t"). It assigns base scores mapped to specific IPC sections without failing the user request.')

    add_heading_styled(doc, '6.3 Evidence Processing Pipeline', level=2)
    add_para(doc, 'File uploaded -> Extension and size validation -> Read into memory -> SHA-256 hash generated -> File saved securely using the hash as the filename -> Metadata stored in database -> Chain of Custody (COC_UPLOAD) audit entry created.')

    # Save
    docx_path = os.path.join(OUTPUT_DIR, 'W-CERT_Detailed_Technical_Summary.docx')
    doc.save(docx_path)
    print(f"[+] Word document saved: {docx_path}")
    return docx_path

def build_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    def section(title, body_lines, level=1):
        if level == 1:
            pdf.set_font('Helvetica', 'B', 14)
            pdf.set_text_color(0, 51, 102)
        else:
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(0, 102, 153)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        for line in body_lines:
            pdf.multi_cell(0, 5, line)
            pdf.ln(1)
        pdf.ln(3)

    # Title page
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(0, 51, 102)
    pdf.ln(40)
    pdf.multi_cell(0, 12, 'W-CERT\nWomen-Centric Cyber Emergency\nResponse & Threat-Analysis Framework', align='C')
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, 'Detailed Technical Architecture & Executive Summary', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, 'Capstone Project - April 2026', align='C', new_x="LMARGIN", new_y="NEXT")

    # Content pages
    pdf.add_page()

    section('1. Technical Stack & Architecture', [])
    section('Frontend (Presentation Layer)', [
        'Framework: React 18 with Vite for Hot Module Replacement.',
        'Styling: Tailwind CSS with custom glassmorphism and neon cyber aesthetics.',
        'Routing: React Router v6 with JWT-based Protected Routes for analysts.',
        'Visuals: Chart.js (react-chartjs-2) for real-time KPI generation.',
        'API Client: Axios with automatic token injection and 401 interceptors.'
    ], level=2)
    
    section('Backend & Data Layer', [
        'Framework: Python Flask 3.0 serving REST APIs with Gunicorn.',
        'Authentication: Flask-JWT-Extended handling Access/Refresh tokens.',
        'AI Engine: Google Gemini 1.5 Flash Vision API with RAG context injection.',
        'Database: Google Sheets (Serverless NoSQL) accessed via gspread.',
        'Cache: 60-second in-memory TTL to prevent Google API rate limiting.'
    ], level=2)

    section('2. Security, Hashing & Encryption', [
        'AES Encryption: PII (Names, Contact, State Location) encrypted using Fernet (AES-128-CBC) before database storage.',
        'Forensic Hashing: Incident descriptions and evidence files undergo SHA-256 hashing to ensure data integrity and legal admissibility.',
        'RBAC: Role-Based Access Control limits operations to USER, ANALYST, and ADMIN roles.',
        'Chain of Custody: Append-only tracking of all evidence interactions (UPLOAD, VIEW, VERIFY).',
        'Audit Logging: Immutable ledger tracking IP addresses, User IDs, and timestamps for every system action.'
    ])

    section('3. Deployment Architecture', [
        'Frontend (Vercel): Deployed on a serverless edge network for ultra-fast global delivery.',
        'Backend (Render.com): Deployed as a Persistent Web Service. This is architecturally critical to preserve the in-memory Google Sheets cache; a serverless backend would trigger rate limits.',
        'Credentials: Google Service Account JSON injected directly as an environment variable to prevent unauthorized file access.'
    ])

    pdf.add_page()

    section('4. Advanced Algorithmic Workflows', [])
    section('The 4-Step Forensic AI Framework', [
        'Step 1 (Authenticity): AI cross-references uploaded images against the victim\'s text.',
        'Step 2 (Classification): Identifies primary attack vectors (Sextortion, Deepfakes, Financial Fraud).',
        'Step 3 (Risk Assessment): Categorizes immediate physical or digital danger to the victim.',
        'Step 4 (Evidence Gaps): Highlights missing artifacts necessary for law enforcement.'
    ], level=2)

    section('Rule-Based Fallback Engine', [
        'If the Gemini API reaches its quota (HTTP 429), the system utilizes a custom Heuristic Fallback Engine. It performs weighted keyword matching (e.g., "leak"=35, "password"=20) across threat dictionaries. It utilizes Negation Guards to prevent false positives (e.g., ignoring "hacked" if preceded by "wasn\'t").'
    ], level=2)

    section('Jurisdictional Escalation Routing', [
        'During report submission, the frontend silently captures the victim\'s state via ipapi.co. This is encrypted in the database. When an analyst clicks "Escalate", the system decrypts this location and dynamically injects the exact contact details for that specific State\'s Cyber Crime Cell and Women\'s Commission.'
    ], level=2)

    pdf_path = os.path.join(OUTPUT_DIR, 'W-CERT_Detailed_Technical_Summary.pdf')
    pdf.output(pdf_path)
    print(f"[+] PDF saved: {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    print("Generating Detailed W-CERT Executive Summary...")
    build_docx()
    build_pdf()
    print("[+] Done! Both detailed files generated.")
