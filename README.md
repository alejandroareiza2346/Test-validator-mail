# Test-validator-mail
**Engineering Lead: Alejandro Areiza Alzate**
**Technical Domain: Input Validation Engineering / Secure Software Development / Regex Pattern Design**

---

## 1. Executive Summary and Architectural Vision

This project implements a **dual-validator input sanitization library** for two of the most common user-submitted data types in Colombian web applications: email addresses and mobile phone numbers. Both validators are built on compiled regular expressions from Python's `re` module, following a pure-function design with no side effects — each validator receives a string and returns a boolean, making the modules directly importable into any Flask route, Django form, or data pipeline requiring format-level input validation. A Tkinter desktop interface (`validador_gui.py`) exposes both validators through a unified GUI for standalone testing and demonstration. The architecture enforces a strict separation between validation logic (pure functions, no I/O) and the presentation layer (GUI class), enabling independent reuse of either component.

---

## 2. Requirement Analysis and Strategic Alignment

- **Functional:** Email address format validation against the RFC-aligned pattern `^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$` — enforcing the presence of a local part, `@` separator, domain name, and a TLD of at least two alphabetic characters; Colombian mobile number validation against the national numbering plan pattern `^3\d{9}$` — enforcing a 10-digit length, mandatory `3` prefix (the Colombian mobile network prefix), and exclusively numeric content; both validators exposed through a shared desktop GUI with independent input fields and real-time feedback.
- **Non-Functional:** Zero external dependencies — both validators use only Python's standard library `re` module; O(1) match time per input via pre-anchored regex patterns; importable as standalone functions without instantiating any class or running any GUI.
- **Strategic Goal:** Production-ready, reusable input validation primitives applicable to contact forms, lead capture pipelines, and API request sanitization layers — directly mitigating OWASP A03 (Injection) and A04 (Insecure Design) risk vectors that arise from accepting unvalidated user-supplied strings.

---

## 3. Technical Stack and Infrastructure

- **Core Language:** Python 3.x
- **Validation Engine:** Python `re` module — compiled regex pattern matching with full anchor enforcement (`^...$`)
- **GUI Framework:** Tkinter (Python Standard Library) — `validador_gui.py` exposes both validators through a desktop interface
- **Testing Framework:** pytest (`test_validador_correo_electronico.py`) — test file scaffolded for unit test implementation
- **Execution Environment:** Any POSIX-compatible system or Windows with Python 3.x; no `pip install` required for core validators
- **Design Pattern:** Pure Function / Functional Core — both `validar_correo_electronico` and `validar_numero_colombia` are stateless, side-effect-free functions with a single string input and boolean return, suitable for use in any execution context (CLI, web server, desktop app, test harness)

---

## 4. Engineering Logic and Implementation

**Email validator (`validador_correo_electronico.py`):**

The validation pattern `^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$` enforces four structural requirements via anchored regex:

- `^[\w\.-]+` — local part: one or more word characters, dots, or hyphens before the `@`
- `@` — mandatory separator
- `[\w\.-]+` — domain label: one or more word characters, dots, or hyphens
- `\.[a-zA-Z]{2,}$` — TLD: a dot followed by at least two alphabetic characters anchored to end of string

The full anchor (`^...$`) ensures the entire string is evaluated, preventing partial matches that would allow malformed prefixes or suffixes to pass validation.

**Colombian mobile validator (`validador_celular_colombia.py`):**

The validation pattern `^3\d{9}$` enforces the Colombian mobile numbering plan:

- `^3` — mandatory leading digit `3`, the prefix assigned to all Colombian mobile operators (Claro, Movistar, Tigo, WOM, ETB) by the national numbering authority (ANE — Agencia Nacional del Espectro)
- `\d{9}` — exactly nine additional numeric digits
- `$` — end anchor preventing strings longer than 10 digits from matching

This produces a 10-digit total length requirement consistent with all active Colombian mobile number assignments.

- **Complexity:** O(n) match scan in string length for both patterns; in practice O(1) for inputs under 320 characters (maximum RFC 5321 email length) — the regex engine exits on first structural violation.
- **Data Structures:** No mutable state — `re.match` compiles and evaluates the pattern against the input string in a single call, returning a match object (truthy) or `None` (falsy), cast to boolean via `bool()`.

---

## 5. Quality Assurance and Systematic Testing

Both validators are accompanied by inline test cases in their `__main__` blocks covering valid and invalid inputs across the primary failure modes. The `test_validador_correo_electronico.py` file provides the pytest scaffold for formalized unit test expansion.

**Email validator — test coverage:**

