# CodeSentry — Hackathon Preparation Guide
**Team:** Ai-vengers | Yashita Gaur & Divjot Bedi
**College:** University School of Automation and Robotics
**Tracks:** Track 1 (ArmorClaw) + Track 2 (ArmorIQ)

---

## 1. Project Overview

CodeSentry is an **AI-powered security code review mentor**. It does not just detect vulnerabilities — it explains them in plain language, suggests fixes, verifies those fixes actually worked, and logs the entire session for compliance.

The core insight: existing tools like Snyk and Semgrep are scanners, not teachers. They dump a list of findings with no context, no explanation, and no proof that a fix worked. CodeSentry closes that gap.

**One-line pitch:**
> *"CodeSentry turns every code review into a security lesson — catching what scanners find, but explaining and proving fixes the way a senior mentor would."*

---

## 2. The Problem in Numbers

| Stat | What It Means |
|---|---|
| 74% of breaches involve human error or known bad patterns | Developers ship vulnerabilities not out of malice but ignorance |
| 0 explanations given by typical scanners to junior devs | Tools flag issues but never teach why they matter |
| 100% of fixes left unverified by traditional tools | There is no proof a fix actually worked |

### Who is affected
- **Junior Developers** — flagged with no idea why the fix matters
- **Startups & SMBs** — no dedicated security staff to review every PR
- **Open-Source Maintainers** — need consistent, explainable security gates on contributions

---

## 3. The Solution — Full Loop in 5 Steps

```
1. Submit Code      →  Upload a file or link a PR
2. ArmorClaw Scan   →  Real security scanner finds issues with severity scores
3. AI Explains      →  Claude explains each risk in plain language + analogy
4. Fix & Re-scan    →  Suggests fix, user applies it, re-scan verifies it worked
5. Audit Log        →  ArmorIQ logs the full session for compliance
```

**What makes CodeSentry different from existing scanners:**

| Existing Scanners | CodeSentry |
|---|---|
| "Here's a list of errors." | "Here's the error, why it matters, the fix, and proof it's fixed." |
| No explanation of why it matters | Beginner-friendly AI explanations with real-world analogies |
| No verification that fixes worked | Re-scan loop confirms resolution |
| No audit trail for compliance | Every session logged via ArmorIQ |

---

## 4. Key Features

### Automated Security Scanning
ArmorClaw scans uploaded code for vulnerabilities like SQL Injection, hardcoded secrets, weak cryptography, command injection, insecure deserialization, path traversal, and debug mode enabled — each with a severity score (Critical / High / Medium / Low).

### Beginner-Friendly AI Explanations
Claude explains *why* each issue is dangerous using plain language and real-world analogies — not jargon. Example for SQL Injection: *"It's like a bank teller who reads your deposit slip aloud as a command — if you write 'and also empty vault 7', they'd do it without question."*

### Auto-Fix Suggestions
For each vulnerability, Claude proposes a corrected code snippet specific to the exact variable or function that was flagged — not a generic template.

### Verification Loop
After the user applies a fix, CodeSentry automatically re-scans the patched code (not the original). If the finding is gone, it flips to ✅ Resolved. If still present, it stays ⚠️ Unresolved. This is the critical difference from all existing tools.

### Compliance Audit Trail (ArmorIQ)
Every session is logged with: session ID, timestamp, filename, all findings (type, severity, line), fix applied (yes/no), and re-scan result. Ready-made evidence for SOC 2 / ISO 27001 audits.

### Team Skill Dashboard *(post-MVP)*
Tracks recurring issue types across a team to highlight where developers need the most mentoring.

---

## 5. Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React + Tailwind CSS | Upload UI, results dashboard, diff view |
| Backend | Python + FastAPI | Orchestrates the scan → explain → verify pipeline |
| Security Scanner | ArmorClaw | Detects vulnerabilities, assigns severity scores |
| AI Layer | Claude API (claude-sonnet-4-6) | Generates plain-language explanations and fix suggestions |
| Audit & Policy | ArmorIQ SDK | Logs every scan, fix, and re-scan result |
| Storage | PostgreSQL / SQLite (MVP) | Session history and review data |

---

## 6. Architecture

