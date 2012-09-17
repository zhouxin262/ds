from django.http import HttpResponseRedirect
from django.shortcuts import render

def home(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/login/')
	return render(request, 'ds/home.html')