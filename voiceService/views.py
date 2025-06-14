from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.db.models import OuterRef, Subquery, Max
from .forms import VoicenForm, VoiceAssignmentForm, VoiceUserForm
from .models import Voice, VoiceAssignment
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from userManager.models import CustomUser
 
def voice_register(request):
    form = VoicenForm(request.POST or None)
    expired = request.GET.get('expired')
    class_expired=''
    if expired:
        date_threshold = timezone.now() - timedelta(days=1)
        voices = Voice.objects.filter(status=False,created_at__lt=date_threshold).order_by('-created_at')
        class_expired='class_expired'
    else:
        print(CustomUser.objects.filter(groups__name='Менеджер', username=request.user),request.user.is_superuser)
        if CustomUser.objects.filter(groups__name='Менеджер', username=request.user) or request.user.is_superuser:
            voices = Voice.objects.filter(status=False).order_by('-created_at')
        else:
            # Подзапрос для получения последнего назначения для каждой заявки
            last_assignment_subquery = VoiceAssignment.objects.filter(
                voice=OuterRef('pk')
            ).order_by('-assigned_at')

            # Получаем все заявки, где последний назначенный сотрудник - текущий пользователь
            voices = Voice.objects.filter(
                status=False,
                assignments__in=Subquery(last_assignment_subquery.values('id')[:1]),
                assignments__employee=request.user
            ).order_by('-created_at').distinct()
    paginator = Paginator(voices, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if form.is_valid():
        voice = form.save()
        VoiceAssignment.objects.create(voice=voice,employee=request.user)
        return redirect('voice_register')
    context = {
        'form': form,
        'page_obj': page_obj,
        'class_expired':class_expired,
    }
    return render(request, 'voice_register.html', context)


class VoiceDetailView(DetailView):
    model = Voice
    template_name = 'voice_detail.html'  # Укажите путь к вашему шаблону
    context_object_name = 'object'  # Имя контекстного объекта, доступного в шаблоне

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voice = self.object  # Получаем текущий объект Voice
        masters = CustomUser.objects.filter(groups__name='Мастер').distinct()
        context['voice_assignments'] = VoiceAssignment.objects.filter(voice=voice).order_by('-assigned_at')  # Фильтруем назначения
        context['form'] = VoiceAssignmentForm()  # Добавляем форму в контекст
        context['masters'] = masters
        return context


def create_update_voice(request, voice_id: int):
    form = VoiceAssignmentForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        voice = Voice.objects.get(id=voice_id)
        obj.voice = voice
        obj.save()
        return redirect(voice.get_absolute_url())
    return render(request, 'voice_register.html')

def closing_voice(request, voice_id: int):
    voice = Voice.objects.get(id=voice_id)
    voice.status=True
    voice.save()
    messages.success(request, 'обращение зарыто')
    return redirect('voice_register')
    
def voice_from_user(request):
    
    if request.user.is_authenticated:
        voices = Voice.objects.filter(client=request.user).order_by('-created_at')
        paginator = Paginator(voices, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        voices = None
        page_obj = None

    form = VoiceUserForm(data = request.POST or None,user=request.user)
    if form.is_valid():
        voice = form.save(commit=False)
        if request.user.is_authenticated:
            voice.client=request.user
        voice.source = 'site'
        voice.save()
        VoiceAssignment.objects.create(voice=voice)
        return redirect('voice_from_user')
    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'user_voice_register.html', context)