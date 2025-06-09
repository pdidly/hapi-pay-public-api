# hAPI Pay - Public UK Payroll API + Calculators

**hAPI Pay** is a lean, API-first UK payroll engine and calculator platform designed to operate as a simple, low-maintenance SaaS for self-service users.

## Features

✅ Public Calculators API (SEO + organic growth funnel):

- Take-home pay calculator → gross → net → tax → NI → student loan
- Tax-only calculator
- NI-only calculator
- Student Loan-only calculator
- Overpayment Refund Calculator (full spec implemented)
- Public Payslip PDF endpoint

✅ Paid Core Payroll API:

- PayrollRun model → gross → net → tax → NI → SL
- Store original calculation and corrected calculation
- View differences → regenerate payslip
- Branded Payslip PDF generation (WeasyPrint / HTML fallback)
- Ready for FPS / EPS RTI submission integration

✅ Core System Architecture:

- ActivityLog model → full user action tracking → reduces support tickets
- EmailSender util → send templated onboarding / alert emails → proactive communication
- GitHub Actions CI → full test coverage maintained on every push
- Single Django + DRF backend → no bloat → easy to maintain as a solo founder
- Optimised for SEO-driven growth → public calculators exposed as API

## Philosophy

hAPI Pay is intentionally designed to be:

✅ Simple → avoid unnecessary complexity  
✅ Self-service first → 99% of actions can be completed without contacting support  
✅ Clear communication → proactive emails and activity logging built-in  
✅ Maintainable → easy to operate and extend with ChatGPT + VS Code  
✅ Low-cost infrastructure → single server / single DB → scalable to £5k–£10k/month MRR with minimal cost  
✅ SEO-first → public calculators are primary acquisition funnel  

## Project Structure
hapi_pay_calc/
├── calculators/
├── payroll/
├── core/
├── .github/workflows/
├── templates/
├── requirements.txt
├── setup.sh
├── Makefile
├── README.md
└── manage.py

# One-time setup
git clone https://github.com/pdidly/hapi-pay-public-api.git
cd hapi-pay-public-api
./setup.sh

