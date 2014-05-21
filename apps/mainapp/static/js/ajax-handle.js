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

function save_answer(exam_code, question_id, selected_ans){
	ajax_request('save_answer', 'save_answer_success', {'qid':question_id, 'sans':selected_ans, 'exam_code':exam_code});
}
function save_answer_success(data){
	data = jQuery.parseJSON(data);
}