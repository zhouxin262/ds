#coding=utf-8
import csv
from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Count
# from django.utils.encoding import smart_unicode
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jiaofu.models import Zixun
from jiaofu.forms import ZixunForm, JiejueForm


def list(request):
    wentileibies = [w.id for w in request.user.wentileibie.all()]
    for group in request.user.groups.all():
        wentileibies += [w.id for w in group.wentileibie.all()]
    zixun_list = Zixun.objects.filter(wentileibie_id__in=wentileibies).order_by('-dateline')

    if request.GET.get('excel'):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all.csv"'
        writer = csv.writer(response)
        writer.writerow([u'序号'.encode('gbk'), u'日期时间'.encode('gbk'), u'咨询方式'.encode('gbk'),
                         u'学号'.encode('gbk'), u'站点名称'.encode('gbk'), u'联系方式'.encode('gbk'),
                         u'咨询问题'.encode('gbk'), u'人员类别'.encode('gbk'), u'问题类别'.encode('gbk'), u'问题处理情况'.encode('gbk'),
                         u'备注'.encode('gbk'), u'问题处理时间'.encode('gbk'), u'问题解决方案'.encode('gbk')])
        for i, zixun in enumerate(zixun_list):
            writer.writerow([i + 1, zixun.dateline, zixun.get_fangshi_display().encode('gbk'),
                             zixun.xuehao.encode('gbk'), zixun.zhandian.encode('gbk'), zixun.lianxifangshi.encode('gbk'),
                             zixun.wenti.encode('gbk'), zixun.get_renyuanleibie_display().encode('gbk'),
                             zixun.wentileibie.name.encode('gbk'), zixun.get_chuliqingkuang_display().encode('gbk'),
                             zixun.memo.encode('gbk'), zixun.jiejue_dateline, zixun.jiejuefangan.encode('gbk')])
        return response

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


def jiejue(request, id):
    zixun = get_object_or_404(Zixun, pk=id)
    zixun.chuliqingkuang = u"处"
    form = JiejueForm(instance=zixun)
    if request.method == "POST":
        form = JiejueForm(request.POST, instance=zixun)
        if form.is_valid():
            zixun = form.save(commit=False)
            zixun.jiejue_typer = request.user
            zixun.save()
            return HttpResponseRedirect(reverse('zixun_list'))
    return render(request, 'jiaofu/create.html', {'form': form})


def tongji(request):
    s = request.GET.get('s', datetime.today().replace(day=1).strftime("%Y-%m-%d"))
    e = request.GET.get('e', datetime.today().replace(month=((datetime.today().month + 1) % 12), day=1).strftime("%Y-%m-%d"))

    dataset = Zixun.objects.filter(dateline__range=[s, e])
    print dataset
    t1 = []
    fangshi = (("Q", u"QQ"), ("E", u"EMAIL"), ("T", u"电话"))
    for i, r in enumerate(dataset.values('fangshi').annotate(c=Count('fangshi'))):
        for f in fangshi:
            if r['fangshi'] == f[0]:
                r['label'] = f[1]
        t1.append(r)
    print t1

    t2 = []
    for i, r in enumerate(dataset.values('renyuanleibie').annotate(c=Count('renyuanleibie'))):
        r['label'] = r['renyuanleibie']
        t2.append(r)

    t3 = []
    for i, r in enumerate(dataset.values('wentileibie__name').annotate(c=Count('wentileibie__name'))):
        r['label'] = r['wentileibie__name']
        t3.append(r)

    return render(request, 'jiaofu/tongji.html', {'t1': t1, 't2': t2, 't3': t3, "s": s, "e": e})
