from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
import pandas as pd
from .forms import UploadFileForm

def handle_uploaded_file(f):
    if f.name.endswith('.csv'):
        data = pd.read_csv(f)
    elif f.name.endswith('.xlsx'):
        data = pd.read_excel(f)
    else:
        return None
    
    # Generate summary in desired format
    summary = data[['Cust State', 'Cust Pin', 'DPD']].drop_duplicates().to_html(classes="table table-striped")
    return summary

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            summary = handle_uploaded_file(request.FILES['file'])
            return render(request, 'fileupload/summary.html', {'summary': summary})
    else:
        form = UploadFileForm()
    return render(request, 'fileupload/upload.html', {'form': form})

def pdf_summary(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            summary = handle_uploaded_file(request.FILES['file'])
            context = {'summary': summary}
            return render_to_pdf('fileupload/summary.html', context)
    return HttpResponse("Invalid request")
