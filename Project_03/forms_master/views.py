from django.shortcuts import render
from .form import InputForm
from .models import FormsModel

def home_view(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            roll_number = form.cleaned_data['roll_number']
            password = form.cleaned_data['password']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            FormsModel.objects.create(title = title, description = description)
    else:
        form = InputForm()

    context = {'form': form}
    return render(request, "forms_master/home.html", context)