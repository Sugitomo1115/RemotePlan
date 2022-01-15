import re
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404,JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import UserCreateForm
from remote_eventplan.models import UserManager, User, Plan, Like

# Create your views here.
def top(request):
    """トップ画面"""
    if request.method == 'POST':
        plan = Plan(name=request.POST['name'], target=request.POST['target'], person=request.POST['person'], category1=request.POST['category1'], category2=request.POST['category2'], time=request.POST['time'], tools=request.POST['tools'], help=request.POST['help'], outline=request.POST['outline'], posted_at=timezone.now(), create_user=request.user)
        plan.save()
        return redirect(top)
    plans = Plan.objects.order_by('-posted_at')
    if 'query' in request.GET:
        q_word = request.GET.get('query')
        if q_word == "" or q_word.isspace():
            plans = Plan.objects.all()
        else:
            search = q_word.replace("　"," ")
            search_list = search.split(" ")

            #(3)クエリを作る
            query = Q()
            for word in search_list:

                #空欄の場合は次のループへ
                if word == "":
                    continue

                #TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。
                query &= Q(Q(name__icontains=word) | Q(outline__icontains=word))

            #(4)作ったクエリを実行
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
        'plans': plans
    }
    return render(request, "remote_eventplan/top.html", context)

@login_required
def create(request):
    """企画制作画面"""
    return render(request, "remote_eventplan/create_plan.html")

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

@login_required
def update(request, plan_id):
    try:
        plan = Plan.objects.get(pk=plan_id)
    except Plan.DoesNotExist:
        raise Http404("Plan does not exist")

    if request.method == 'POST':
        plan.name = request.POST['name']
        plan.outline= request.POST['outline']
        plan.save()
        return redirect(detail, plan_id)

    context = {
        'plan': plan
    }
    return render(request, 'remote_eventplan/edit.html', context)

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
    form = UserCreateForm(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)

def login(request):
    return render(request, "remote_eventplan/login.html")

def privacy(request):
    return render(request, "remote_eventplan/privacy.html")

def privacy_check(request):
    return render(request, "remote_eventplan/privacy_check.html")