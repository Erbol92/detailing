import json
from datetime import time, datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from userManager.models import ScheduleWork, ScheduleRecord, CustomUser
from .forms import ClientListForm

from .models import Service


# Create your views here.

def service(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'service.html', context)


def service_detail(request, pk: int):
    object = Service.objects.filter(id=pk).first()
    context = {
        'object': object,
    }
    return render(request, 'service_detail.html', context)


def calendar_events(request):
    services = Service.objects.all()
    context = {
        'services': services,
        'form': ClientListForm(),
    }
    return render(request, 'calendar_events_new.html', context)


def get_free_time_for_next_30_days(user):
    # Определите рабочие часы
    work_start = time(9, 0)  # 9:00
    work_end = time(17, 0)  # 17:00

    # Получаем текущую дату
    today = datetime.now().date()
    free_time_by_date = {}

    # Итерируемся по 30 дням от текущей даты
    for i in range(30):
        current_date = today + timedelta(days=i)

        # Получите все рабочие дни для пользователя на текущую дату
        work_days = ScheduleWork.objects.filter(user=user, date=current_date)

        # Если нет рабочих дней, пропускаем этот день
        if not work_days.exists():
            continue

        # Получите все занятые записи для пользователя на текущую дату
        busy_records = ScheduleRecord.objects.filter(user=user, date=current_date)

        # Создайте список занятых интервалов
        busy_intervals = []
        for record in busy_records:
            busy_intervals.append((record.start_time, record.end_time))

        # Сортируем занятые интервалы по времени начала
        busy_intervals.sort(key=lambda x: x[0])

        # Определяем свободные интервалы
        free_intervals = []
        current_start = work_start

        for start, end in busy_intervals:
            # Если текущее начало меньше времени начала занятого интервала, добавляем свободный интервал
            if current_start < start:
                free_intervals.append((current_start, start))
            # Обновляем текущее начало до конца занятого интервала, если оно больше
            current_start = max(current_start, end)

        # Проверяем, есть ли свободное время после последнего занятого интервала
        if current_start < work_end:
            free_intervals.append((current_start, work_end))

        # Сохраняем свободные интервалы для текущей даты
        free_time_by_date[current_date] = free_intervals

    return free_time_by_date


def get_schedule_work(request):
    service_id: int = request.GET.get('service_id')  # Получаем ID услуги из запроса
    try:
        service = Service.objects.get(id=service_id)  # Получаем услугу по ID
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Услуга не найдена'}, status=404)

    masters = service.user.all()  # Получаем всех мастеров, предоставляющих эту услугу
    today = datetime.now().date()
    schedule_data = {}
    for master in masters:
        schedules = ScheduleWork.objects.filter(user=master,date__gte=today)  # Получаем график работы мастера
        schedule_data[master.id] = {
            'name': master.username,
            'schedules': [
                {
                    'date': schedule.date,
                }
                for schedule in schedules
            ],
            'service_id': service_id,
        }
    return JsonResponse(schedule_data)


def get_schedule_record(request):
    user_id: int = request.GET.get('user_id')
    date_str: str = request.GET.get('date')
    date = datetime.strptime(date_str, "%d.%m.%Y")
    try:
        records = ScheduleRecord.objects.filter(user_id=user_id, date=date)  # Получаем услугу по ID
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Услуга не найдена'}, status=404)
    # if not records.exists():
    # Если записей нет, возвращаем возможность выбрать время
    return JsonResponse({
        'message': 'Записей нет. Выберите время.' if not records.exists() else 'Доступные промежутки:',
        'time_selection': True,
        'available_slots': get_available_time_slots() if not records.exists() else get_available_time_slots(records),
        'user_id': user_id,
        'date_str': date_str,
    })


def get_available_time_slots(records=None):
    # Определяем рабочие часы
    start_hour = 9
    end_hour = 18
    time_slots = []

    # Создаем список всех возможных временных промежутков
    for hour in range(start_hour, end_hour):
        for minute in [0, 30]:  # Каждые 30 минут
            start_time = time(hour, minute)
            end_time = time(hour, minute + 30) if minute + 30 < 60 else time(hour + 1, 0)

            # Проверяем, заняты ли временные промежутки
            if records:
                is_occupied = any(record.start_time < end_time and record.end_time > start_time for record in records)
                time_slots.append({
                    'slot': f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}",
                    'occupied': is_occupied
                })
            else:
                time_slots.append({
                    'slot': f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}",
                    'occupied': False
                })
    return time_slots


def add_record_time(request):
    try:
        # Получаем данные из запроса
        data = json.loads(request.body)
        start_time = data.get('startTime')
        end_time = data.get('endTime')
        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()
        date = data.get('date')
        date = datetime.strptime(date, "%d.%m.%Y")
        service_id = data.get('serviceId')
        user_id = data.get('userId')
        client_id = data.get('clientId')
        master = CustomUser.objects.get(id=user_id)
        client = CustomUser.objects.get(id=client_id)
        service = Service.objects.get(id=service_id)
        record, created = ScheduleRecord.objects.get_or_create(
            user=master,
            start_time=start_time,
            end_time=end_time,
            service=service,
            date=date,
            client=client
        )

        if created:
            return JsonResponse({'message': 'Запись успешно добавлена!'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

