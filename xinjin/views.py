#coding=utf-8
# import xlrd
import csv
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# from django.utils.encoding import smart_unicode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader, Context
from xinjin.models import Xinjin, XinjinDan
from xinjin.forms import XinjinForm, XinjinDanForm


def xinjin_smart_float(f):
    try:
        return float(f)
    except:
        return 0


def list(request):
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    first_name = request.GET.get('first_name', '')
    xiangmu = request.GET.get('xiangmu', '')
    querystr = "year=%s&month=%s&first_name=%s&xiangmu=%s" % (
        year, month, first_name, xiangmu)
    args = {}

    if year:
        args['year'] = year
    if month:
        args['month'] = month

    xinjin = XinjinDan.objects.filter(**args).order_by('-dateline')

    paginator = Paginator(xinjin, 25)
    page = request.GET.get('page')
    try:
        xinjin_list = paginator.page(page)
    except PageNotAnInteger:
        xinjin_list = paginator.page(1)
    except EmptyPage:
        xinjin_list = paginator.page(paginator.num_pages)
    return render(request, 'xinjin/list.html', {'xinjin_list': xinjin_list, 'querystr': querystr, "args": args})


def create(request):
    form = XinjinDanForm()
    if request.method == "POST":
        form = XinjinDanForm(request.POST)
        if form.is_valid():
            xinjin = form.save(commit=False)
            xinjin.bianhao = xinjin.bianhao.upper()
            xinjin.typer = request.user
            xinjin.year = datetime.today().year
            xinjin.month = datetime.today().month
            xinjin.save()
            return HttpResponseRedirect(reverse('xinjin_list', args=[xinjin.id]))
    return render(request, 'xinjin/create.html', {'form': form})


def update(request, id):
    xinjin = get_object_or_404(XinjinDan, pk=id)
    form = XinjinDanForm(instance=xinjin)
    if request.method == "POST":
        form = XinjinDanForm(request.POST, instance=xinjin)
        if form.is_valid():
            xinjin = form.save(commit=False)
            xinjin.typer = request.user
            xinjin.save()
            return HttpResponseRedirect(reverse('xinjin_list', args=[id]))
    return render(request, 'xinjin/create.html', {'form': form})


def delete(request, id):
    xinjin = get_object_or_404(XinjinDan, pk=id)
    xinjin.delete()
    return HttpResponseRedirect('/xinjin/list/')


def xinjin_list(request, id):
    xinjindan = get_object_or_404(XinjinDan, pk=id)

    xinjin_list = xinjindan.xinjin.filter().order_by('-id')
    # xinjin_total = xinjindan.xinjin.filter().values('xinjindan').annotate(y=Sum("yingfa"), b=Sum("baoxian"), g=Sum("gongjijin"))

    if request.GET.get('excel'):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="' + xinjindan.bianhao + '.csv"'
        writer = csv.writer(response)
        writer.writerow([u'序号'.encode('gbk'), u'编号'.encode('gbk'), u'项目'.encode('gbk'),
                         u'姓名'.encode('gbk'), u'身份证号码'.encode('gbk'), u'年份'.encode('gbk'),
                         u'月份'.encode('gbk'), u'应发'.encode('gbk'), u'保险'.encode('gbk'), u'公积金'.encode('gbk'),
                         u'类型'.encode('gbk')])
        for i, xinjin in enumerate(xinjin_list):
            setattr(xinjin, 'get_username_gbk', xinjin.user.first_name.encode('gbk'))
            setattr(xinjin, 'get_xiangmu_gbk', xinjin.xinjindan.xiangmu.encode('gbk'))
            setattr(xinjin, 'get_leixing_gbk', xinjin.leixing.encode('gbk'))
            writer.writerow([i + 1, xinjin.xinjindan.bianhao, xinjin.get_xiangmu_gbk,
                             xinjin.get_username_gbk, '="' + xinjin.user.last_name + '"', xinjin.year,
                             xinjin.month, xinjin.yingfa, xinjin.baoxian, xinjin.gongjijin, xinjin.get_leixing_gbk])
        return response

    return render(request, 'xinjin/xinjin_list.html', {'xinjindan': xinjindan, 'xinjin_list': xinjin_list, })


