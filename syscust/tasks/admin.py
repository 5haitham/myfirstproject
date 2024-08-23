from django.contrib import admin
from .models import Category, Tag, Goal, Task, Notification, PerformanceReport, GoogleCredentials, UserCreation
from django.utils.translation import gettext_lazy as _

# تخصيص نموذج الإدارة لنموذج Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    verbose_name = _("تصنيف")
    verbose_name_plural = _("التصنيفات")

# تخصيص نموذج الإدارة لنموذج Tag
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    verbose_name = _("وسم")
    verbose_name_plural = _("الأوسمة")

# تخصيص نموذج الإدارة لنموذج Goal
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date')
    search_fields = ('title',)
    list_filter = ('due_date',)
    verbose_name = _("هدف")
    verbose_name_plural = _("الأهداف")

# تخصيص نموذج الإدارة لنموذج Task
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date', 'priority', 'status', 'assigned_to', 'category', 'goal')
    list_filter = ('priority', 'status', 'category', 'goal', 'assigned_to')
    search_fields = ('title', 'description', 'assigned_to__username')  # يمكنك البحث بالاسم المستخدم
    verbose_name = _("مهمة")
    verbose_name_plural = _("المهام")

# تخصيص نموذج الإدارة لنموذج Notification
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'message', 'sent_at')
    list_filter = ('user', 'sent_at')
    search_fields = ('message', 'user__username', 'task__title')  # يمكنك البحث بالاسم المستخدم وبعنوان المهمة
    verbose_name = _("تنبيه")
    verbose_name_plural = _("التنبيهات")

# تخصيص نموذج الإدارة لنموذج PerformanceReport
class PerformanceReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_date', 'total_tasks', 'completed_tasks', 'overdue_tasks', 'in_progress_tasks', 'points')
    list_filter = ('user', 'report_date')
    search_fields = ('user__username',)  # البحث بالاسم المستخدم
    verbose_name = _("تقرير الأداء")
    verbose_name_plural = _("تقارير الأداء")

# تخصيص نموذج الإدارة لنموذج GoogleCredentials
class GoogleCredentialsAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)  # البحث بالاسم المستخدم
    verbose_name = _("بيانات اعتماد Google")
    verbose_name_plural = _("بيانات اعتماد Google")

# تخصيص نموذج الإدارة لنموذج UserCreation
class UserCreationAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    verbose_name = _("إنشاء مستخدم")
    verbose_name_plural = _("إنشاء المستخدمين")

# تسجيل النماذج مع تخصيصات الإدارة
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(PerformanceReport, PerformanceReportAdmin)


