from django.shortcuts import render
from voiceService.models import Voice, VoiceAssignment
from userManager.models import ScheduleRecord
from autoService.models import PriceService
from datetime import datetime, timedelta
import pandas as pd
from django.db.models import Count, Q, F, Sum, OuterRef, Subquery
from django.http import HttpResponse


# Create your views here.
def report_main(request):
    context = {
        'title':'отчет'
    }
    return render(request, 'report/report_main.html', context)

def user_voice_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date()
    # Запрос для получения количества обращений, сгруппированных по тематике
    inquiries = Voice.objects.filter(created_at__gte=start_date, created_at__lt=end_date).values('topic__title').annotate(count=Count('id')).order_by('topic__title')

    # Подготовка данных для DataFrame
    data = {
        'Виды обращений': [inquiry['topic__title'] for inquiry in inquiries],
        'Количество обращений': [inquiry['count'] for inquiry in inquiries],
    }

    # Создание DataFrame
    df = pd.DataFrame(data)

    # Создание HTTP-ответа с файлом Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="client_inquiries_report_{datetime.now()}.xlsx"'

    # Запись DataFrame в ответ
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

def profit_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date()
    # Получаем все записи расписания
    schedule_records = ScheduleRecord.objects.filter(date__gte=start_date, date__lt=end_date,status='closed').select_related('service', 'auto')

    # Создаем словарь для хранения итоговой прибыли по каждой услуге
    profit_by_service = {}

    # Проходим по всем записям расписания
    for record in schedule_records:
        # Получаем тип кузова автомобиля
        body_type = record.auto.model.body_type
        
        # Получаем цену услуги для данного типа кузова
        price_service = PriceService.objects.filter(service=record.service, auto_body=body_type).first()
        if price_service:
            # Если цена услуги найдена, добавляем ее к итоговой прибыли
            service_title = record.service.title
            profit = price_service.price
            
            if service_title in profit_by_service:
                profit_by_service[service_title] += profit
            else:
                profit_by_service[service_title] = profit
    # Подготовка данных для DataFrame
    data = {
        'Услуга': [record for record in profit_by_service.keys()],
        'Общая прибыль': [record for record in profit_by_service.values()],
    }

    # Создание DataFrame
    df = pd.DataFrame(data)

    # Создание HTTP-ответа с файлом Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="profit_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'

    # Запись DataFrame в ответ
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response


def master_service_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date()
    # Получаем все записи расписания
    schedule_records = ScheduleRecord.objects.filter(date__gte=start_date, date__lt=end_date).select_related('service', 'user')

    # Создаем словарь для хранения количества записей по каждой услуге для каждого мастера
    report_data = {}

    # Проходим по всем записям расписания
    for record in schedule_records:
        master_name = record.user.username  # Или используйте любое другое поле для имени мастера
        service_title = record.service.title
        
        # Создаем ключ для мастера и услуги
        key = (master_name, service_title)
        
        # Увеличиваем счетчик для данной услуги у данного мастера
        if key in report_data:
            report_data[key]['count'] += 1
            if record.status == 'closed':
                report_data[key]['closed_count'] += 1
        else:
            report_data[key] = {'count': 1, 'closed_count': 1 if record.status == 'closed' else 0}

    # Подготовка данных для DataFrame
    data = {
        'Мастер': [key[0] for key in report_data.keys()],
        'Услуга': [key[1] for key in report_data.keys()],
        'Количество записей': [info['count'] for info in report_data.values()],
        'Количество закрытых записей': [info['closed_count'] for info in report_data.values()],
    }

    # Создание DataFrame
    df = pd.DataFrame(data)

    # Создание HTTP-ответа с файлом Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="master_service_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'

    # Запись DataFrame в ответ
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

from django.utils import translation
translation.activate('ru')

def generate_inquiries_report(request):
    current_year = datetime.now().year  # получаем текущий год
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date()
    # Данные по месяцам текущего года
    months_data = []
    # Фильтруем данные за каждый месяц отдельно
    oral_inquiries_monthly = Voice.objects.filter(created_at__gte=start_date, created_at__lt=end_date, source='call').count()
    written_inquiries_monthly = Voice.objects.filter( Q(source='whatsapp') | Q(source='instagram') | Q(source='site'), created_at__gte=start_date, created_at__lt=end_date).count()

    # Переадресованные обращения
    oral_redirects_monthly = VoiceAssignment.objects.filter(voice__created_at__gte=start_date, voice__created_at__lt=end_date, voice__source='call').values('voice').annotate(count=Count('id')).filter(count__gt=2).count()
    written_redirects_monthly = VoiceAssignment.objects.filter(voice__created_at__gte=start_date, voice__created_at__lt=end_date, voice__in=Voice.objects.filter(Q(source='whatsapp') | Q(source='instagram') | Q(source='site'))).values('voice').annotate(count=Count('id')).filter(count__gt=2).count()

    # Рассмотрение письменных обращений без нарушений срока
    timely_written_inquiries_monthly = Voice.objects.filter(
        Q(source='whatsapp') | Q(source='instagram') | Q(source='site'),
        created_at__gte=start_date, created_at__lt=end_date,
        created_at__lte=F('created_at') + timedelta(days=5),
    ).annotate(is_redirected=Count('assignments')).filter(is_redirected=0).count()

    # Обращения с нарушением срока рассмотрения
    late_written_inquiries_monthly = written_redirects_monthly - timely_written_inquiries_monthly

    # Формируем строку отчета для каждого месяца
    months_data.append({
        'Месяц': f'{start_date}/{end_date}',  # Название месяца и год
        'Общее количество устных обращений': oral_inquiries_monthly,
        'Переадресовано устных обращений': oral_redirects_monthly,
        'Общее количество письменных обращений': written_inquiries_monthly,
        'Переадресовано письменных обращений': written_redirects_monthly,
        'Рассмотрено вовремя': timely_written_inquiries_monthly,
        'Просрочено': late_written_inquiries_monthly
    })

    # Создаем DataFrame
    df = pd.DataFrame(months_data)

    # Удаляем строки, где нет данных по обращению (например, пустые месяцы)
    df = df.dropna(how='all', subset=['Общее количество устных обращений', 'Общее количество письменных обращений'])

    # Генерируем файл Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="report_{current_year}-{datetime.now().strftime("%m-%d")}.xlsx"'

    # Сохраняем DataFrame в Excel-файл
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response