from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ToDoForm
from .models import ToDo

def index(request):
    item_list = ToDo.objects.order_by("-date")
    if request.method == "POST":
        form = ToDoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("todo")
    form = ToDoForm

    page = {
        "forms":form,
        "list":item_list,
        "title":"TO-DO LIST"
    }
    return render(request, "ToDoApp/index.html", page)

def remove(request, item_id):
    item = ToDo.objects.get(id=item_id)
    title = item.title
    item.delete()
    messages.info(request, f"{title} was removed")
    return redirect("todo")