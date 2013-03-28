#coding=utf-8
import csv
from datetime import datetime
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from webstatus.forms import WebStatusForm
from webstatus.models import WebStatus
from django.db.models import Count


@permission_required('webstatus.add_webstatus')
def create(request):
    form = WebStatusForm()
    datestr = "%s-%s-%s" % (datetime.today().year, datetime.today().month, datetime.today().day)
    if request.method == "POST":
        form = WebStatusForm(request.POST)
        if form.is_valid():
            ws = form.save(commit=False)
            ws.user = request.user
            ws.save()
            return HttpResponseRedirect(reverse('webstatus_list'))
    return render(request, 'webstatus/create.html', {'form': form, 'datestr': datestr})


@permission_required('webstatus.change_webstatus')
def update(request, id):
    ws = get_object_or_404(WebStatus, pk=id, user=request.user)
    form = WebStatusForm(instance=ws)
    if request.method == 'POST':
        form = WebStatusForm(request.POST, instance=ws)
        if form.is_valid():
            ws = form.save()
        return render(request, 'webstatus/create.html', {'form': form, 'post': True})
    return render(request, 'webstatus/create.html', {'form': form})


@permission_required('webstatus.add_webstatus')
def view(request, id):
    ws = get_object_or_404(WebStatus, pk=id)
    form = WebStatusForm(instance=ws)
    return render(request, 'webstatus/view.html', {'form': form})


@permission_required('webstatus.delete_webstatus')
def delete(request, id):
    ws = get_object_or_404(WebStatus, pk=id, user=request.user)
    ws.delete()
    return HttpResponseRedirect(reverse('webstatus_list'))


@permission_required('webstatus.add_webstatus')
def list(request):
    webstatus_list = WebStatus.objects.filter().order_by('log_time').order_by('log_date')
    if request.GET.get('excel'):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="webstatus.csv"'
        writer = csv.writer(response)
        writer.writerow([u'时间日期'.encode('gbk'), u'监测人'.encode('gbk'), u'教师工作室'.encode('gbk'),
                         u'学生工作室'.encode('gbk'), u'在线测试'.encode('gbk'), u'交互课堂 '.encode('gbk'), u'备注'.strip().replace('\n', ' ').encode('gbk')])
        for i, ws in enumerate(webstatus_list):
            writer.writerow([ws.log_date.strftime('%Y-%m-%d') + ' ' + ws.log_time, ws.user.first_name.encode('gbk'),
                             ws.jsgzs.encode('gbk'), ws.xsgzs.encode('gbk'), ws.zxcs.encode('gbk'), ws.jhkt.encode('gbk'), ws.memo.encode('gbk')])
        return response
    # paginator = Paginator(ws, 25)
    # page = request.GET.get('page')
    # try:
    #     webstatus_list = paginator.page(page)
    # except PageNotAnInteger:
    #     webstatus_list = paginator.page(1)
    # except EmptyPage:
    #     webstatus_list = paginator.page(paginator.num_pages)
    return render(request, 'webstatus/list.html', {'webstatus_list': webstatus_list})


def tongji(request):
    s = request.GET.get('s', datetime.today().replace(day=1).strftime("%Y-%m-%d"))
    e = request.GET.get('e', datetime.today().replace(month=((datetime.today().month + 1) % 12), day=1).strftime("%Y-%m-%d"))

    dataset = WebStatus.objects.filter(log_date__range=[s, e])
    t1 = dataset.values('jsgzs').annotate(c=Count('jsgzs'))
    t2 = dataset.values('xsgzs').annotate(c=Count('xsgzs'))
    t3 = dataset.values('zxcs').annotate(c=Count('zxcs'))
    t4 = dataset.values('jhkt').annotate(c=Count('jhkt'))

    return render(request, 'webstatus/tongji.html', {'t1': t1, 't2': t2, 't3': t3, 't4': t4, "s": s, "e": e})
