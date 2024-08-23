from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver




# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("الاسم"))

    def __str__(self):
        return self.name

# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("الاسم"))

    def __str__(self):
        return self.name

# Goal model
class Goal(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("العنوان"))
    description = models.TextField(blank=True, verbose_name=_("الوصف"))
    due_date = models.DateField(verbose_name=_("تاريخ الاستحقاق"))

    def __str__(self):
        return self.title

# Task model
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', _('عالية')),
        ('Medium', _('متوسطة')),
        ('Low', _('منخفضة')),
    ]

    STATUS_CHOICES = [
        ('Not Started', _('لم يبدأ')),
        ('In Progress', _('قيد التنفيذ')),
        ('Completed', _('منفذ')),
    ]

    title = models.CharField(max_length=200, verbose_name=_("العنوان"))
    description = models.TextField(blank=True, verbose_name=_("الوصف"))
    start_date = models.DateField(default=date.today, verbose_name=_("تاريخ البداية"))
    end_date = models.DateField(verbose_name=_("تاريخ النهاية"))
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium', verbose_name=_("الأولوية"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started', verbose_name=_("الحالة"))
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("مخصص لـ"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("التصنيف"))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("الوسوم"))
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("الهدف"))
    reminder_date = models.DateField(null=True, blank=True, verbose_name=_("تاريخ التذكير"))
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks', verbose_name=_("المهمة الأصل"))
    comments = models.TextField(blank=True, verbose_name=_("التعليقات"))  # التعليقات كحقل نصي داخل مهمة
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإنشاء"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاريخ التحديث"))

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(_('يجب أن يكون تاريخ النهاية بعد تاريخ البداية.'))

# Notification model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("المستخدم"))
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_("المهمة"))
    message = models.CharField(max_length=255, verbose_name=_("الرسالة"))
    sent_at = models.DateTimeField(default=timezone.now, verbose_name=_("تاريخ الإرسال"))

    def __str__(self):
        return f"Notification for user {self.user} - {self.task}"

class PerformanceReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("المستخدم"))
    report_date = models.DateField(default=date.today, verbose_name=_("تاريخ التقرير"))
    total_tasks = models.IntegerField(default=0, verbose_name=_("المهام الكليّة"))
    completed_tasks = models.IntegerField(default=0, verbose_name=_("المهام المكتملة"))
    overdue_tasks = models.IntegerField(default=0, verbose_name=_("المهام المتأخرة"))
    in_progress_tasks = models.IntegerField(default=0, verbose_name=_("المهام قيد التنفيذ"))
    points = models.IntegerField(default=0, verbose_name=_("النقاط"))

    def __str__(self):
        return f"Performance report for user {self.user} on {self.report_date}"

    def save(self, *args, **kwargs):
        # تحديد تاريخ التقرير
        report_date = self.report_date or date.today()

        # احسب المهام الكليّة حتى تاريخ التقرير
        self.total_tasks = Task.objects.filter(
            assigned_to=self.user,
            start_date__lte=report_date  # يجب أن تكون تاريخ البداية أقل من أو تساوي تاريخ التقرير
        ).count()

        # احسب المهام المكتملة حتى تاريخ التقرير
        self.completed_tasks = Task.objects.filter(
            assigned_to=self.user,
            status='Completed',
            end_date__lte=report_date  # حتى تاريخ التقرير
        ).count()

        # احسب المهام المتأخرة حتى تاريخ التقرير
        self.overdue_tasks = Task.objects.filter(
            assigned_to=self.user,
            status__in=['Not Started', 'In Progress'],
            end_date__lt=report_date  # حتى تاريخ التقرير
        ).count()

        # احسب المهام قيد التنفيذ التي ليست متأخرة
        self.in_progress_tasks = Task.objects.filter(
            assigned_to=self.user,
            status='In Progress',
            end_date__gte=report_date  # يجب أن تكون بتاريخ نهاية أكبر من أو يساوي تاريخ التقرير
        ).count()

        # احصل على النقاط من عدد المهام المكتملة
        self.points = self.completed_tasks  # كل مهمة مكتملة تعطي نقطة واحدة

        super().save(*args, **kwargs)



# GoogleCredentials model
class GoogleCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("المستخدم"))
    credentials = models.JSONField(verbose_name=_("الاعتمادات"))

    def __str__(self):
        return f"Google credentials for user {self.user.username}"

# بديل عن UserProfile لإنشاء المستخدمين فقط (UserCreation model)
class UserCreation(models.Model):
    username = models.CharField(max_length=150, verbose_name=_("اسم المستخدم"))
    email = models.EmailField(unique=True, verbose_name=_("البريد الإلكتروني"))
    password = models.CharField(max_length=128, verbose_name=_("كلمة المرور"))

    def __str__(self):
        return self.username
