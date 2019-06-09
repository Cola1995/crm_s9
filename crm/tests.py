from django.test import TestCase

# Create your tests here.
data = {'57': {'score': '90', 'homework_note': '11111'}, '58': {'score': '90', 'homework_note': '22'}}

def aa(**kwargs):
    print(kwargs)
