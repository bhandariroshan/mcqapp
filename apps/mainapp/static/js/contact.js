
     function send_email(receiver)
     {
      var sender_name = $("#sender_name").val();
      var sender_email = $("#sender_email").val();
      var receiver_email = receiver;
      var message = $("#email_message").val();



  ajax_request("send_email", 'close_contact_model', {name:sender_name, receiver:receiver_email, sender:sender_email, message:message});  

     }



     
function post_contact_tweet(mention)
{  
  var sender_name = $("#sender_name").val();
      var sender_email = $("#sender_email").val();
      var receiver_email = "sujitmhj@gmail.com";
      var message = mention+" " + $("#email_message").val();
 
  ajax_request("post_tweet_admin", 'close_contact_model', {message: message});
}

     function close_contact_model(data)
{
 
  $('#modal_contact').modal('hide');
}
function check_status(){
  if (validate_login()['status'] == '1'){

  }
  else{
    $('#btn_must_be_logged').click();
  }
}