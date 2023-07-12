from django.shortcuts import render
from authors.forms import RegisterForm


def register(request):
    form = RegisterForm()

    return render(request, 'authors/pages/register.html', context={
        'form': form,
    })
