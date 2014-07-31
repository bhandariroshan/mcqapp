function ajax_request(s_handler, c_handler, input_data)
{
   $.ajax({
    type: "POST",
    url: "/quiz/quiz-ajax/" + s_handler,
    data: input_data,
    success: function(data) {
      window[c_handler](data);
    }
});
}

function save_quiz_answer(exam_code, question_id, selected_ans, csrf){
	ajax_request('save_quiz_answer', 'save_quiz_answer_success', 
	{'question_id':question_id, 'option':selected_ans, 'exam_code':exam_code, 'csrfmiddlewaretoken':csrf});	
}

function save_quiz_answer_success(data){
	data = jQuery.parseJSON(data);
}

function ajax_set_quiz_finished(exam_code, csrf){
    ajax_request('set_quiz_finished', 'set_quiz_finished_success', {'exam_code':exam_code, 'csrfmiddlewaretoken':csrf});  
}

function set_quiz_finished_success(data){
  data =jQuery.parseJSON(data);
  if(data['status'] == 'success'){
    window.location = '/quiz/myscore/';
  }
}