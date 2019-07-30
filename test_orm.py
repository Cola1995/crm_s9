import  os

if __name__=='__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm_s9.settings")
    import django
    django.setup()
    from crm.models import *
    # customers = Customer.objects.all()
    # from datetime import *
    # time_3 = datetime.now()-timedelta(days=3)
    # time_15 = datetime.now()-timedelta(days=15)
    # print(time_3)
    # print(time_15)
    # from django.db.models import Q
    # out = Customer.objects.filter(Q(last_consult_date__lt=time_3) | Q(recv_date__lt=time_15),status=2)
    # print(out)
    from django.db.models import Count

    # [{
    #     name: 'Python班级',
    #     data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
    # }, {
    #     name: 'Linux班级',
    #     data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
    # }]


    s=Student.objects.values("class_list__course").annotate(c=Count("id")).values("class_list__course__name","c")
    # d = Student.objects.values("create_time").annotate(c=Count("id")).values("create_time","c")
    d = Student.objects.extra(select={"create_time":"strftime('%Y-%m',create_time)"}).values("create_time").annotate(c=Count("id")).values("create_time","c")
    # tt = Student.objects.filter(pk=5).first().create_time
    # 格式化时间
    a = Student.objects.extra(select={"create_time":"strftime('%Y-%m',create_time)"})
    # 通过classlist统计人数
    # c_count = ClassList.objects.filter(pk=1).first().student_set.all()
    # # d = Student.objects.filter(id=1).extra(select={"create_time": "DATE_FORMAT(create_time, '%%e')"}).values("create_time").annotate(c=Count("id")).values("create_time","c")
    #
    # # 构建日期数据
    # m_list=[0,0,0,0,0,0,0,0,0,0,0,0]
    # for i in c_count:
    #   m_list[i.create_time.month]=m_list[i.create_time.month]+1
    # print(m_list)


    # 构建首页highchart需要的数据
    classlists = ClassList.objects.all()
    a_list=[]
    for cls in  classlists:
        c_dict = {}
        m_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        c_dict['name']=cls.course.name+str(cls.semester)
        for student in ClassList.objects.filter(pk=cls.pk).first().student_set.all():
            m_list[student.create_time.month] = m_list[student.create_time.month] + 1
        c_dict["data"]=m_list
        a_list.append(c_dict)

    print(a_list)



