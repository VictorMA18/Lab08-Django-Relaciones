from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.template.loader import get_template
from django.urls import reverse
from .utils import render_to_pdf
from django.core.mail import send_mail
from django.conf import settings
import locale
from . import utils
# Create your views here.

def get_pdf(request, *args, **kwargs):
    template = get_template('invoice.html')
    context = {
        "invoice_number": 123,
        "customer_name": "Victor Mamani",
        "amount": 1399.9,
        "date": "Today",
    }
    html = template.render(context)
    pdf = render_to_pdf('invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s" %("12345")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def get_pdf_advanced(request):
    locale.setlocale(locale.LC_ALL, "")
    invoice_number = "007cae"
    context = {
        "customer_name": "Victor",
        "invoice_number": f"{invoice_number}",
        "amount": locale.currency(100_000, grouping=True),
        "date": "2024-15-06",
        "pdf_title": f"Invoice #{invoice_number}",
    }
    response = utils.render_to_pdf("invoice.html", context)
    if response.status_code == 404:
        raise HTTP404("Invoice not found")
    filename = f"Invoice_{invoice_number}.pdf"
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response


def emails(request):
    if request.method == 'POST':
        asunto = request.POST.get('subject', '')
        mensaje = request.POST.get('message', '')
        destinatario = request.POST.get('recipient', '')
        send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [destinatario], fail_silently=False)
        emails_url = reverse('emails')
        return HttpResponse(f'Correo enviado correctamente. <br> <p><a href="{emails_url}">Volver al menú principal</a></p>')
    return render(request, 'emails.html')

def index(request):
    return render(request, 'index.html')