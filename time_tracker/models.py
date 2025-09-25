from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class AttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(default=timezone.localdate, db_index=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date", "-id"]

    def __str__(self) -> str:
        return f"{self.user} - {self.date}"

    @property
    def total_duration_seconds(self) -> int:
        total = 0
        for entry in self.entries.all():
            total += entry.duration_seconds
        return total

    @property
    def total_duration_hours(self) -> float:
        return round(self.total_duration_seconds / 3600.0, 2)


class AttendanceEntry(models.Model):
    record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name="entries")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-start_time", "-id"]

    def __str__(self) -> str:
        return f"{self.record.user} {self.record.date} ({self.start_time} - {self.end_time or '...'} )"

    @property
    def is_open(self) -> bool:
        return self.end_time is None

    @property
    def duration_seconds(self) -> int:
        if self.start_time and self.end_time:
            return int((self.end_time - self.start_time).total_seconds())
        return 0

    @property
    def duration_hours(self) -> float:
        return round(self.duration_seconds / 3600.0, 2)

# Create your models here.
