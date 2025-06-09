from django.template.loader import render_to_string

def generate_overpayment_pdf(calculation):
    html = render_to_string('overpayment_template.html', {'calculation': calculation})

    try:
        # Import WeasyPrint only inside try block → avoids crash at import time
        import weasyprint
        pdf = weasyprint.HTML(string=html).write_pdf()
        return pdf
    except Exception as e:
        print("WARNING: WeasyPrint failed → returning HTML fallback")
        return html  # return raw HTML string