def all(request):
    year = request.GET.get('year', datetime.now().year)
    month = request.GET.get('month', datetime.now().month)
    name = request.GET.get('bh', '__')

    xinjin_list = Xinjin.objects.filter(year=year, month=month, status='1').order_by('-id')

    if not name == '__':
        xinjin_list = xinjin_list.filter(xinjindan__bianhao__icontains=name)

    if request.GET.get('excel'):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all.csv"'
        writer = csv.writer(response)
        writer.writerow([u'序号'.encode('gbk'), u'编号'.encode('gbk'), u'项目'.encode('gbk'),
                         u'姓名'.encode('gbk'), u'身份证号码'.encode('gbk'), u'年份'.encode('gbk'),
                         u'月份'.encode('gbk'), u'应发'.encode('gbk'), u'保险'.encode('gbk'), u'公积金'.encode('gbk'),
                         u'类型'.encode('gbk')])
        for i, xinjin in enumerate(xinjin_list):
            setattr(xinjin, 'get_username_gbk', xinjin.user.first_name.encode('gbk'))
            setattr(xinjin, 'get_xiangmu_gbk', xinjin.xinjindan.xiangmu.encode('gbk'))
            setattr(xinjin, 'get_leixing_gbk', xinjin.leixing.encode('gbk'))
            writer.writerow([i + 1, xinjin.xinjindan.bianhao, xinjin.get_xiangmu_gbk,
                             xinjin.get_username_gbk, '="' + xinjin.user.last_name + '"', xinjin.year,
                             xinjin.month, xinjin.yingfa, xinjin.baoxian, xinjin.gongjijin, xinjin.get_leixing_gbk])
        return response

    return render(request, 'xinjin/all.html', {'xinjin_list': xinjin_list, 'bh': name})


def xinjin_create(request, id):
    xinjindan = get_object_or_404(XinjinDan, pk=id)
    form = XinjinForm()
    form.fields['user'].queryset = User.objects.exclude(username='admin')
    form.fields['user'].label_from_instance = lambda obj: "%s (%s)" % (obj.first_name, obj.username)
    if request.method == "POST":
        print request.POST.get('next')
        form = XinjinForm(request.POST)
        if form.is_valid():
            xinjin = form.save(commit=False)
            xinjin.xinjindan = xinjindan
            xinjin.typer = request.user
            xinjin.year = datetime.today().year
            xinjin.month = datetime.today().month
            xinjin.save()

            if request.POST.get('next', None):
                return HttpResponseRedirect(reverse('xinjin_create', args=[id]))
            return HttpResponseRedirect(reverse('xinjin_list', args=[id]))
    return render(request, 'xinjin/xinjin_create.html', {'xinjindan': xinjindan, 'form': form})


def xinjin_update(request, id, xid):
    xinjindan = get_object_or_404(XinjinDan, pk=id)
    xinjin = get_object_or_404(Xinjin, pk=xid)
    form = XinjinForm(instance=xinjin)
    form.fields['user'].choices = [(item.pk, "%s(%s)" % (
        item.first_name, item.last_name)) for item in User.objects.exclude(username='admin')]
    if request.method == "POST":
        form = XinjinForm(request.POST, instance=xinjin)
        if form.is_valid():
            xinjin = form.save(commit=False)
            xinjin.typer = request.user
            xinjin.year = datetime.today().year
            xinjin.month = datetime.today().month
            xinjin.save()
            if request.POST.get('next', None):
                return HttpResponseRedirect(reverse('xinjin_create', args=[id]))
            return HttpResponseRedirect(reverse('xinjin_list', args=[id]))
    return render(request, 'xinjin/xinjin_create.html', {'xinjindan': xinjindan, 'form': form})


def xinjin_delete(request, id, xid):
    xinjin = get_object_or_404(XinjinDan, pk=id)
    xinjin.delete()
    return HttpResponseRedirect(reverse('xinjin_list', args=[id]))


def xinjin_valid(request, id, xid):
    xinjin = get_object_or_404(Xinjin, pk=xid)
    if xinjin.status == "0":
        xinjin.status = "1"
    else:
        xinjin.status = "0"
    xinjin.save()
    return HttpResponseRedirect(reverse('xinjin_list', args=[id]))
