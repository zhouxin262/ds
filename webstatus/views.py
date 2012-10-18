#coding=utf-8
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from webstatus.forms import WebStatusForm
from webstatus.models import WebStatus

def create(request):
    form = WebStatusForm()
    if request.method=="POST":
        form = WebStatusForm(request.POST)
        if form.is_valid():
            ws = form.save(commit=False)
            ws.user = request.user 
            ws.save()
            return HttpResponseRedirect(reverse('webstatus_list'))
    return render(request, 'webstatus/create.html', {'form': form})

def update(request,id):
    ws = get_object_or_404(WebStatus, pk=id)
    form = WebStatusForm(instance=ws)
    if request.method == 'POST':
        form = WebStatusForm(request.POST,instance=ws)
        if form.is_valid():
            ws = form.save()
        return render(request, 'webstatus/create.html',{'form': form,'post':True})
    return render(request, 'webstatus/create.html',{'form': form})

def view(request,id):
    ws = get_object_or_404(WebStatus, pk=id)
    form = WebStatusForm(instance=ws)
    return render(request, 'webstatus/view.html',{'form': form})

def delete(request,id):
    ws = get_object_or_404(WebStatus, pk=id)
    ws.delete()
    return HttpResponseRedirect(reverse('webstatus_list'))

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
    return render(request, 'webstatus/list.html',{'webstatus_list':webstatus_list})
