from django.db import models
from django.conf import settings

# Create your models here.

# Book
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    cover_image_url = models.URLField(blank=True)
    goodreads_url = models.URLField(blank=True)
    publication_year = models.PositiveSmallIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title

# Poll
class Poll(models.Model):
    MONTH_CHOICES = [
        (1, "January"), (2, "February"), (3, "March"), (4, "April"),
        (5, "May"), (6, "June"), (7, "July"), (8, "August"),
        (9, "September"), (10, "October"), (11, "November"), (12, "December"),
    ]

    month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES)
    year = models.PositiveSmallIntegerField()
    genre = models.CharField(max_length=100, blank=True)

    # You no longer need a manually entered question
    question = models.CharField(max_length=255, editable=False)

    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    closes_at = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Build the dynamic title automatically
        month_name = dict(self.MONTH_CHOICES).get(self.month, "")
        genre_part = f" - {self.genre}" if self.genre else ""
        self.question = f"{month_name} {self.year} Book Club Poll{genre_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question

    @property
    def open(self):
        if self.is_closed:
            return False
        if self.closes_at:
            return timezone.now() < self.closes_at
        return True

# Poll Options
class PollOption(models.Model):
    poll = models.ForeignKey(Poll, related_name="options", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.poll.question} – {self.book.title}"

# Votes
class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name="votes", on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, related_name="votes", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("poll", "user")

    def __str__(self):
        return f"{self.user} → {self.option.book.title}"

# Profile
class MemberProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # DOB without year
    dob_month = models.PositiveSmallIntegerField(null=True, blank=True)
    dob_day = models.PositiveSmallIntegerField(null=True, blank=True)

    # Book club history
    is_new_member = models.BooleanField(default=False)
    first_attended_month = models.PositiveSmallIntegerField(null=True, blank=True)
    first_attended_year = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

# Meetings
class Meeting(models.Model):
    MONTH_CHOICES = [
        (1, "January"), (2, "February"), (3, "March"), (4, "April"),
        (5, "May"), (6, "June"), (7, "July"), (8, "August"),
        (9, "September"), (10, "October"), (11, "November"), (12, "December"),
    ]

    month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES)
    year = models.PositiveSmallIntegerField()

    # Optional: actual meeting date if you want to track it
    date = models.DateField(null=True, blank=True)

    # Optional: link to the book read that month
    book = models.ForeignKey(
        Book,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="meetings",
    )

    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("month", "year")
        ordering = ["-year", "-month"]

    def __str__(self):
        month_name = dict(self.MONTH_CHOICES).get(self.month, "")
        return f"{month_name} {self.year} Meeting"

# Attendance
class Attendance(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name="attendance",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ("meeting", "user")

    def __str__(self):
        return f"{self.user.username} – {self.meeting} – {'Yes' if self.attended else 'No'}"
