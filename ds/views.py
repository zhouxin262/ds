#coding=utf-8
import datetime
import codecs
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_unicode
from django.shortcuts import render
from ds.models import News

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
        return render(request, 'ds/home.html', {'news_list1':news_list1,'news_list2':news_list2})