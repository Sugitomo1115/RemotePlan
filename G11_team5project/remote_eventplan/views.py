from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import Http404,JsonResponse
from django.utils import timezone
from django.db.models import Q

from remote_eventplan.models import Plan

# Create your views here.
def top(request):
    """トップ画面"""
    if request.method == 'POST':
        plan = Plan(name=request.POST['name'], target=request.POST['target'], person=request.POST['person'], time=request.POST['time'], tools=request.POST['tools'], help=request.POST['help'], outline=request.POST['outline'], posted_at=timezone.now())
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

            query = Q()
            for word in search_list:

                if word == "":
                    continue

                query &= Q(Q(name__icontains=word) | Q(outline__icontains=word))

            plans = Plan.objects.filter(query)
        plans = plans.order_by('-posted_at')
    
    if 'select' in request.GET:
        s_word = request.GET.get('select')
        if s_word == "":
            plans = Plan.objects.all()
        else:
            plans = Plan.objects.filter(Q(target__icontains=s_word))
        plans = plans.order_by('-posted_at')

    if 'sort' in request.GET:
        if request.GET['sort']=='date':
            plans=Plan.objects.order_by('-posted_at')
        elif request.GET['sort']=='like':
            plans=Plan.objects.order_by('-like')
    context = {
        'plans': plans
    }
    return render(request, "remote_eventplan/top.html", context)

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

def delete(request, plan_id):
    try:
        plan = Plan.objects.get(pk=plan_id)
    except Plan.DoesNotExist:
        raise Http404("Plan does not exist")
    
    plan.delete()
    return redirect(top)

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
        plan.like+=1
        plan.save()
    except Plan.DoesNotExist:
            raise Http404("Plan does not exist")
    return redirect(detail,plan_id)

def api_like(request, plan_id):
	try:
		plan=Plan.objects.get(pk=plan_id)
		plan.like+=1
		plan.save()
	except Plan.DoesNotExist:
		raise Http404("Plan does not exist")
	result={'id':plan_id, 'like':plan.like}
	return JsonResponse(result)

def get_queryset(self):
        q_word = self.request.GET.get('query')
 
        if q_word:
            plans = Plan.objects.filter(
                Q(name__icontains=q_word) | Q(outline__icontains=q_word))
        else:
            plans = Plan.objects.all()
        return plans