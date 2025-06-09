from django.template.loader import render_to_string

def generate_payslip_pdf(payroll):
    html = render_to_string('payslip_template.html', {'payroll': payroll})

    try:
        import weasyprint
        pdf = weasyprint.HTML(string=html).write_pdf()
        return pdf
    except Exception as e:
        print("WARNING: WeasyPrint failed → returning HTML fallback")
        return html  # fallback HTML