```
User (Browser)
     │
     ▼
React Frontend
     │  POST /api/scan  (original code)
     ▼
FastAPI Backend
     │
     ├──► ArmorClaw Scanner ──► findings JSON (type, severity, line, snippet)
     │
     ├──► Claude API (per finding) ──► explanation + analogy + fix snippet
     │
     │  POST /api/verify  (PATCHED code — not original)
     │
     ├──► ArmorClaw Scanner ──► re-scan findings
     │
     └──► ArmorIQ SDK ──► audit log entry
     │
     ▼
React Frontend ◄── Full results with Resolved / Unresolved status
```

**Key implementation detail on verify:** The `/api/verify` endpoint receives the patched code (with all user-applied fixes) and re-scans that, not the original upload. This is what makes the resolution status accurate.

---

## 7. Demo Results (Live)

From our working prototype scanning `vulnerable_app.py`:

| ID | Type | Severity | Line | Status |
|---|---|---|---|---|
| f1 | Hardcoded Secret | Critical | 10 | ✅ Resolved |
| f2 | Hardcoded Secret | Critical | 11 | ✅ Resolved |
| f3 | SQL Injection | Critical | 26 | ✅ Resolved |
| f4 | Weak Cryptography | High | 35 | ✅ Resolved |
| f5 | Command Injection | High | 43 | ✅ Resolved |
| f6 | Insecure Deserialization | High | 51 | ✅ Resolved |
| f7 | Debug Mode Enabled | Medium | 57 | ✅ Resolved |

**7/7 findings resolved after applying fixes — verified by re-scan.**

---

## 8. Impact & Feasibility

### Who Benefits
- **Junior Developers** — learn security on the job, every flagged issue becomes a mini-lesson
- **Startups & SMBs** — get enterprise-grade security review without hiring a security team
- **Open-Source Projects** — maintain consistent, explainable security gates on community PRs

### Real-World Impact
- Fewer vulnerabilities shipped to production
- Security awareness builds organically within dev teams over time
- Ready-made compliance evidence (SOC 2, ISO 27001) generated as a byproduct of normal development
- Reduces dependency on scarce, expensive security specialists

### Scalability
- Plugs directly into GitHub Actions / GitLab CI — scales to teams of any size
- Built on open-source ArmorClaw + existing ArmorIQ platform — low infrastructure cost
- Deployable as SaaS or self-hosted for enterprise privacy needs

---

## 9. Hackathon Q&A Prep

### Technical Questions

**Q: How does ArmorClaw work under the hood?**
> ArmorClaw is a static analysis security scanner. It parses source code using pattern matching and AST (Abstract Syntax Tree) analysis to identify known vulnerability patterns — things like string concatenation in SQL queries, calls to `os.system()` with user input, use of `pickle.loads()`, and hardcoded credential patterns. Each finding includes the vulnerability type, line number, and a severity score.

**Q: Why Claude specifically for explanations?**
> Claude is particularly strong at following nuanced instructions and producing consistent, structured output. We prompt it with the vulnerability type, the exact code snippet, and the scanner message, and it reliably returns a plain-language explanation, a real-world analogy, and a code-specific fix — all tailored to the exact variable or function flagged, not a generic template.

**Q: How does the verification loop actually work?**
> When a user clicks "Apply Fix," the fix is applied to an in-memory copy of the code in the frontend. When they click "Verify," we send that patched code — not the original file — to our `/api/verify` endpoint, which runs a fresh ArmorClaw scan. Any finding that no longer appears in the re-scan is marked Resolved. This is the core differentiator from every existing tool.

**Q: What if the AI suggests a wrong fix?**
> The fix suggestion is shown as a diff before the user applies it — they always have final control. We never auto-apply without user confirmation. Additionally, the re-scan loop immediately tells them if the fix actually worked, so incorrect fixes are caught before they ship.

**Q: How do you handle false positives from the scanner?**
> ArmorClaw's findings are passed through Claude, which has context about the full code snippet and can qualify its explanation. In future iterations, we plan to add a "dismiss" button per finding with a reason, which would also be logged in ArmorIQ for audit purposes.

**Q: What languages does it support?**
> Currently Python, JavaScript, TypeScript, Java, and Go — the most common languages in startup and open-source codebases. ArmorClaw's rules are language-specific, so adding new languages is a matter of adding rule sets.

**Q: How does ArmorIQ integration work?**
> We use the ArmorIQ SDK to write a structured log entry at the end of each session. The entry contains session ID, timestamp, filename, all findings with their metadata, which fixes were applied, and the re-scan outcome. This creates a ready-made audit trail without any extra developer effort.

---

### Product & Strategy Questions

