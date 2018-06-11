from django import forms
from .models import SubscriptionPlan


# Used for adding a new subscription
class SubscriptionForm(forms.Form):
    service_name = forms.CharField(max_length=64,
        widget=forms.TextInput( # noqa E128
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the name of the service'
            }
        )
    )
    personal_rating = forms.IntegerField(required=False,
        widget=forms.NumberInput( # noqa E128
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your personal rating of this subscription' # noqa E501
            }
        )
    )
    price = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the price of the subscription'
            }
        )
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the duration (in days)'
            }
        )
    )
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput( # noqa E128
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the beginning of the period' # noqa E501
            }
        )
    )
    link = forms.CharField(
        widget=forms.DateTimeInput( # noqa E128
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the link to the service'
            }
        )
    )
    plan = forms.ModelChoiceField(required=False, queryset=SubscriptionPlan.objects.all()) # noqa E501
    notes = forms.CharField(required=False,
        widget=forms.TextInput( # noqa E128
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter personal notes'
            }
        )
    )
    tags = forms.CharField(required=False,
        widget=forms.TextInput( # noqa E128
            attrs={
                'class': 'form-control',
                'placeholder': 'music science films shows games work etc...'
            }
        )
    )


# Used for adding a new subscription plan
class SubscriptionPlanForm(forms.Form):
    name = forms.CharField(max_length=128,
        widget=forms.TextInput( # noqa E128
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the name of the plan'
            }
        )
    )
    planned_budget = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your planned budget for this plan (in $)'
            }
        )
    )
    planned_amount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the planned amount of subscriptions for this plan' # noqa E501
            }
        )
    )
