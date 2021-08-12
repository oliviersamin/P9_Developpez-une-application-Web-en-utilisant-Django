from django import forms
from django.forms import ModelForm, Form
from . import models as mod


class CreateTicket(ModelForm):
    class Meta:
        model = mod.Ticket
        # fields = "__all__"
        fields = ['title', 'description', 'image']
        exclude = ['user', 'time_created']


class CreateReview(ModelForm):
    CHOICES = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = mod.Review
        fields = ['rating', 'headline', 'body']
        exclude = ['ticket', 'user', 'time_created']


class SearchForm(Form):
    username = forms.CharField(label='Search', max_length=50)
