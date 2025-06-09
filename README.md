# hAPI Pay - Public UK Payroll Calculator API

[![CI](https://img.shields.io/badge/Tests-passing-brightgreen)]()

**hAPI Pay** is the UK’s first API-first payroll calculator backend:

✅ Public API endpoints (SEO-friendly)  
✅ Take-Home Pay calculator  
✅ Tax-only calculator  
✅ NI-only calculator  
✅ Student Loan-only calculator  
✅ Overpayment calculator with PDF export  
✅ PayrollRun API → run payroll per employee → full API  
✅ Payslip PDF export → branded template  
✅ Ready for RTI phase 2 → FPS/EPS/Corrected FPS planned  
✅ Fully tested with CI support  

---

## Features

✅ Public Calculators API (SEO + traffic):

- `POST /api/calculators/take-home/`
- `POST /api/calculators/tax-only/`
- `POST /api/calculators/ni-only/`
- `POST /api/calculators/student-loan-only/`
- `POST /api/calculators/overpayment/`
- `GET /api/calculators/overpayment/<id>/pdf/`

✅ Paid Core Payroll Engine:

- `POST /api/payroll/runs/`
- `GET /api/payroll/runs/`
- `GET /api/payroll/runs/<id>/`
- `GET /api/payroll/runs/<id>/payslip/pdf/`

✅ Full unit test coverage → `python manage.py test`  
✅ GitHub Actions CI template provided  

---

## Setup Instructions

1️⃣ Clone this repo  
2️⃣ Create and activate a virtualenv:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
