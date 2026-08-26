```markdown
# Angza – AI Contract Auditor

**Illuminate the fine print. Secure your contracts.**

---

## 📌 Introduction

Angza is an AI-powered contract and financial document auditing platform. It helps businesses, legal teams, compliance officers, and freelancers quickly identify hidden risks, problematic clauses, and compliance gaps in their documents.

Instead of spending hours reading hundreds of pages of legal text, users upload their documents and receive a structured risk report with severity scores, key terms, red flags, and actionable recommendations — all in under two minutes.

**Try the live demo:** [https://angza.vercel.app](https://angza.vercel.app)

---

## 🧠 Problem Statement

Contracts are the backbone of every business. Yet, they are often long, dense, and filled with legal jargon that makes it difficult to spot risks.

**Key challenges:**

- **Hidden clauses:** Unbalanced liability caps, one‑sided termination terms, and ambiguous payment conditions are buried in pages of text.
- **Time-consuming review:** Legal teams spend hours manually reviewing documents, delaying decisions.
- **Costly mistakes:** A single missed clause can cost thousands in legal fees or lost revenue.
- **Inefficient workflows:** Freelancers, startups, and small businesses often lack access to in‑house legal counsel.
- **Compliance pressure:** Businesses must comply with regulations like SOC-2, GDPR, and industry standards — but tracking compliance across hundreds of documents is a nightmare.

There is a clear need for a tool that makes contract review fast, accurate, and accessible to everyone — not just large law firms.

---

## ✅ How Angza Solves It

Angza transforms manual contract review into a fast, automated, and precise audit.

**How it works:**

1. **Upload:** Users upload a document (PDF, Word, Excel, or TXT).
2. **Analyse:** Angza's AI extracts key terms, classifies the document, runs deterministic checks, and performs deep semantic reasoning to flag risks.
3. **Get Report:** Users receive a structured report with:
   - **Risk Score** (0–100)
   - **Key Terms** (parties, payment terms, termination, liability cap, governing law)
   - **Findings** (clause‑level issues with severity scores and recommendations)
   - **Red Flags** (critical issues requiring immediate attention)

**Key features:**

| Feature | Description |
|---------|-------------|
| **Unlimited Document Length** | Reviews entire contracts, annual reports, or codebases of any size. |
| **Multi‑Stage AI Analysis** | Classifies, extracts, cross‑references, and flags risks using a specialised pipeline. |
| **Enterprise‑Grade Security** | SOC‑2 ready, on‑premise deployment available, zero data retention. |
| **Universal Document Support** | PDF, Word, Excel, emails, and scanned images (OCR included). |
| **Smart Risk Identification** | Severity scores with actionable recommendations and clause citations. |
| **Custom Compliance Rules** | Define deterministic checks (cap limits, currency thresholds) via simple configuration. |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js (for frontend development, optional)
- OpenRouter, Gemini, or Groq API key

### Local Development

1. Clone the repository:

```bash
git clone https://github.com/ClovisOdhiambo444/Angza.git
cd Angza
```

2. Set up the backend:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Environment variables:

> **Note:** You already have a `.env` file. If setting up fresh, copy `.env.example` to `.env` and add your API keys.

4. Run the backend:

```bash
python3 run.py
```

5. Run the frontend (in a new terminal):

```bash
cd frontend
python3 -m http.server 3000
```

6. Open `http://localhost:3000` in your browser.

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla), TailwindCSS |
| **Backend** | Python, FastAPI |
| **AI Integration** | OpenRouter (Gemini 2.5 Flash), Groq, Gemini |
| **File Parsing** | PyPDF2, python-docx, openpyxl, pandas |
| **Report Generation** | ReportLab (PDF), openpyxl (Excel) |
| **Deployment** | Vercel (Frontend), Render (Backend) |

---

## 📊 Use Cases

| Use Case | Who It's For |
|----------|--------------|
| **NDA Review** | Startups, legal teams, freelancers |
| **Vendor Contract Audit** | Procurement, compliance teams |
| **Employment Agreement** | HR, legal departments |
| **Financial Compliance** | CFOs, finance teams |
| **Investment Term Sheets** | Founders, investors |
| **Annual Report Review** | Analysts, auditors |

---

## 📁 Project Structure

```
ANGZA/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── audit_engine.py
│   │   ├── deepseek_client.py
│   │   ├── parsers/
│   │   ├── routes/
│   │   └── report_generator.py
│   ├── requirements.txt
│   ├── .env
│   ├── .env.example
│   └── run.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── assets/
│       ├── logo.png
│       ├── bg.jpg
│       ├── bg4.jpeg
│       └── favicon.ico
├── render.yaml
├── .gitignore
└── README.md
```

---

## 🔐 Security & Privacy

- **Zero data retention:** Uploaded documents are processed in memory and immediately discarded.
- **No third‑party sharing:** Your data is never shared with third parties.
- **SOC‑2 ready:** Built with enterprise‑grade security standards.
- **On‑premise deployment:** Available for enterprises requiring full data control.

---

## 🧪 Testing

### Test the API directly

```bash
curl -X POST "https://angza-backend.onrender.com/api/upload" \
  -F "file=@/path/to/sample.pdf"
```

### Test the frontend

Open `http://localhost:3000` or the live URL `https://angza.vercel.app` and upload a document.

---

## 🌐 Live Deployment

| Service | URL |
|---------|-----|
| **Frontend** | [https://angza.vercel.app](https://angza.vercel.app) |
| **Backend** | [https://angza-backend.onrender.com](https://angza-backend.onrender.com) |
| **API Docs** | [https://angza-backend.onrender.com/docs](https://angza-backend.onrender.com/docs) |

---

## 🚀 Future Roadmap

| Feature | Status |
|---------|--------|
| Email report delivery | Planned |
| Drag‑and‑drop upload | ✅ Done |
| Real‑time progress bar | Planned |
| Shareable report links | Planned |
| Multi‑language support | Planned |
| Custom rule templates | Planned |

---

## 🧑‍💻 Built By

**Clovis Odhiambo**
- [GitHub](https://github.com/ClovisOdhiambo444)
- [LinkedIn](https://linkedin.com/in/clovisodhiambo)

---

## 📄 License

This project is proprietary and confidential. Unauthorised copying, distribution, or use is strictly prohibited.

---

## 🤝 Contributing

Contributions are welcome. Please open an issue or submit a pull request for review.

---

## 📬 Contact

For questions, feedback, or custom deployment inquiries:

- Email: **clovisodhiambo44@gmail.com**
- GitHub: [ClovisOdhiambo444](https://github.com/ClovisOdhiambo444)

---

**© 2026 Angza, Inc. Built by Clovis Odhiambo.**