from .models import *
from Xadmin.service.Xadmin import site,ModelXadmin
from  django.shortcuts import render, redirect, HttpResponse
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from datetime import *

class Userinfo(ModelXadmin):
    list_display = ['name','username','email','depart']

class Classlistconfig(ModelXadmin):

    def display_classname(self, obj=None, is_header=False):
        # print("调试：", type(obj))
        if is_header:
            return "班级名称"
        class_name = "%s(%s)" % (obj.course.name, str(obj.semester))
        return class_name

    list_display = [display_classname, "tutor", "teachers"]
    list_filter = ["school"]
site.register(School)
site.register(UserInfo,Userinfo)
site.register(ClassList,Classlistconfig)

class Customerconfig(ModelXadmin):
    def display_gender(self,obj=None, is_header=False):
        if is_header:
            return "性别"
        return obj.get_gender_display()


    def display_course(self,obj=None, is_header=False):
        """
        构建课程多对多连接a便签类
        :param obj:
        :param is_header:
        :return:
        """
        temp = []
        if is_header:
            return "课程"
        for i in  obj.course.all():
            a = "<a  href='/Xadmin/crm/customer/cancel_course/%s/%s' style='border:solid 1px;padding:3px 6px;margin-left:10px;'>%s</a>"%(obj.pk,i.pk,str(i))
            temp.append(a)
        from django.utils.safestring import mark_safe
        return mark_safe("".join(temp))

    def cancel_course(self, request, customer_id, course_id):
        """
        扩展移出课程视图
        :param request:
        :param customer_id:
        :param course_id: 课程id
        :return:
        """
        # print(customer_id, course_id)

        obj = Customer.objects.filter(pk=customer_id).first()
        obj.course.remove(course_id)
        return redirect(self.get_list_url())


    def public_view(self,request):
        """
        公共也页面视图
        公共客户标准：3天为跟进或15天未成单且未报名的客户
        :param request:
        :return:
        """

        time_3 = datetime.now() - timedelta(days=3)
        time_15 = datetime.now() - timedelta(days=15)
        from django.db.models import Q
        customers = Customer.objects.filter(Q(last_consult_date__lt=time_3) | Q(recv_date__lt=time_15), status=2)
        return render(request, "public_customer.html",locals())

    def futher(self, request,customer_id):

        user_id = 6  # 我是销售
        print(customer_id)
        now = datetime.now()

        time_3 = datetime.now() - timedelta(days=3)
        time_15 = datetime.now() - timedelta(days=15)
        from django.db.models import Q
        ret = Customer.objects.filter(pk=customer_id).filter(Q(last_consult_date__lt=time_3) | Q(recv_date__lt=time_15), status=2).update(recv_date=now,last_consult_date=now, consultant=user_id)
        if not ret:
            return HttpResponse("已经被跟进了")
        else:
            CustomerDistrbute.objects.create(customer_id=customer_id, consultant_id=user_id, date=now, status=1)
            return HttpResponse("跟进成功")

    def mycustomer(self,request):
        user_id = 6
        mycustomer = CustomerDistrbute.objects.filter(consultant=user_id)
        return render(request,"mycustomer.html",locals())


    def extra_url(self):
        """
        扩展url 类
        :return:
        """
        temp = []
        temp.append(url(r"cancel_course/(\d+)/(\d+)", self.cancel_course))    # 添加路由
        temp.append(url(r"public/$", self.public_view))    # 添加公共客户路由
        temp.append(url(r"futher/(\d+)", self.futher))    # 添加公共客户路由
        temp.append(url(r"mycustomer/", self.mycustomer))    # 添加公共客户路由

        return temp

    list_display = ["name", display_gender,display_course,"consultant","education"]

site.register(Customer, Customerconfig)
site.register(Department)
site.register(Course)

class ConsultRecordConfig(ModelXadmin):
    list_display = ['customer','consultant','note','date']

