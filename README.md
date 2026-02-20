# Payload Generation Framework

**Organization:** ITSOLERA (PVT) LTD  
**Author:** Offensive Team Zeta  
**Task:** Offensive Security Tool Development — Payload Generation Framework  
**Date:** February 20, 2026

---

> ⚠️ **ETHICAL USE ONLY.**  
> This tool is developed strictly for educational, defensive, and authorized penetration testing environments.  
> Any misuse outside legal authorization is strictly prohibited.  
> Aligned with the [OWASP Code of Ethics](https://owasp.org/www-project-code-of-ethics/).

---

## Overview

A modular, Python-based CLI framework that generates payload **templates** for three common web vulnerability classes. It demonstrates how attackers attempt to exploit vulnerabilities and how security controls (WAFs, filters, validators) respond — without sending any live traffic or executing any real commands.

All three modules are accessible through a single unified entry point:

```
python3 main.py --module <xss|sqli|cmdi> [options]
```

---

## Project Structure

```
├── main.py                        ← Unified CLI entry point (all modules)
├── README.md
├── assignment.md
├── pyrightconfig.json
├── .gitignore
│
├── modules/
│   ├── xss/
│   │   └── xss_module.py          ← XSS generator logic
│   ├── sqli/
│   │   └── sqli_module.py         ← SQL Injection generator logic
│   └── cmdi/
│       ├── cmdi_module.py         ← Command Injection generator logic
│       └── cmdi_docs.py           ← CMDi reference documentation
│
└── payloads/
    ├── templates/
    │   └── xss_templates.json     ← XSS payload template definitions
    └── output/                    ← Generated export files (auto-created)
        ├── xss/
        ├── sqli/
        └── cmdi/
```

---

## Quick Start

### Requirements

- Python 3.8+
- No external dependencies — standard library only

### Run

```bash
python3 main.py --help
```

---

## Modules

### A. XSS Payload Module

Generates non-executing XSS payload templates demonstrating reflected, stored, and DOM-based XSS across HTML, attribute, and JavaScript injection contexts.

**Features:**

- Payload types: `reflected`, `stored`, `dom`
- Context awareness: `html`, `attribute`, `javascript`
- Encoding: `url`, `base64`, `hex`
- WAF bypass techniques: case manipulation, comment insertion, tag switching
- Burp Suite + OWASP ZAP export
- Defensive notes

**Usage:**

```bash
# All payloads, CLI output
python3 main.py --module xss

# Reflected XSS in HTML context, URL-encoded
python3 main.py --module xss --type reflected --context html --encode url

# DOM XSS with bypass techniques, exported to Burp Suite format
python3 main.py --module xss --type dom --bypass --output burp --no-banner

# Export all formats at once
python3 main.py --module xss --output all --no-banner

# Show defensive countermeasures
python3 main.py --module xss --defensive
```

**Reference:** [PortSwigger XSS Cheat Sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)

---

### B. SQL Injection Payload Module (Simulation Mode)

Generates SQLi string examples used in labs and scanners. No live database interaction.

**Features:**

- Injection types: `error`, `union`, `blind` (boolean), `time`, `comment`
- DB selector: `mysql`, `postgresql`, `mssql`, or `all`
- Comment-based bypass examples
- Case variation and whitespace abuse (WAF/IDS evasion)
- Encoding demonstrations: `url`, `base64`, `hex`
- Burp Suite + OWASP ZAP export
- Defensive notes

**Usage:**

```bash
# All payloads for all databases, CLI output
python3 main.py --module sqli

# MySQL error-based payloads only
python3 main.py --module sqli --db mysql --type error

# PostgreSQL UNION payloads with detailed explanations
python3 main.py --module sqli --db postgresql --type union --explain

# Show WAF bypass techniques with base64 encoding demo
python3 main.py --module sqli --db mysql --bypass --encode base64 --no-banner

# Export all formats for all databases
python3 main.py --module sqli --db all --output all --no-banner

# Show defensive countermeasures
python3 main.py --module sqli --defensive
```

**Reference:** [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)

---

### C. Command Injection Module (Pattern-Based)

Generates command injection string patterns for study. All patterns are disabled by default, clearly marked as non-executable examples, and no system commands are run.

**Features:**

- OS detection: `linux`, `windows`, or `all`
- Command separators as strings only: `;`, `&&`, `||`, `|`, backtick, `$()`, `%0A`, `^&`, CRLF
- Explanation of why each filter fails
- Burp Suite + OWASP ZAP export
- Defensive notes

**Usage:**

```bash
# All patterns for all OSes, CLI output
python3 main.py --module cmdi

# Linux patterns with filter-fail explanations
python3 main.py --module cmdi --os linux --explain

# Windows patterns exported to JSON
python3 main.py --module cmdi --os windows --output json --no-banner

# Show filter bypass explanation
python3 main.py --module cmdi --bypass --no-banner

# Export all formats
python3 main.py --module cmdi --output all --no-banner

# Show defensive countermeasures
python3 main.py --module cmdi --defensive
```

**Reference:** [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)

---

## CLI Reference

All options are available from the unified `main.py` entry point.

```
python3 main.py --module MODULE [options]
```

| Flag | Values | Description |
|---|---|---|
| `--module` | `xss` \| `sqli` \| `cmdi` | **Required.** Select the vulnerability module |
| `--type` | `reflected\|stored\|dom\|all` *(xss)* / `error\|union\|blind\|time\|comment\|all` *(sqli)* | Payload sub-type |
| `--context` | `html\|attribute\|javascript\|all` | *[xss]* Injection context |
| `--db` | `mysql\|postgresql\|mssql\|all` | *[sqli]* Database type |
| `--os` | `linux\|windows\|all` | *[cmdi]* Target operating system |
| `--encode` | `none\|url\|base64\|hex` | Encoding demonstration |
| `--output` | `cli\|json\|txt\|burp\|zap\|all` | Output format |
| `--bypass` | flag | Include WAF/IDS bypass and evasion techniques |
| `--explain` | flag | Include detailed explanation for each payload |
| `--stats` | flag | Show payload/pattern count statistics |
| `--defensive` | flag | Show defensive notes and WAF detection info, then exit |
| `--no-banner` | flag | Suppress the ethics prompt (for scripting/automation) |

---

## Output Formats

| Format | Description | Location |
|---|---|---|
| `cli` | Formatted terminal output | terminal |
| `json` | Full payload data with metadata | `*_output/*.json` |
| `txt` | Plain-text payload catalog | `*_output/*.txt` |
| `burp` | Burp Suite Intruder payload list | `*_output/*_burp.txt` |
| `zap` | OWASP ZAP Fuzzer payload list | `*_output/*_zap.txt` |
| `all` | Exports every format at once | all of the above |

### Using with Burp Suite (Payload Export Only)

1. Open Burp Suite → Proxy → Intercept a request from your **authorized** target
2. Right-click → **Send to Intruder**
3. Intruder → Positions → highlight the injection point → click **Add §**
4. Intruder → Payloads → Payload type: `Simple list`
5. Click **Load** → select the generated `*_burp.txt` file
6. Click **Start Attack** (authorized lab / DVWA only)

> ❌ This tool does **not** send any requests. It exports template lists for import only.

### Using with OWASP ZAP (Offline Mode)

1. Start ZAP → **Manual Explore** → browse to your authorized target
2. Find the request in the **History** tab
3. Right-click → **Attack** → **Fuzz**
4. Highlight the injection point in the request body
5. Payloads → **Add** → Type: `File` → select the generated `*_zap.txt` file
6. Click **Start Fuzzer** (authorized lab only)

---

## Advanced Features

### Encoding Demonstrations

The `--encode` flag applies encoding to demonstrate how payloads can evade naive filters:

```bash
python3 main.py --module xss --encode url --no-banner
python3 main.py --module sqli --db mysql --encode base64 --no-banner
python3 main.py --module xss --encode hex --no-banner
```

### Obfuscation / WAF Bypass

The `--bypass` flag produces evasion variants:

- **Comment insertion** — `UN/**/ION SE/**/LECT`
- **Case variation** — `uNiOn SeLeCt`
- **Whitespace abuse** — tab, newline, `/**/` as space substitutes
- **Mixed encoding** — hex, CHAR(), CONCAT() chaining

```bash
python3 main.py --module sqli --bypass --no-banner
python3 main.py --module xss --bypass --output burp --no-banner
```

### Defensive Notes

Each module includes a `--defensive` flag that explains:

- Why WAFs block these payload patterns
- How modern defenses detect evasion attempts
- The best mitigations (parameterised queries, allowlists, API-based commands, etc.)

```bash
python3 main.py --module xss   --defensive
python3 main.py --module sqli  --defensive
python3 main.py --module cmdi  --defensive
```

---

## Sample Payload Templates

Example payloads included in `payloads/output/` and `sqli_output/` after running with `--output all`:

**XSS (reflected, HTML context):**

```
<script>alert('XSS')</script>
<img src=x onerror=alert(1)>
<svg onload=alert(document.domain)>
```

**SQLi (MySQL, error-based):**

```
1' AND extractvalue(rand(), concat(0x3a, (SELECT user())))--
1' AND updatexml(1, concat(0x3a, (SELECT database())), 1)--
```

**CMDi (Linux):**

```
EXAMPLE - DO NOT EXECUTE: INPUT_VALUE ; example_command
EXAMPLE - DO NOT EXECUTE: INPUT_VALUE $(example_command)
```

---

## Ethical Disclaimer

```
This tool is developed strictly for educational, defensive, and authorized
penetration testing environments.
Any misuse outside legal authorization is strictly prohibited.
```

**Permitted use:**

- Authorized penetration testing with written permission
- Academic learning, research, and CTF challenges
- Your own systems and controlled lab environments (DVWA, HackTheBox, TryHackMe)

**Prohibited use:**

- Unauthorized access to any systems, databases, or networks
- Real-world attacks without explicit written permission
- Any activity that violates local or international law

---

## References

| Resource | URL |
|---|---|
| OWASP Testing Guide | <https://owasp.org/www-project-web-security-testing-guide/> |
| OWASP Code of Ethics | <https://owasp.org/www-project-code-of-ethics/> |
| OWASP SQL Injection | <https://owasp.org/www-community/attacks/SQL_Injection> |
| OWASP Command Injection | <https://owasp.org/www-community/attacks/Command_Injection> |
| PortSwigger XSS Cheat Sheet | <https://portswigger.net/web-security/cross-site-scripting/cheat-sheet> |
| PortSwigger Web Security Academy | <https://portswigger.net/web-security> |
| PayloadsAllTheThings (Study Only) | <https://github.com/swisskyrepo/PayloadsAllTheThings> |
| OWASP WAF Bypass Research | <https://owasp.org/www-project-top-ten/> |

---

*Signed — ITSOLERA Cyber Department · Muhammad Ahsan Ayaz · Cyber Team Lead*
