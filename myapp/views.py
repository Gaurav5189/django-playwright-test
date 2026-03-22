from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ContactForm, DemoItemForm
from .models import DemoItem


def home(request):
    return render(request, "myapp/home.html")


def item_list(request):
    items = DemoItem.objects.all()
    return render(request, "myapp/item_list.html", {"items": items})


def item_add(request):
    if request.method == "POST":
        form = DemoItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item saved.")
            return redirect("item_list")
    else:
        form = DemoItemForm()
    return render(request, "myapp/item_form.html", {"form": form})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(
                request,
                f"Thanks, {form.cleaned_data['name']}! Your message was received (demo only).",
            )
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "myapp/contact.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "myapp/dashboard.html")