site.register(ConsultRecord,ConsultRecordConfig)
class CourseRecordConfig(ModelXadmin):


    def patch_record(self, request, queryset):
        # print("调试record",queryset)
        # queryset.delete()
        temp = []
        for course in queryset:
            for student in Student.objects.filter(class_list__id = course.class_obj.pk):
                studyecord = StudyRecord(course_record=course, student=student)
                temp.append(studyecord)
                # StudyRecord.objects.create(course_record=course,student=student)
        # return redirect(self.get_list_url())
        StudyRecord.objects.bulk_create(temp)

    def score(self, request, course_record_id):

        """"
        添加score视图函数
        """
        # print(course_record_id)
        # study_record_list = StudyRecord.objects.filter(course_record=course_record_id)
        if request.method == "POST":
            print("post请求数据",request.POST)
            data = {}
            for key, value in request.POST.items():   # 处理传过来的数据
                #{'csrfmiddlewaretoken': ['WYIjIV8uNk5H1qj04RyquVrvmj6hWeMoUXe6o6VUakmmaRsBGXV8XrDrFtFuJvv5'], 'score_57': ['90'], 'homework_note_57': ['11111'], 'score_58': ['90'], 'homework_note_58': ['22']}
                if key == "csrfmiddlewaretoken": continue
                field, pk = key.rsplit("_", 1)   # homework_note_57 字符串切割 从右边开始切割一次
                if pk in data:
                    data[pk][field] = value
                else:
                    data[pk] = {field: value}  # data  {4:{"score":90}}
            # print("data", data)
            # data = {'57': {'score': '90', 'homework_note': '11111'}, '58': {'score': '90', 'homework_note': '22'}}

            for pk, update_data in data.items():
                # print("调试**",**update_data)
                StudyRecord.objects.filter(pk=pk).update(**update_data)
            return redirect(request.path)  # 重定向到本页
        else:
            study_record_list = StudyRecord.objects.filter(course_record=course_record_id)
            score_choices = StudyRecord.score_choices
            # print("调试323", study_record_list)
            return render(request, "score.html", locals())

    def recored_score(self,obj=None, is_header = False):
        if is_header:
            return "录入成绩"
        else:
            return mark_safe("<a href='record_score/%s'>录入成绩</a>"%(obj.pk))

    def extra_url(self):
        """
        扩展url
        :return:
        """
        temp = []
        temp.append(url(r"record_score/(\d+)", self.score))  # 添加路由
        return temp


    def d_record(self,obj=None,is_header = False):
        if is_header:
            return "考勤"
        else:
            return mark_safe("<a href='/Xadmin/crm/studyrecord/?course_record=%s'>go</a>"%(obj.pk))

    list_display = ['class_obj', 'teacher', d_record, 'day_num', recored_score]

    patch_record.short_description = "批量生成学生记录"
    actions = [patch_record]


site.register(CourseRecord,CourseRecordConfig)

class StudyRecordConfig(ModelXadmin):
    def get_record_display(self,obj=None,is_header= False):
        if is_header:
            return "上课记录"
        return obj.get_record_display()

    def get_score_display(self,obj=None,is_header= False):
        if is_header:
            return "成绩"
        return obj.get_score_display()
    def path_late(self, request, queryset):
        queryset.update(record="late")
    path_late.short_description = "迟到"


    def path_checked(self, request, queryset):
        queryset.update(record="checked")
    path_checked.short_description = "签到"


    actions = [path_late,path_checked]
    list_display = ['student','course_record','record','score']

    # search_fields = ['id']
    # list_filter = ['note']

site.register(StudyRecord,StudyRecordConfig)


class StudentConfig(ModelXadmin):
    def score_show(self, obj= None, is_header = False):
        if is_header:
            return "查看成绩"
        else:
            return mark_safe("<a href='show_score/%s'>查看</a>"%(obj.pk))

    def score_show_view(self, request, student_id):
        """
        查看成绩
        :param request:
        :param student_id:
        :return:
        """
        if request.is_ajax():   # 判断是否是ajax提交
            # print('收到ajax请求')
            c_id = request.GET.get("c_id")
            s_id = request.GET.get("s_id")
            # print("course_id",c_id,"s_id",s_id)
            data = []
            # 查询每一天的学习记录
            records = StudyRecord.objects.filter(student= s_id,course_record__class_obj=c_id)      #[["day94",90]]
            # print(records.first().course_record.day_num)
            # 构建hichart需要的数据结构
            for record in records:
                data.append(["day%s"%record.course_record.day_num,record.score])
            # print(data)
            return JsonResponse(data, safe=False)
        else:
            student = Student.objects.filter(pk = student_id).first()
            class_list =student.class_list.all()
            return render(request, "show_score.html", locals())

    def extra_url(self):
        temp = []
        temp.append(url(r"show_score/(\d+)", self.score_show_view))  # 添加路由
        return temp

    list_display = ["username","class_list", score_show]
site.register(Student,StudentConfig)
site.register(CustomerDistrbute)
