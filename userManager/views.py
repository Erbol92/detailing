from autoService.forms import AutoForm
from autoService.models import ModelAuto
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import ProfileForm, UserForm, LegalEntity
from .models import Profile


# Create your views here.

def auth_form_processor(request):
    creating_form = UserCreationForm()
    auth_form = AuthenticationForm()
    creating_form_legal = LegalEntity()
    return {
        'creating_form': creating_form,
        'auth_form': auth_form,
        'creating_form_legal': creating_form_legal,
    }


def request_auth_form_processor(request):
    creating_form = UserForm(request.POST or None)
    creating_form_legal = LegalEntity(request.POST or None)
    auth_form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        match request.POST.get('action'):
            case 'auth':
                if auth_form.is_valid():  # Проверяем форму на валидность
                    username = auth_form.cleaned_data.get('username')
                    password = auth_form.cleaned_data.get('password')
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
            case 'reg':
                if creating_form.is_valid():
                    user = creating_form.save()
                    login(request, user)
            case 'reg':
                if creating_form_legal.is_valid():
                    user = creating_form_legal.save()
                    login(request, user)
        return redirect('main')


def main(request):
    context = {
    }
    return render(request, 'main.html', context)


def user_logout(request):
    logout(request)
    return redirect('/')


def get_models(request):
    mark_id = request.GET.get('mark_id')
    models = ModelAuto.objects.filter(model_auto_id=mark_id).values('id', 'title')
    model_list = list(models)
    print(mark_id, models, model_list)
    return JsonResponse(model_list, safe=False)


@login_required
def profile(request):
    profile_form = ProfileForm(request.POST or None, instance=request.user.user_profile if Profile.objects.filter(
        user=request.user) else None, prefix='profile_form')
    user_form = UserForm(request.POST or None, instance=request.user, prefix='user_form')
    auto_form = AutoForm(request.POST or None, prefix='auto_form')
    print(request.POST)
    if 'action_user' in request.POST:
        if profile_form.is_valid():
            obj = profile_form.save(commit=False)
            obj.user = request.user
            obj.save()
        if user_form.is_valid():
            user_form.save()
        return redirect('profile')
    if 'action_auto' in request.POST and auto_form.is_valid():
        obj = auto_form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('profile')
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'auto_form': auto_form,
    }
    return render(request, 'profile.html', context)
