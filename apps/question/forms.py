from django import forms

from apps.mainapp.classes.query_database import QuestionApi


class QuestionForm(forms.Form):

    question_api_object = QuestionApi()
    exam_type_choice = [
        (exam_type.lower(), exam_type.upper())
        for exam_type in question_api_object.find_distinct_value('exam_type')['results']
    ]
    subject_choice = [
        (subj.lower(), subj.upper())
        for subj in question_api_object.find_distinct_value('subject')['results']
    ]

    question_number = forms.IntegerField(label='Question Number')
    question_text = forms.CharField(
        label='Question', widget=forms.Textarea(
            attrs={
                'placeholder': 'Type the question here',
                'required': 'required',
                'rows': 3
            }
        )
    )
    question_image = forms.CharField(label='Question Image', required=False)
    option_a = forms.CharField(
        label='Question', widget=forms.Textarea(
            attrs={
                'placeholder': 'Type option \'A\' here',
                'required': 'required',
                'rows': 3
            }
        )
    )
    option_a_image = forms.CharField(label='Option a Image', required=False)
    option_b = forms.CharField(
        label='Question', widget=forms.Textarea(
            attrs={
                'placeholder': 'Type option "B" here',
                'required': 'required',
                'rows': 3
            }
        )
    )
    option_b_image = forms.CharField(label='Option b Image', required=False)
    option_c = forms.CharField(
        label='Question', widget=forms.Textarea(
            attrs={
                'placeholder': 'Type option "C" here',
                'required': 'required',
                'rows': 3
            }
        )
    )
    option_c_image = forms.CharField(label='Option c Image', required=False)
    option_d = forms.CharField(
        label='Question', widget=forms.Textarea(
            attrs={
                'placeholder': 'Type option "D" here',
                'required': 'required',
                'rows': 3
            }
        )
    )
    option_d_image = forms.CharField(label='Option d Image', required=False)
    subject = forms.ChoiceField(label='Subject', choices=subject_choice)
    exam_code = forms.IntegerField(label='Exam Code')
    exam_type = forms.ChoiceField(label='Exam Type', choices=exam_type_choice)
    marks = forms.IntegerField(label='Marks', initial=1)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(QuestionForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data
        return data
