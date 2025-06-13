from django.shortcuts import render, redirect, get_object_or_404
from .models import LedgerEntry
from .forms import LedgerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import pandas as pd
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO

def signup_view(request):
    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    form = LedgerForm()
    entries = LedgerEntry.objects.all()

    # Filter logic
    if request.GET.get("client"):
        entries = entries.filter(client_name__icontains=request.GET["client"])
    if request.GET.get("date"):
        entries = entries.filter(date=request.GET["date"])

    total_cr = sum(e.credit for e in entries)
    total_dr = sum(e.debit for e in entries)
    total_rem = sum(e.remaining() for e in entries)

    if request.method == "POST":
        form = LedgerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'home.html', {
        "form": form,
        "entries": entries,
        "total_cr": total_cr,
        "total_dr": total_dr,
        "total_rem": total_rem
    })

@login_required
def delete_entry(request, id):
    LedgerEntry.objects.get(id=id).delete()
    return redirect('home')

@login_required
def edit_entry(request, id):
    entry = get_object_or_404(LedgerEntry, id=id)
    if request.method == 'POST':
        form = LedgerForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = LedgerForm(instance=entry)
    return render(request, 'edit.html', {"form": form, "id": id})

@login_required
def export_excel(request):
    df = pd.DataFrame(list(LedgerEntry.objects.all().values()))
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ledger.xlsx"'
    df.to_excel(response, index=False)
    return response

@login_required
def export_pdf(request):
    entries = LedgerEntry.objects.all()
    total_cr = sum(e.credit for e in entries)
    total_dr = sum(e.debit for e in entries)
    total_rem = sum(e.remaining() for e in entries)
    template = get_template('pdf.html')
    html = template.render({"entries": entries, "total_cr": total_cr, "total_dr": total_dr, "total_rem": total_rem})
    response = BytesIO()
    pisa.CreatePDF(html, dest=response)
    return HttpResponse(response.getvalue(), content_type='application/pdf')