**Q: How is this different from Snyk or Semgrep?**
> Snyk and Semgrep are great at detection, but they stop there. They give you a list of issues with technical descriptions — no explanation of why it matters, no suggested fix specific to your code, no verification that the fix worked, and no audit trail. CodeSentry adds the entire layer between "finding" and "fixed and proven" — which is where junior developers and small teams actually get stuck.

**Q: Who is your primary target user?**
> Junior developers and small engineering teams at startups. They write most of the vulnerable code, they have the least security training, and they have no dedicated security staff. Every flagged issue in CodeSentry becomes a teaching moment, so the team gets more secure over time just by using the tool normally.

**Q: What's the business model post-hackathon?**
> SaaS with a freemium model — free for individual developers scanning individual files, paid tiers for team features (shared audit trails, team skill dashboard, GitHub Actions integration, higher scan volume). Enterprise can self-host for data privacy compliance.

**Q: Could this be misused to understand vulnerabilities for malicious purposes?**
> The explanations are educational — the same content is in every security textbook and OWASP guide. CodeSentry explains why a pattern is dangerous and how to fix it, not how to exploit it. The tool is oriented entirely toward remediation, not attack.

**Q: What's the roadmap beyond the hackathon?**
> Phase 1 (now): File upload MVP with full scan → explain → fix → verify → log loop. Phase 2: GitHub PR integration and GitHub Actions support. Phase 3: Team skill dashboard showing recurring vulnerability patterns per developer. Phase 4: Custom rule sets and enterprise self-hosting.

---

### Track-Specific Questions

**Q: How does this meet Track 1 (ArmorClaw) requirements?**
> ArmorClaw is our core scanning engine. Every vulnerability detection — the finding type, severity score, and line number — comes directly from ArmorClaw. We also use it for the re-scan in the verification loop, making it central to both the detection and resolution flow.

**Q: How does this meet Track 2 (ArmorIQ) requirements?**
> ArmorIQ is our audit and compliance layer. We use the ArmorIQ SDK to log every session with full metadata — findings, fixes applied, re-scan results, timestamps. This directly serves the compliance use case (SOC 2, ISO 27001) and is visible in the UI as the Audit Trail panel.

**Q: Why did you choose both tracks?**
> They're naturally complementary. ArmorClaw provides the ground truth of what's vulnerable; ArmorIQ provides the record of what was done about it. A tool that detects but doesn't log is incomplete for compliance. A log without accurate detection is meaningless. Together they make CodeSentry's loop complete.

---

### Curveball Questions

**Q: What if ArmorClaw misses a vulnerability?**
> No scanner catches everything — that's true of Snyk, Semgrep, and every other static analysis tool. We're transparent about this: CodeSentry is a layer of defense, not a guarantee. The AI explanation layer actually helps here — Claude can sometimes flag additional concerns in its explanation even if the scanner missed them.

**Q: Why not just use GPT-4 to scan and explain in one step without a dedicated scanner?**
> LLMs are inconsistent at security scanning — they hallucinate findings, miss real ones, and can't produce reliable severity scores. ArmorClaw gives us deterministic, rule-based detection with structured output. Claude then adds the layer that rule-based tools can't: contextual explanation and education. Each tool does what it's best at.

**Q: How do you ensure the audit log can't be tampered with?**
> In the MVP, ArmorIQ handles log integrity. In production, we'd add log signing and immutable storage (append-only database or a service like AWS CloudTrail) to ensure audit records are tamper-evident — important for SOC 2 compliance.

**Q: What's your biggest technical risk?**
> Claude API latency per finding — if a file has 10+ findings, sequential API calls can make the UI feel slow. We mitigate this with parallel async calls in FastAPI and skeleton loaders in the UI so the user sees results streaming in rather than waiting for everything at once.

---

## 10. One-Minute Pitch (Memorize This)

> "74% of security breaches involve human error or known bad patterns. Junior developers ship SQL injections and hardcoded secrets not because they're careless, but because they don't recognize the risk. Existing tools like Snyk dump a list of findings with no explanation and no proof that fixes work.
>
> CodeSentry is an AI-powered security mentor. You upload your code, ArmorClaw scans it, Claude explains each vulnerability in plain language with a real-world analogy, suggests a fix, and then we re-scan to prove the fix actually worked. Every session is logged in ArmorIQ for compliance.
>
> We just demoed this live — 7 vulnerabilities detected, 7 fixed, 7 verified resolved, full audit trail logged. Scanners detect. CodeSentry teaches, fixes, and proves."

---

*Version 1.0 — Hackathon Day Prep*
