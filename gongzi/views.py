#coding=utf-8
import xlrd
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
# from django.utils.encoding import smart_unicode
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from gongzi.models import Gongzi


def home(request):
    years = [('__', u'全部'), ]
    for i in range(5):
        if datetime.now().year - i >= 2012:
            years.append((str(datetime.now().year - i), str(datetime.now().year - i)))
    if not request.GET.get("from_year", None):
        y = request.GET.get('y', '__')
        if y == '__':
            year = None
        else:
            year = y

        page = int(request.GET.get('page', 0))
        last_month = datetime.now().month
        try:
            if int(year) < datetime.now().year:
                last_month = 12
        except:
            pass
        
        m1 = last_month - page * 3
        m2 = last_month - 1 - page * 3
        m3 = last_month - 2 - page * 3

        if year:
            args = {'year': year, 'month__in': [m1, m2, m3], 'user': request.user}
        else:
            args = {'user': request.user}

        if page > 0:
            prev = "?y=" + y + "&page=" + str(page - 1)
        else:
            prev = "#"

        if y != "__":
            if m3 > 1:
                next = "?y=" + y + "&page=" + str(page + 1)
            else:
                next = "#"
        else:
            next = "?y=" + y + "&page=" + str(page + 1)

        gs = Gongzi.objects.filter(**args).order_by('-year', '-month', '-yingfa')
        return render(request, 'gongzi/home.html', {'gs': gs, 'y': y, 'm1': m1, 'm2': m2, 'm3': m3,
                                                    'years': years, 'next': next, 'prev': prev})
    else:
        fy = request.GET.get("from_year", None)
        fm = request.GET.get("from_month", None)
        ty = request.GET.get("to_year", None)
        tm = request.GET.get("to_month", None)
        args = {'user': request.user, 'year__range': [fy, ty], "month__range": [fm, tm]}
        print args
        gs = Gongzi.objects.filter(**args).order_by('-year', '-month', '-yingfa')
        return render(request, 'gongzi/home.html', {'gs': gs, "years": years})


def query(request):
    years = []
    months = []
    for i in range(5):
        if datetime.now().year - i >= 2012:
            years.append((str(datetime.now().year - i), str(datetime.now().year - i)))
    for i in range(13)[1:]:
        months.append((str(i), str(i)))

    return render(request, 'gongzi/query.html', {"years": years, "months": months})


@permission_required('gongzi.add_gongzi')
def upload(request):
    err = []
    this_month = datetime.now().month

    if request.method == 'POST':
        month = request.POST.get('month', None)
        year = request.POST.get('year', None)
        f = request.FILES.get('file', None)
        import os
        if month and year and f:
            des_path = os.path.abspath('.') + '/django/ds/gongzi/uploads/upload.xls'
            des_f = open(des_path, "wb")
            for chunk in f.chunks():
                des_f.write(chunk)
            des_f.close()

            bk = xlrd.open_workbook(des_path)
            sheet = bk.sheet_by_index(0)
            rows_num = sheet.nrows
            #cols_num = sheet.ncols

            #title = []
            #rows = []
            gs = []
            for j in range(1, rows_num):
                try:
                    g = Gongzi()
                    g.user = User.objects.get(last_name=sheet.cell_value(j, 3))
                    g.realname = sheet.cell_value(j, 0)
                    g.idcard = sheet.cell_value(j, 2)
                    g.yingfa = smart_float(sheet.cell_value(j, 4))
                    g.baoxian = smart_float(sheet.cell_value(j, 5))
                    g.gongjijin = smart_float(sheet.cell_value(j, 6))
                    g.shuijin = smart_float(sheet.cell_value(j, 7))
                    g.shifa = smart_float(sheet.cell_value(j, 8))
                    g.xiangmu = sheet.cell_value(j, 2)
                    g.memo = sheet.cell_value(j, 9)
                    g.guilei = sheet.cell_value(j, 10)
                    g.month = month
                    g.year = year
                    g.dateline = datetime.today()
                    gs.append(g)
                except User.DoesNotExist:
                    err.append(u'第%s行中身份证号在数据库中找不到对应人员，错误数据%s' % (j + 1, sheet.cell_value(j, 2)))

            if not err:
                Gongzi.objects.bulk_create(gs)
        else:
            err.append(u'表单每项都不能为空')
        return render(request, 'gongzi/admin/upload.html', {'month': this_month, 'err': err, 'post': True})
    return render(request, 'gongzi/admin/upload.html', {'month': this_month, 'err': err})


