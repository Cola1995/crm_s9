from .models import *
from Xadmin.service.Xadmin import site,ModelXadmin
from  django.shortcuts import render, redirect, HttpResponse
from django.conf.urls import url
from django.utils.safestring import mark_safe

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

    def extra_url(self):
        """
        扩展url 类
        :return:
        """
        temp = []
        temp.append(url(r"cancel_course/(\d+)/(\d+)", self.cancel_course))    # 添加路由
        return temp

    list_display = ["name", display_gender,display_course,"consultant"]

site.register(Customer, Customerconfig)
site.register(Department)
site.register(Course)
site.register(ConsultRecord)
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
    list_display = ["username","class_list"]
site.register(Student,StudentConfig)
