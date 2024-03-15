# Create your views here.
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from common.forms import UserForm

#'''
# SMTP 관련 인증
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
#'''

from django.urls import reverse

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            
            # Generate the activation link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activate_url = reverse('common:activate', kwargs={'uidb64': uid, 'token': token})
            activation_link = request.build_absolute_uri(activate_url)
            
            # Send the activation email with the activation link
            username = user.username
            message = f"{username}님, E-tickets입니다. 아래 링크를 클릭하여 계정을 활성화하세요: {activation_link}"
            mail_title = "계정 활성화 확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
         
# 계정 활성화 함수(토큰을 통해 인증)
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('index')
    return render(request, 'kaist/notification_list.html', {'error' : '계정 활성화 오류'})