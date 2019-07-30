from django.shortcuts import render,redirect
from rbac.service.perssions import initial_session
# Create your views here.
from crm.models import *
from rbac.models import *
from django.http import JsonResponse
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

def logout(request):
    request.session.delete()
    return redirect("/login/")



def index(request):
    user = request.session['user']




    return render(request,"rbac/base1.html",locals())

def show_data(request):
    classlists = ClassList.objects.all()
    a_list = []
    for cls in classlists:
        c_dict = {}
        m_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        c_dict['name'] = cls.course.name + str(cls.semester)
        for student in ClassList.objects.filter(pk=cls.pk).first().student_set.all():
            m_list[student.create_time.month] = m_list[student.create_time.month] + 1
        c_dict["data"] = m_list
        a_list.append(c_dict)
    return JsonResponse(a_list,safe=False)




def test(request):

    return render(request,"admin.html")