| Input | Expected | Failure mode tested |
|---|---|---|
| `usuario@dominio.com` | Valid | — |
| `usuario@dominio.co` | Valid | Short but valid TLD |
| `usuario@dominio` | Invalid | Missing TLD |
| `usuario@.com` | Invalid | Missing domain label |
| `@dominio.com` | Invalid | Missing local part |
| `usuario@dominio.c` | Invalid | TLD under 2 characters |
| `usuario.nombre@dominio.com` | Valid | Dot in local part |
| `usuario-nombre@dominio.com` | Valid | Hyphen in local part |

**Colombian mobile validator — test coverage:**

| Input | Expected | Failure mode tested |
|---|---|---|
| `3123456789` | Valid | — |
| `312345678` | Invalid | 9 digits only |
| `4123456789` | Invalid | Wrong prefix (not `3`) |
| `31234567890` | Invalid | 11 digits |
| `3a23456789` | Invalid | Non-numeric character |
| `3000000000` | Valid | Minimum operator prefix range |

- **Edge Case Handlers:** Empty string — `re.match` returns `None` on empty input for both patterns due to `+` quantifier on the local part; whitespace-only strings — rejected by both patterns as `\w` and `\d` do not match spaces; inputs with newlines — anchored patterns prevent cross-line partial matches.

---

## 6. Security Governance and Compliance

- **Input Validation as Security Control:** Both validators implement format-level input validation — the first line of defense against malformed data entering application logic, database queries, or external API calls. Rejecting structurally invalid email addresses at the entry point prevents a class of injection vectors that rely on malformed `@` placement or domain manipulation.
- **No Dynamic Execution:** Neither validator uses `eval()`, `exec()`, or any dynamic code execution path. All validation logic is static pattern matching via the `re` module.
- **OWASP Alignment:**
  - **A03 — Injection:** Structural validation of email and phone inputs before any downstream use in SQL queries, SMTP relay calls, or SMS gateway APIs prevents format-based injection attempts.
  - **A04 — Insecure Design:** Pure-function validators with boolean return enforce a fail-closed design — any input that does not match the pattern is rejected by default, with no ambiguous or partial-match state.
- **Production Integration Note:** These validators perform format-level validation only. For production use, email deliverability should be confirmed via SMTP handshake or a verification link; Colombian mobile number ownership should be confirmed via OTP delivery. Format validation is a necessary but not sufficient control for full input integrity assurance.

---

## 7. Deployment and Initialization

**Prerequisites:** Python 3.x (no external packages required for core validators)

```bash
# Clone the repository
git clone https://github.com/alejandroareiza2346/Test-validator-mail.git

cd Test-validator-mail

# Run the email validator with built-in test cases
python validador_correo_electronico.py

# Run the Colombian mobile validator with built-in test cases
python validador_celular_colombia.py

# Launch the GUI (both validators accessible from one interface)
python validador_gui.py
```

**Import as a module in your own project:**

```python
from validador_correo_electronico import validar_correo_electronico
from validador_celular_colombia import validar_numero_colombia

# Email validation
validar_correo_electronico("user@example.com")   # True
validar_correo_electronico("not-an-email")        # False

# Colombian mobile validation
validar_numero_colombia("3201234567")  # True
validar_numero_colombia("1234567890")  # False — does not start with 3
```

**Run the test suite:**

```bash
pip install pytest
pytest test_validador_correo_electronico.py -v
```

---

## 8. Repository Contents

| File | Description |
|---|---|
| `validador_correo_electronico.py` | Email format validator — regex pattern + inline test cases |
| `validador_celular_colombia.py` | Colombian mobile number validator — ANE numbering plan + inline test cases |
| `validador_gui.py` | Tkinter GUI exposing both validators in a shared desktop interface |
| `test_validador_correo_electronico.py` | pytest scaffold for email validator unit tests |
| `requirements.txt` | Dependency declaration (standard library only) |

---

## 9. Professional Background

Project designed and developed by **Alejandro Areiza Alzate**, Computer Engineering student at Universidad Autónoma Latinoamericana (UNAULA), Medellín, and GitHub Developer Program member.

- **LinkedIn:** [linkedin.com/in/alejandro-areiza-alzate-8a73a53b4](https://www.linkedin.com/in/alejandro-areiza-alzate-8a73a53b4)
- **Research (ORCID):** [0009-0002-2116-6918](https://orcid.org/0009-0002-2116-6918)
- **Certifications:** Microsoft Learn Level 6 — 26,950 XP (Azure Identity, Network Security & SQL Security); Cisco; Google; IBM; OWASP Top 10

---

## 10. License

Distributed under the **MIT License**. See `LICENSE` for full terms.