def smart_float(f):
    try:
        return float(f)
    except:
        return 0


@permission_required('gongzi.add_gongzi')
def list(request):
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')
    first_name = request.GET.get('first_name', '')
    xiangmu = request.GET.get('xiangmu', '')
    querystr = "year=%s&month=%s&first_name=%s&xiangmu=%s" % (year, month, first_name, xiangmu)
    args = {}
    print first_name
    if year:
        args['year'] = year
    if month:
        args['month'] = month
    if first_name:
        args['user__first_name__contains'] = first_name
    if xiangmu:
        args['xiangmu__contains'] = xiangmu
    gongzi = Gongzi.objects.filter(**args).order_by('-dateline')

    paginator = Paginator(gongzi, 25)
    page = request.GET.get('page')
    try:
        gongzi_list = paginator.page(page)
    except PageNotAnInteger:
        gongzi_list = paginator.page(1)
    except EmptyPage:
        gongzi_list = paginator.page(paginator.num_pages)
    return render(request, 'gongzi/admin/list.html', {'gongzi_list': gongzi_list, 'querystr': querystr, "args": args})


@permission_required('gongzi.add_gongzi')
def create(request):
    args = {}
    us = User.objects.exclude(username='admin')
    args['us'] = us

    if request.method == 'POST' and request.POST.get('user'):
        args['post'] = True
        gongzi = Gongzi()
        u = User.objects.get(id=request.POST.get('user'))
        gongzi.user = u
        gongzi.year = request.POST.get('year', datetime.today().year)
        gongzi.month = request.POST.get('month', datetime.today().month)
        gongzi.xiangmu = request.POST.get('xiangmu', '')
        gongzi.yingfa = request.POST.get('yingfa', 0)
        gongzi.baoxian = request.POST.get('baoxian', 0)
        gongzi.gongjijin = request.POST.get('gongjijin', 0)
        gongzi.shuijin = request.POST.get('shuijin', 0)
        gongzi.shifa = request.POST.get('shifa', 0)
        gongzi.memo = request.POST.get('memo', '')
        gongzi.guilei = request.POST.get('guilei', '')
        gongzi.realname = u.first_name
        gongzi.idcard = u.last_name
        gongzi.dateline = datetime.now()
        gongzi.save()
        return render(request, 'gongzi/admin/create.html', args)
    return render(request, 'gongzi/admin/create.html', args)


@permission_required('gongzi.add_gongzi')
def update(request, id):
    args = {}
    us = User.objects.exclude(username='admin')
    args['us'] = us
    gongzi = Gongzi.objects.get(id=id)
    args['gongzi'] = gongzi

    if request.method == 'POST':
        args['post'] = True
        u = User.objects.get(id=request.POST.get('user'))
        gongzi.user = u
        gongzi.year = request.POST.get('year')
        gongzi.month = request.POST.get('month')
        gongzi.xiangmu = request.POST.get('xiangmu')
        gongzi.yingfa = request.POST.get('yingfa')
        gongzi.baoxian = request.POST.get('baoxian')
        gongzi.gongjijin = request.POST.get('gongjijin')
        gongzi.shuijin = request.POST.get('shuijin')
        gongzi.shifa = request.POST.get('shifa')
        gongzi.memo = request.POST.get('memo', '')
        gongzi.guilei = request.POST.get('guilei', '')
        gongzi.realname = u.first_name
        gongzi.idcard = u.last_name
        gongzi.dateline = datetime.now()
        gongzi.save()
        return render(request, 'gongzi/admin/create.html',
                      args)
    return render(request, 'gongzi/admin/create.html', args)


@permission_required('gongzi.add_gongzi')
def delete(request, id):
    Gongzi.objects.get(id=id).delete()
    return HttpResponseRedirect('/gongzi/admin/list/')


@permission_required('gongzi.add_gongzi')
def bulk_delete(request):
    gongzi_list = []
    for g in Gongzi.objects.filter(year=datetime.now().year).values('month').distinct().order_by('-month'):
        gongzi_list.append({'year': datetime.now().year, 'month': g['month']})

    if request.GET.get('year', None) and request.GET.get('month', None):
        Gongzi.objects.filter(year=request.GET.get('year', None), month=request.GET.get('month', None)).delete()
        return HttpResponseRedirect('/gongzi/admin/bulk_delete/')

    return render(request, 'gongzi/admin/bulk_delete.html', {'gongzi_list': gongzi_list})
