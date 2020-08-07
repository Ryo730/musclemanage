from django import forms
from django.utils import timezone
import datetime

category_choice=(
        ('chest','胸'),
        ('shoulder','肩'),
        ('spine','背中'),
        ('arm','腕'),
        ('abs','腹'),
        ('leg','脚')
    )



class trainlogform(forms.Form):
    used_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mr-2',
                'id': 'date_choice',
                'style': 'width:120px',
                'placeholder': '日付',
                }
            )
        )

    category = forms.ChoiceField(
        choices=category_choice,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
                }
            )
        )

    comment = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mr-3',
                'style': 'width:150px',
                'placeholder': '詳細を入力してください',
                }
            )
        )

    def clean_used_date(self):
            used_date = self.cleaned_data.get('used_date')
            now = (timezone.now() + datetime.timedelta(hours=9)).date()
            if used_date > now:
                self.add_error('used_date', '翌日以降の支出は登録できません')
            return used_date

class BodyWeightform(forms.Form):
     used_date = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mr-2',
                'id': 'date_choice',
                'style': 'width:120px',
                'placeholder': '日付',
                }
            )
        )
     weight=forms.FloatField()

class Spanform(forms.Form):
    spanchoices=(
            (1,'一ヶ月'),
            (2,'二ヶ月'))
    span=forms.MultipleChoiceField(
        choices=spanchoices,
        initial=1,
        widget=forms.CheckboxSelectMultiple()

    )
