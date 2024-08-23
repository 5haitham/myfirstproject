
from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task, Notification
from django.core import mail

class TaskSignalTests(TestCase):
    def setUp(self):
        # إعداد بيانات الاختبار
        self.user = User.objects.create_user(username='admin', email='mohamedhaitham09587@gmail.com', password='123')

    def test_task_creation_sends_notification(self):
        # إنشاء مهمة جديدة
        task = Task.objects.create(
            title='Test Task',
            start_date='2024-08-22',
            end_date='2024-08-22',
            assigned_to=self.user
        )
        
        # تحقق من إنشاء الإشعار
        notification = Notification.objects.get(task=task)
        self.assertEqual(notification.user, self.user)
        self.assertIn('Test Task', notification.message)
        
        # تحقق من إرسال البريد الإلكتروني
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'مهمة جديدة مخصصة لك')
        self.assertIn('Test Task', mail.outbox[0].body)
