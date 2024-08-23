from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task, Notification

@receiver(post_save, sender=Task)
def send_task_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.assigned_to
        notification_message = f"لديك مهمة جديدة بعنوان '{instance.title}' والتي تبدأ في {instance.start_date}."

        # إرسال إشعار عبر البريد الإلكتروني
        send_mail(
            subject='مهمة جديدة مخصصة لك',
            message=notification_message,
            from_email='mohamedhaitham09587@gmail.com',
            recipient_list=[user.email],
        )

        # إذا كنت تستخدم نموذج Notification، يمكنك إنشاء سجل جديد:
        Notification.objects.create(
            user=user,
            task=instance,
            message=notification_message
        )
