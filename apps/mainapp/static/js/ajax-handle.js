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
		$('#dangerMessage').html('<li class="danger alert">Invalid Coupon code, you can try for 2 more times before your account gets locked.</li>');
		$('#dangerMessage').show(5000);
	}
}