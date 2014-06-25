
var hour_rem = exam_duration/60;
var min_rem = parseInt(exam_duration%60);
var sec_rem = min_rem * 60;
var toal_time = exam_duration * 60;

var myVar=setInterval(function(){
    if (toal_time >0 ){
        toal_time = toal_time-1;  
        hour_rem  = parseInt(toal_time/3600);
        min_rem   = parseInt(toal_time/60) - hour_rem *60;
        sec_rem   = parseInt(toal_time - hour_rem*3600 - min_rem*60);
        myTimer();        
        /*alert(toal_time);*/
    }
    else if (toal_time == 0)
    {
      toal_time = toal_time -1;
      $('#reviewAns').hide();
      $('#infoText').html('Your time is up. Please submit answers to view result.');
      ajax_set_exam_finished(exam_code, false);
      $('#trigger_gumby_div').click();
    }
    else{
      $('#reviewAns').hide();
      $('#infoText').html('Your time is up. Please submit answers to view result.');
      $('#trigger_gumby_div').click(); 
    }
},1000);

function myTimer() {    
    $("#timeRemained").html('<i class="icon-clock"></i><strong> '+ hour_rem + 'h ' + min_rem + 'm ' + sec_rem  +'s</strong>')
}


$('.li-height').click(function(){
  /*$(this).effect("highlight", {}, 2000);*/
  ret_value = save_answer(exam_code, question_id, this.id, current_question_number);

  var clicked = this.children[1].id.substr(9,this.children[1].id.length);
  var check_id = "#inputoption"+clicked;
  $(check_id).trigger('gumby.check');

   ans_html = $('#myAnswers').html();  
   ans_html = ans_html  + '<button  style="border: 0px;background: #fff; display:inline;" href="#" onclick="load_question('+ current_question_number +')">' + String(current_question_number+1) +
   '. <li id="liAns' + String(current_question_number) +'" class="success badge">' + clicked + '</li></button>';

   if ((ans_list.indexOf(current_question_number) > -1)==false)  {
      $('#myAnswers').html(ans_html);
      ans_list.push(current_question_number);
    }
    else{
      //if((ans_na.indexOf(current_question_number) > -1)==false){
              var clicked = this.children[1].id.substr(9,this.children[1].id.length);
              $('#liAns'+String(current_question_number)).html(clicked);
              attempted.push(current_question_number);
              $('#liAns'+String(current_question_number)).removeClass('danger');
              $('#liAns'+String(current_question_number)).addClass('success');
              /*$('#aHref'+String(current_question_number)).removeAttr('onclick');*/
      //}
    }
  if(current_question_number+1 < max_questions_number){
    /*$('#aHref'+ String(current_question_number+1)).click();*/
   load_question(parseInt(current_question_number)+1);
  }
  else{
    $('#trigger_gumby_div').click();
  }

});