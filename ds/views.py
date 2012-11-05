#coding=utf-8
import datetime
import codecs
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_unicode
from django.shortcuts import render
from ds.models import News
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User

def home(request):
    n = News.objects.filter(date__gte = datetime.date.today()).count()
    if not n:
        import urllib2
        from BeautifulSoup import BeautifulSoup
        res = urllib2.urlopen('http://dispub.bjtu.edu.cn/cms/xwdb/index.htm').read()
        soup = BeautifulSoup(''.join(res), fromEncoding='gbk')
        n = News()
        n.content = str(soup.find('ul', {'class':'liebiao'}))
        n.title = '新闻点播'
        n.save()
        res = urllib2.urlopen('http://dispub.bjtu.edu.cn/cms/xytz/index.htm').read()
        soup = BeautifulSoup(''.join(res), fromEncoding='gbk')
        n = News()
        n.content = str(soup.find('ul', {'class':'liebiao'}))
        n.title = '学院通知'
        n.save()

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/')
    else:
        news_list1 = News.objects.filter(title = '新闻点播').order_by('-date')[0].content
        news_list2 = News.objects.filter(title = '学院通知').order_by('-date')[0].content
        # 用户管理员
        usermanagers = User.objects.filter(username__in = ['admin', '6616',])
        # 工资管理员
        gongzimanagers = User.objects.filter(username__in = ['admin', '6616',])
        # 网站状态监控员
        # webstatusmanagers = User.objects.filter(username__in = ['admin', '430124198809180011', '70251', '13022419820312081X', '5054', '70248', '110221198211183615','6836'])
        return render(request, 'ds/home.html', {'news_list1':news_list1,
            'news_list2':news_list2,
            'usermanagers': usermanagers,
            'gongzimanagers': gongzimanagers})

def adduser(request):
    if request.method == "POST":
        err = ''
        u = User.objects.filter(username = request.POST.get('username', ''))
        print  u
        if u:
            err = u'重复的证件账号'
        else:
            u = User()
            u.username = request.POST.get('username', '')
            u.password = request.POST.get('password', '')
            u.first_name = request.POST.get('first_name', '')
            u.last_name = request.POST.get('username', '')
            u.save()
        return render(request, 'ds/user/add.html', {'err':err, 'post':True})
    return render(request, 'ds/user/add.html')

def edituser(request,id):
    u = User.objects.get(pk=id)
    res_dic = {'u':u}
    if request.method == "POST":
        u.password = request.POST.get('password', '')
        u.first_name = request.POST.get('first_name', '')
        u.save()
        res_dic['post'] =  True
    return render(request, 'ds/user/edit.html', res_dic)

def listuser(request):
    fn = request.GET.get('fn', '')
    users = User.objects.filter(first_name__contains = fn).order_by('date_joined')
    paginator = Paginator(users, 15)
    page = request.GET.get('page')
    try:
        user_list = paginator.page(page)
    except PageNotAnInteger:
        user_list = paginator.page(1)
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)
    return render(request, 'ds/user/list.html', {'user_list':user_list, 'fn':fn})

def deluser(request,id):
    u = User.objects.get(pk=id)
    u.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/user/list/'))
