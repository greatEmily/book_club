from django.contrib import admin
from .models import Book, Poll, PollOption, Vote, MemberProfile, Meeting, Attendance

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    search_fields = ("title", "author")

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 3

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("question", "month", "year", "genre", "created_at", "is_closed")
    fields = ("month", "year", "genre", "description", "closes_at", "is_closed")
    inlines = [PollOptionInline]

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("poll", "option", "user", "voted_at")

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "dob_month", "dob_day", "is_new_member", "first_attended_month", "first_attended_year")
    search_fields = ("user__username", "user__email")

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("month", "year", "book")
    list_filter = ("year", "month")
    inlines = [AttendanceInline]

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("meeting", "user", "attended")
    list_filter = ("attended", "meeting__year", "meeting__month")
    search_fields = ("user__username", "user__email")