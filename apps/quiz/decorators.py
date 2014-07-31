import datetime
import time


def check_quiz_generated(view_func):
    '''
    Condition 1: if the quiz is already generated then return the quiz model
    '''
    from apps.mainapp.classes.query_database import ExammodelApi

    def _wrapped_view_func(*args, **kwargs):
        exam_date = time.mktime(datetime.datetime.now().date().timetuple())
        exammodel_api = ExammodelApi()
        exam_type_dict = {"engineering": "BE-IOE", "medical": "MBBS-IOM"}
        new_exam_model = exammodel_api.find_one_exammodel(
            {"exam_date": exam_date,
             "exam_family": "QUIZ",
             "exam_category": exam_type_dict[str(args[1].lower())]}
        )
        if new_exam_model is not None:
            return new_exam_model

        return view_func(*args, **kwargs)

    return _wrapped_view_func
