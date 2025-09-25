from django.contrib import admin
from .models import AttendanceRecord, AttendanceEntry


class AttendanceEntryInline(admin.TabularInline):
    model = AttendanceEntry
    extra = 0
    fields = ("start_time", "end_time", "duration_hours")
    readonly_fields = ("duration_hours",)


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "total_duration_hours")
    list_filter = ("date", "user")
    search_fields = ("user__username", "user__email")
    inlines = [AttendanceEntryInline]
