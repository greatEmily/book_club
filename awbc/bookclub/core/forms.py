from django import forms
from .models import MemberProfile

# Month dropdown choices
MONTH_CHOICES = [
    (0, "---------"),  # hidden default
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
]

YEAR_CHOICES = [(0, "---------")] + [(y, y) for y in range(2017, 2032)]


class MemberProfileForm(forms.ModelForm):
    dob_month = forms.TypedChoiceField(
        choices=MONTH_CHOICES,
        coerce=int,
        required=False,
        label="Birth Month"
    )
    
    dob_day = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=31,
        label="Birth Day"
    )

    is_new_member = forms.BooleanField(
        required=False,
        label="I am a new member"
    )

    first_attended_month = forms.TypedChoiceField(
        choices=MONTH_CHOICES,
        coerce=int,
        required=False,
        label="First Attended Month"
    )

    first_attended_year = forms.TypedChoiceField(
        choices=YEAR_CHOICES,
        coerce=int,
        required=False,
        label="First Attended Year"
    )

    class Meta:
        model = MemberProfile
        fields = [
            "dob_month",
            "dob_day",
            "is_new_member",
            "first_attended_month",
            "first_attended_year",
        ]