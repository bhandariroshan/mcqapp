from django import forms

EXAM_CHOICES = (('BE-IOE', 'BE-IOE',),
                ('MBBS-IOM', 'MBBS-IOM'))


class SignupForm(forms.Form):

    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': u'Username',
                               'class': 'form-control'}))

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': u'Email',
                             'class': 'form-control'}))

    # exam_type = forms.MultipleChoiceField(required=True,
    #     widget=forms.CheckboxSelectMultiple, choices=EXAM_CHOICES)

    def signup(self, request, user):
        print 'signup function called'
