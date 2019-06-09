from django.test import TestCase

# Create your tests here.

class Person:
    city = 'ma'
    def __init__(self,name):
        self.name = name
    def run(self):
        print('run')

p = Person('ma')
# p.run()
val = getattr(p,"city")

print(val)