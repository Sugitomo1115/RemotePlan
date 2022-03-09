from multiprocessing import context
import re
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404,JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserCreateForm, LoginForm
from remote_eventplan.models import UserManager, User, Plan, Like, Category

# Create your views here.
def top(request):
    """トップ画面"""
    if request.method == 'POST':
        plan = Plan(name=request.POST['name'], target=request.POST['target'], person=request.POST['person'], category1=request.POST['category1'], category2=request.POST['category2'], time=request.POST['time'], tools=request.POST['tools'], help=request.POST['help'], outline=request.POST['outline'], posted_at=timezone.now(), create_user=request.user)
        plan.save()
        return redirect(top)
    plans = Plan.objects.order_by('-posted_at')
    categories = Category.objects.all
    if 'query' in request.GET:
        q_word = request.GET.get('query')
        if q_word == "" or q_word.isspace():
            plans = Plan.objects.all()
        else:
            search = q_word.replace("　"," ")
            search_list = search.split(" ")

            #クエリを作る
            query = Q()
            for word in search_list:

                #空欄の場合は次のループへ
                if word == "":
                    continue

                #OR検索
                query &= Q(Q(name__icontains=word) | Q(outline__icontains=word))

            #作ったクエリを実行
            plans = Plan.objects.filter(query)
        plans = plans.order_by('-posted_at')
    
    if 'select' in request.GET or 'searchcategory' in request.GET:
        select_query = Q()
        target_word = request.GET.get('select')
        category_word = request.GET.get('searchcategory')
        
        select_query = Q(Q(target__icontains=target_word) & Q(Q(category1__icontains=category_word) | Q(category2__icontains=category_word)))

        plans = Plan.objects.filter(select_query)
        plans = plans.order_by('-posted_at')

    if 'sort' in request.GET:
        if request.GET['sort']=='date':
            plans=plans.order_by('-posted_at')
        elif request.GET['sort']=='like_num':
            plans=plans.order_by('-like_num')
    context = {
        'plans': plans,
        'categories':categories
    }
    return render(request, "remote_eventplan/top.html", context)

@login_required
def create(request):
    """企画制作画面"""
    if request.method == 'POST':
        category = Category(category_name=request.POST['category_name'])
        category.save()
        return redirect(create)
    categories = Category.objects.all
    context = {
        'categories':categories
    }
    return render(request, "remote_eventplan/create_plan.html", context)

@login_required
def add_category(request):
    return render(request, "remote_eventplan/add_category.html")

def detail(request, plan_id):
    """企画詳細画面"""
    try:
        plan = Plan.objects.get(pk=plan_id)
    except Plan.DoesNotExist:
        raise Http404("Plan does not exist")
    context = {
        'plan': plan
    }
    return render(request, "remote_eventplan/detail_plan.html", context)

@login_required
def delete(request, plan_id):
    try:
        plan = Plan.objects.get(pk=plan_id)
        if request.user.id == plan.create_user.id:
            plan.delete()
            return redirect(top)
        else:
            context = {
                'plan': plan
            }
            messages.error(request, 'この操作は企画制作者のみ可能です')
            return render(request, "remote_eventplan/detail_plan.html", context)
    except Plan.DoesNotExist:
        raise Http404("Plan does not exist")

def like(request, plan_id):
    try:
        plan=Plan.objects.get(pk=plan_id)
        plan.like_num+=1
        plan.save()
    except Plan.DoesNotExist:
            raise Http404("Plan does not exist")
    return redirect(detail,plan_id)

@login_required
def api_like(request, plan_id):
    try:
        plan=Plan.objects.get(pk=plan_id)
        is_like = Like.objects.filter(post_user__pk=request.user.id, post_plan__pk=plan_id).count()
        if is_like > 0:
            liking = Like.objects.get(post_user__pk=request.user.id, post_plan__pk=plan_id)
            liking.delete()
            plan.like_num-=1
            plan.save()
        else:
            post_like = Like(post_user=request.user, post_plan=plan)
            plan.like_num+=1
            post_like.save()
            plan.save()
    except Plan.DoesNotExist:
        raise Http404("Plan does not exist")
    result={'id':plan_id, 'like':plan.like_num}
    return JsonResponse(result)

def get_queryset(self):
        q_word = self.request.GET.get('query')
 
        if q_word:
            plans = Plan.objects.filter(
                Q(name__icontains=q_word) | Q(outline__icontains=q_word))
        else:
            plans = Plan.objects.all()
        return plans

@require_POST
def regist_save(request):
    form = UserCreateForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(top)

    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)
        

def signup(request):
    """サインアップ画面"""
    form = UserCreateForm(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)

def privacy(request):
    """利用規約画面"""
    return render(request, "remote_eventplan/privacy.html")

def privacy_check(request):
    """ユーザー登録前の利用規約確認画面"""
    return render(request, "remote_eventplan/privacy_check.html")

def login(request):
    """ログイン画面"""
    return render(request, "remote_eventplan/login.html")

#改造したLoginView
class CustomLoginView(LoginView):
    form_class = LoginForm

    #GETをした際にユーザー名を記憶していれば初期値に設定
    def get(self, request, *args, **kwargs):
        if 'form_data' in self.request.session:
            saved_username = request.session.get('form_data')
            form = LoginForm(initial=dict(username = saved_username))
            context = {
                'form': form
            }
        else:
            form = LoginForm()
            context = {
                'form': form
            }
        return render(self.request, self.template_name, context)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        #ユーザー名の記憶するかのチェック
        if(self.request.POST.get('saveflag')):
            self.request.session['form_data'] = self.request.POST.get('username')
            self.request.session['saveflag'] = True
        else:
            self.request.session['saveflag'] = False
        return HttpResponseRedirect(self.get_success_url())

#改造したLogoutView
class CustomLogoutView(LogoutView):

    def Custom_auth_logout(self, request):
        """
        Remove the authenticated user's ID from the request and flush their session
        data.
        """
        # Dispatch the signal before the user is logged out so the receivers have a
        # chance to find out *who* logged out.
        user = getattr(request, "user", None)
        if not getattr(user, "is_authenticated", True):
            user = None
        user_logged_out.send(sender=user.__class__, request=request, user=user)
        #ログイン時にチェックを入れていた場合はユーザー名を記憶
        if request.session.get('saveflag'):
            username = request.session.get('form_data')
            request.session.flush()
            request.session['form_data'] = username
        else:
            request.session.flush()
        if hasattr(request, "user"):
            from django.contrib.auth.models import AnonymousUser

            request.user = AnonymousUser()

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self.Custom_auth_logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)