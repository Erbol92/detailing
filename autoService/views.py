from django.shortcuts import render

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
