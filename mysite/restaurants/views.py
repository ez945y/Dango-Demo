from django.shortcuts import render
from restaurants.models import Restaurant, Food, Comment
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from restaurants.forms import CommentForm
from django.contrib.sessions.models import Session
from django.contrib import auth


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')


def comment(request, id):
    if id:
        r = Restaurant.objects.get(id=id)
    else:
        return HttpResponseRedirect("/restaurants_list/")
    if request.POST:
        f = CommentForm(request.POST)
        if f.is_valid():
            visitor = f.cleaned_data['visitor']
            content = f.cleaned_data['content']
            email = f.cleaned_data['email']
            date_time = timezone.localtime(timezone.now())  # 擷取現在時間
            Comment.objects.create(
                visitor=visitor, email=email, content=content, date_time=date_time, restaurant=r)
            visitor, content, email = ('', '', '')
            f = CommentForm(initial={'content': '我沒意見'})
    else:
        f = CommentForm(initial={'content': '我沒意見'})
    return render(request, 'comments.html', locals())


def menu(request):
    if 'id' in request.GET and request.GET['id'] != '':
        restaurant = Restaurant.objects.get(id=request.GET['id'])
        return render(request, 'menu.html', locals())
    else:
        return HttpResponseRedirect("/restaurants_list/")


def meta(request):
    values = request.META.items()
    html = []
    for k, v in values:
        html.append('<tr><td>{0}</td><td>{1}</td></tr>'.format(k, v))
    return HttpResponse('<table>{0}</table>'.format('\n'.join(html)))


'''def menu(request, id):
    if id:
        restaurant = Restaurant.objects.get(id=id)
        return render(request, 'menu.html', locals())
    else:
        return HttpResponseRedirect("/restaurants_list/")
'''


def welcome(request):
    if 'user_name' in request.GET and request.GET['user_name'] != '':
        return HttpResponse('Welcome!~' + request.GET['user_name'])
    else:
        return render(request, 'welcome.html', locals())


def list_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants_list.html', locals())


def set_c(request):
    response = HttpResponse('Set your lucky_number as 8')
    response.set_cookie('lucky_number', 8)
    return response


def get_c(request):
    if 'lucky_number' in request.COOKIES:
        return HttpResponse('Your lucky_number is {0}'.format(request.COOKIES['lucky_number']))
    else:
        return HttpResponse('No cookies.')


def use_session(request):
    request.session['lucky_number'] = 8  # 設置lucky_number
    if 'lucky_number' in request.session:
        lucky_number = request.session['lucky_number']  # 讀取lucky_number
        response = HttpResponse('Your lucky_number is ' + str(lucky_number))
    return response


def session_test(request):
    sid = request.COOKIES['sessionid']
    sid2 = request.session.session_key
    s = Session.objects.get(pk=sid)
    s_info = 'Session ID:' + sid + '<br>SessionID2:' + sid2 + \
        '<br>Expire_date:' + str(s.expire_date) + \
        '<br>Data:' + str(s.get_decoded())
    return HttpResponse(s_info)


def list_restaurants(request):
    restaurants = Restaurant.objects.all()
    request.session['restaurants'] = restaurants  # 試著利用session保存模型物件
    return render(request, 'restaurants_list.html', locals())
