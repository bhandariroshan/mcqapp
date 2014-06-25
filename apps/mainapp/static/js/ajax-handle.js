function ajax_request(s_handler, c_handler, input_data)
{
   $.ajax({
    type: "POST",
    url: "/ajax-handler/" + s_handler,
    data: input_data,
    success: function(data) {
      window[c_handler](data);
    }
});
}
function validate_coupon(exam_code, coupon_id){
	ajax_request('validate_coupon', 'validate_coupon_success',{'exam_code':exam_code, 'coupon_code':coupon_id});
}
function get_next_page(exam_code,current, next){
	ajax_request('get_nexp_page_of_questions', 'get_next_page_success', {'exam_code':exam_code, 'current':current, 'next':next});
}


function get_next_page_success(data){
	data= jQuery.parseJSON(data);
	$('#showExam').html('');
	if (data['status'] == 'ok'){
		$('#showExam').html(data['html']);
		Gumby.initialize(['skiplink', 'checkbox', 'radiobtn'], true);
		MathJax.Hub.Queue(["Typeset",MathJax.Hub]);	
		all_ans = data['all_ans'];
		var q_no = []
		for (var i = 0; i < all_ans.length; i++){
    		q_no.push(all_ans[i]['q_no']);
		}

		for (var i = 0; i < all_ans.length; i++ ){
			len = all_ans[i]['attempt_details'].length;
			slected = all_ans[i]['attempt_details'][len-1]['selected_ans'];
			check_id = "#radio_" + q_no[i] + '_' + slected.toUpperCase();
  			$(check_id).trigger('gumby.check');  			
		}
		current_pg_num = data['current_pg_num'];
		$('#full_screen_inner_content').animate({
			   scrollTop: 0
		}, 'slow');
		}

}
function load_result(exm_code){
	ajax_request('load_result', 'load_result_success', {'exam_code':exm_code});
}

function get_unattempted_questions_number(exam_code){
	ajax_request('get_unattempted_questions_number', 'get_unattempted_questions_number_success', {'exam_code':exam_code});
}

function get_unattempted_questions_number_success(data){
	data = jQuery.parseJSON(data);
	if(data['status'] == 'ok'){
		$('#unAttemptedQuestions').html(data['questions']);
		$('#remainingQuestionsClicked').html(data['questions']);
		$('#remaining').html('<a href="javascript:void(0)" style="color:red" id="remained"> Remaining:</a>' + data['notattempted']);
		$('#attempted').html('Attempted:: ' + data['attempted']);
	}

}
function load_result_success(data){
	data= jQuery.parseJSON(data);
	$('#showExam').html('');
	if (data['status'] == 'ok'){
		$('#showExam').html(data['html']);
		$('#showExam').show();
		$('#ioe_system_ender').hide();
	}
}

function validate_coupon_success(data){
	data=jQuery.parseJSON(data);
	if (data['status']=='ok'){
		$('#dangerMessage').html('');
		$('#trigger_gumby_div').click();
		window.location = data['url'];
	}
	else{	
		$('#dangerMessage').html('<li class="danger alert">Invalid Coupon code, Please enter a valid coupon code.</li>');
		$('#dangerMessage').show(5000);
	}
}

function is_subscribed(exam_code){
	ajax_request('is_subscribed', 'is_subscribed_success', {'exam_code':exam_code});
}

function is_subscribed_success(data){
	data = jQuery.parseJSON(data);
	if(data['status']!='ok'){		
		$('#trigger_gumby_div').click();
	}
	else{
		window.location = data['url'];
	}
}

function save_answer(exam_code, question_id, selected_ans,current_question_number){
	ajax_request('save_answer', 'save_answer_success', 
	{'qid':question_id, 'sans':selected_ans, 'exam_code':exam_code, 'current_question_number':current_question_number});

}
function save_answer_success(data){
	data = jQuery.parseJSON(data);
	if (data['status'] == 'TimeElapsedError'){

	}
	else{
		toal_time = data['time_remained']*60;
		get_unattempted_questions_number(exm_code);		
	}
}
function ajax_honor_code_accept(exam_code){
	ajax_request('honor_code_accept', 'honor_code_accept_success', {'exam_code':exam_code});
}
function honor_code_accept_success(data){
	data = jQuery.parseJSON(data);
	if (data['status']=='ok'){
		window.location = data['url'];
	}
}
function ajax_set_exam_finished(exam_code, redirect){
	if (redirect){
		ajax_request('set_exam_finished', 'set_exam_finished_success', {'exam_code':exam_code,'redirect':1});
	}
	else{
		ajax_request('set_exam_finished', 'set_exam_finished_success', {'exam_code':exam_code, 'redirect':0});		
	}
}
function set_exam_finished_success(data){
	data= jQuery.parseJSON(data);
	dat = data;	
	if(data['status'] =='ok' && data['redirect'] == '1'){
		$('#closegumby').click();
		window.location = data['url'];
	}
}

function ajax_save_category(ioe_check, iom_check){
	ajax_request('save_category', 'save_category_success', {'ioe_check':ioe_check,'iom_check':iom_check});	
}

function save_category_success(data){
	data = jQuery.parseJSON(data);
	if(data['status']=='ok'){
		$('#categorySelect').hide();
	}
}