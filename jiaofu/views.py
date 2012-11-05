#coding=utf-8
import csv
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# from django.utils.encoding import smart_unicode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader, Context
from jiaofu.models import Zixun
from jiaofu.forms import ZixunForm


def list(request):
    zixun = Zixun.objects.filter().order_by('-dateline')

    paginator = Paginator(zixun, 25)
    page = request.GET.get('page')
    try:
        zixun_list = paginator.page(page)
    except PageNotAnInteger:
        zixun_list = paginator.page(1)
    except EmptyPage:
        zixun_list = paginator.page(paginator.num_pages)
    return render(request, 'jiaofu/list.html', {'zixun_list': zixun_list, })


def create(request):
    form = ZixunForm()
    if request.method == "POST":
        form = ZixunForm(request.POST)
        if form.is_valid():
            zixun = form.save(commit=False)
            zixun.typer = request.user
            zixun.year = datetime.today().year
            zixun.month = datetime.today().month
            zixun.save()
            return HttpResponseRedirect(reverse('zixun_list'))
    return render(request, 'jiaofu/create.html', {'form': form})


def update(request, id):
    zixun = get_object_or_404(Zixun, pk=id)
    form = ZixunForm(instance=zixun)
    if request.method == "POST":
        form = ZixunForm(request.POST, instance=zixun)
        if form.is_valid():
            zixun = form.save(commit=False)
            zixun.typer = request.user
            zixun.save()
            return HttpResponseRedirect(reverse('zixun_list'))
    return render(request, 'jiaofu/create.html', {'form': form})



def view(request, id):
    zixun = get_object_or_404(Zixun, pk=id)
    form = ZixunForm(instance=zixun)
    return render(request, 'jiaofu/view.html', {'form': form})


def delete(request, id):
    zixun = get_object_or_404(Zixun, pk=id)
    zixun.delete()
    return HttpResponseRedirect('/jiaofu/list/')
