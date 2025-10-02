from django.shortcuts import render
from django.http import HttpResponse
from .utils import generate_qr_code

def qr_code_view(request,url):
    link = url  # replace with dynamic link if needed
    qr_file = generate_qr_code(link)
    
    # Return as an image response
    response = HttpResponse(qr_file, content_type="image/png")
    response['Content-Disposition'] = 'inline; filename="qr_code.png"'
    return response
