from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from recipes.models import Recipe
from ..forms import RegisterForm, LoginForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register.html', context={
        'form': form,
        'form_action': reverse('authors:register_create')
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'You user is created, please login')

        del (request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'),
        )

        if authenticated_user is not None:
            messages.success(request, "Your are logged")
            login(request, authenticated_user)
        else:
            messages.error(request, "Invalid credentials")
    else:
        messages.error(request, "Invalid username or password")

    return redirect(reverse('authors:dashboard'))


@login_required(redirect_field_name="next", login_url='authors:login')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        # print("Invalid user name", request.POST, request.user)
        return redirect(reverse('authors:login'))

    logout(request)
    messages.success(request, 'User logged out successfully')
    return redirect(reverse('authors:login'))


@login_required(redirect_field_name="next", login_url='authors:login')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user,
    )

    return render(
        request,
        'authors/pages/dashboard.html',
        context={
            'recipes': recipes,
        }
    )