import floppyforms as forms

from apps.mainapp.classes.query_database import QuestionApi


class QuestionForm(forms.Form):

    # def __init__(self, *args, **kwargs):
    #     self.cleaned_data = data

    question_api_object = QuestionApi()
    exam_type_choice = [
        (exam_type.lower(), exam_type.upper())
        for exam_type in question_api_object.find_distinct_value('exam_type')['results']
    ]
    subject_choice = [
        (subj.upper(), subj.lower())
        for subj in question_api_object.find_distinct_value('subject')['results']
    ]
    question_text = forms.CharField(
        label='Question Text', widget=forms.Textarea(
            attrs={
                'placeholder': 'Type the question here',
                'required': 'required',
                'rows': 3
            }
        )
    )
    question_image = forms.CharField(label='Question Image', required=False)
    option_a_text = forms.CharField(label='Option a')
    option_a_image = forms.CharField(label='Option a Image', required=False)
    option_b_text = forms.CharField(label='Option b')
    option_b_image = forms.CharField(label='Option b Image', required=False)
    option_c_text = forms.CharField(label='Option c')
    option_c_image = forms.CharField(label='Option c Image', required=False)
    option_d_text = forms.CharField(label='Option d')
    option_d_image = forms.CharField(label='Option d Image', required=False)
    correct = forms.ChoiceField(
        label='Correct', choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')]
    )
    subject = forms.ChoiceField(label='Subject', choices=subject_choice)
    marks = forms.IntegerField()
    exam_code = forms.IntegerField()
    exam_type = forms.ChoiceField(label='Exam Type', choices=exam_type_choice)

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        question_dict = {
            "question": {
                "text": data.get('question_text'),
                "image": data.get('question_image')
            },
            "answer": {
                "a": {
                    "text": data.get('option_a_text'),
                    "image": data.get('option_a_image')
                },
                "b": {
                    "text": data.get('option_b_text'),
                    "image": data.get('option_b_image')
                },
                "c": {
                    "text": data.get('option_c_text'),
                    "image": data.get('option_c_image')
                },
                "d": {
                    "text": data.get('option_d_text'),
                    "image": data.get('option_d_image')
                },
                "correct": str(data.get('correct')).lower()
            },
            "subject": str(data.get('subject')).lower(),
            "marks": int(data.get('marks')),
            "exam_code": int(data.get('exam_code')),
            "exam_type": str(data.get('exam_type')).upper()
        }
        # question_api_object = QuestionApi()
        # question_api_object.insert_new_question(question_dict)
        print question_dict
