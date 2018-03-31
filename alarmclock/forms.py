from django import forms

class SchedulerForm(forms.Form):

    run = forms.BooleanField()


