#coding=utf-8
import xlrd
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode

from gongzi.models import Gongzi

def home(request):
    gs = Gongzi.objects.filter(user=request.user).order_by('-year', '-month', '-yingfa')
    return render(request, 'gongzi/home.html',{'gs': gs} )

def upload(request):
    import datetime
    err = []
    this_month = datetime.date.today().month

    if request.method == 'POST':
        month = request.POST.get('month', None)
        year = request.POST.get('year', None)
        f = request.FILES.get('file', None)
        import os
        if month and year and f:
            des_path = os.path.abspath('.') + '/gongzi/uploads/upload.xls'
            des_f = open(des_path, "wb")  
            for chunk in f.chunks():
                des_f.write(chunk)
            des_f.close()  

            bk = xlrd.open_workbook(des_path)
            sheet = bk.sheet_by_index(0)
            rows_num = sheet.nrows
            cols_num = sheet.ncols
            
            title = []
            rows = []
            gs = []
            for j in range(1, rows_num): 
                try:
                    g = Gongzi()
                    g.user = User.objects.get(last_name=sheet.cell_value(j,2))
                    g.realname = sheet.cell_value(j,1)
                    g.idcard = sheet.cell_value(j,2)
                    g.yingfa = smart_float(sheet.cell_value(j,3))
                    g.baoxian = smart_float(sheet.cell_value(j,4))
                    g.gongjijin = smart_float(sheet.cell_value(j,5))
                    g.shuijin = smart_float(sheet.cell_value(j,6))
                    g.shifa = smart_float(sheet.cell_value(j,7))
                    g.xiangmu = sheet.cell_value(j,8)
                    g.month = sheet.cell_value(j,0)
                    g.year = year
                    g.dateline = datetime.date.today()
                    gs.append(g)
                except User.DoesNotExist:
                    err.append(u'第%s行中身份证号在数据库中找不到对应人员，错误数据%s' % (j+1, sheet.cell_value(j,2)))

            if not err:
                for g in gs:
                    #try:
                        g.save()
                    # except:
                    #     pass           

    return render(request, 'gongzi/upload.html', {'month': this_month, 'err': err})

def smart_float(f):
    try:
        return float(f)
    except:
        return 0