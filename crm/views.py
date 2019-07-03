from django.shortcuts import render,redirect
from rbac.service.perssions import initial_session
# Create your views here.
from rbac.models import *
def login(request):

    if request.method=="POST":
        username = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user = User.objects.filter(name=username,pwd=pwd).first()
        initial_session(user,request)
        request.session['user_id'] = user.pk
        request.session['user'] = user.name

        # return render(request,"rbac/base1.html",locals())
        return redirect('/index/')
    return render(request,"login.html",locals())



def index(request):
    user = request.session['user']
    return render(request,"rbac/base1.html",locals())




def test(request):

    return render(request,"admin.html")