#coding=utf-8
from datetime import datetime
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from webstatus.forms import WebStatusForm
from webstatus.models import WebStatus


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
    ws = WebStatus.objects.filter().order_by('-id')
    paginator = Paginator(ws, 25)
    page = request.GET.get('page')
    try:
        webstatus_list = paginator.page(page)
    except PageNotAnInteger:
        webstatus_list = paginator.page(1)
    except EmptyPage:
        webstatus_list = paginator.page(paginator.num_pages)
    return render(request, 'webstatus/list.html', {'webstatus_list': webstatus_list})
