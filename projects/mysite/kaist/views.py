from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Notification
from django.core.paginator import Paginator


def index(request):
    page = request.GET.get('page', '1')  # 페이지
    notification_list = Notification.objects.order_by('-create_date')
    context = {'notification_list': notification_list}
    paginator = Paginator(notification_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'notification_list': page_obj}
    return render(request, 'kaist/notification_list.html', context)

def detail(request, notification_id):
    question = get_object_or_404(Notification, pk=notification_id)
    context = {'notification': question}
    return render(request, 'kaist/notification_detail.html', context)