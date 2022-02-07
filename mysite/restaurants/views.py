from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from restaurants.models import Restaurant, Food, Comment
from restaurants.forms import CommentForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['request'] = request
        return self.render(request, context)

    def get_context_data(self, **kwargs):
        # 取得字典型態的Context
        context = super(IndexView, self).get_context_data(**kwargs)
        # 加入我們額外想要的時間參數
        context["time"] = timezone.now()
        return context


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', locals())


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


def user_can_comment(user):
    return user.is_authenticated and user.has_perm('restaurants.can_comment')


class CommentView(FormView, SingleObjectMixin):
    form_class = CommentForm
    template_name = 'comments.html'
    success_url = '/comment/'
    initial = {'content': '我沒意見'}
    model = Restaurant
    context_object_name = 'r'

    def form_valid(self, form):
        Comment.objects.create(
            visitor=form.cleaned_data['visitor'],
            email=form.cleaned_data['email'],
            content=form.cleaned_data['content'],
            date_time=timezone.localtime(timezone.now()),
            restaurant=self.get_object(),
        )
        return self.render(request, self.get_context_data(
            form=self.form_class(initial=self.initial)
        ))

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        return super(CommentView, self).get_context_data(object=self.object, **kwargs)
        # return super(CommentView, self).form_valid(form)

    @method_decorator(user_passes_test(user_can_comment, login_url='/accounts/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(CommentView, self).dispatch(request, *args, **kwargs)


@permission_required('restaurants.can_comment', login_url='/accounts/login/')
def comment(request, id):
    if request.user.is_authenticated and request.user.has_perm('restaurants.can_comment'):
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
    else:
        return HttpReponseRedirect('/restaurants_list/')


class MenuView(DetailView):
    model = Restaurant
    template_name = 'menu.html'
    context_object_name = 'restaurant'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MenuView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        try:
            return super(MenuView, self).get(self, request, pk=pk, *args, **kwargs)
        except Http404:
            return HttpResponseRedirect('/restaurants_list/')


def menu(request, id=1):
    if id:
        restaurant = Restaurant.objects.get(id=id)
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


class RestaurantsView(ListView):
    model = Restaurant
    template_name = 'restaurants_list.html'
    context_object_name = 'restaurants'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(RestaurantsView, self).dispatch(request, *args, **kwargs)


def list_restaurants(request):
    """if not request.user.is_authenticated:
        return rende(request,'error.html')"""
    """request.session['restaurants'] = restaurants"""
    restaurants = Restaurant.objects.all()
    print(request.user.user_permissions.all())
    return render(request, 'restaurants_list.html', locals())


def list_users(request):
    users = auth.models.User.objects.all()
    return render(request, 'users_list.html', locals())


@login_required
def list(request, model):
    objs = model.objects.all()
    return render(request, '{0}s_list.html'.format(model.__name__.lower()), locals())


def test(request):
    return render(request, 'test.html', locals())


class AdvTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.context)


class MyView(AdvTemplateView):
    template_name = 'index.html'
    # 利用一個tricky的技巧取得context
    context = AdvTemplateView().get_context_data()
    context['hello'] = '123'  # 提供了hello變量
