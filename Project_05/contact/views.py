from django.shortcuts import render, HttpResponse
from .forms import ContactForm

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            return HttpResponse("Yay! You are a human!")
        else:
            return HttpResponse("OOPS! Bot suspected.")
    else:

        form = ContactForm
    return render(request, "contact/contact.html", {"form":form})