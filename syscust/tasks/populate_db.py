import os
import django
from datetime import datetime

# إعداد بيئة Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Task
from django.contrib.auth.models import User

# إنشاء مستخدم جديد إذا لم يكن موجوداً بالفعل
user, created = User.objects.get_or_create(username='username', defaults={
    'email': 'email@example.com',
    'first_name': 'First',
    'last_name': 'Last'
})
if created:
    user.set_password('password')
    user.save()

# إنشاء مهمة جديدة وإسنادها للمستخدم
task = Task.objects.create(
    title='Task Title',
    description='Task Description',
    start_date=datetime.now(),
    end_date=datetime.now(),
    priority='Medium',
    assigned_to=user
)
print(f'Task "{task.title}" assigned to user "{user.username}".')
