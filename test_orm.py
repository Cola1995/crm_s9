import  os

if __name__=='__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm_s9.settings")
    import django
    django.setup()
    from crm.models import *
    customers = Customer.objects.all()
    from datetime import *
    time_3 = datetime.now()-timedelta(days=3)
    time_15 = datetime.now()-timedelta(days=15)
    print(time_3)
    print(time_15)
    from django.db.models import Q
    out = Customer.objects.filter(Q(last_consult_date__lt=time_3) | Q(recv_date__lt=time_15),status=2)
    print(out)