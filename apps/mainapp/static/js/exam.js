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
 
function load_question(q_no){
  next_question = parseInt(q_no);
  current_question_number = next_question;
  question_id = questions[current_question_number]['uid']['id'];
  $('#loadNext').attr('id', 'loadNext' + questions[current_question_number]['uid']['id']);
    var question_text = '<span  style="font-weight:bold;"><span style="color:blue;">' + (current_question_number+1) + '. </span>' +  questions[next_question]['question']['text'] + '</span>';

  if (questions[next_question]['question']['image'] != undefined && questions[next_question]['question']['image'] != ''){
        question_text = question_text + '<img src="/static/images/'+ exam_code + '/' + String(questions[next_question]['question']['image']) + '" style=" height:140px;" />'; 
      }
  $('#questionText').html(question_text);

  var option_a_text = '<a href="javascript:void(0)"><span></span>' + questions[next_question]['answer']['a']['text'] + '<br>';
  if (questions[next_question]['answer']['a']['image'] != undefined && questions[next_question]['answer']['a']['image'] != ''){
        option_a_text= option_a_text + '<img src="/static/images/' + exam_code + '/'+ questions[next_question]['answer']['a']['image'] + '" style=" height:140px;" />';
    }
  $('#divOptionA').html(option_a_text + "</a>");

  var option_b_text = '<a href="javascript:void(0)"><span></span>' + questions[next_question]['answer']['b']['text'] + '<br>';
  if (questions[next_question]['answer']['b']['image'] != undefined && questions[next_question]['answer']['b']['image'] != ''){
        option_b_text= option_b_text + '<img src="/static/images/' + exam_code +'/'+ questions[next_question]['answer']['b']['image'] + '" style=" height:140px;" />';
    }
  $('#divOptionB').html(option_b_text + "</a>");

  var option_c_text = '<a href="javascript:void(0)"><span></span>' + questions[next_question]['answer']['c']['text'] + '<br>';
  if (questions[next_question]['answer']['c']['image'] != undefined && questions[next_question]['answer']['c']['image'] != ''){
          option_c_text = option_c_text + '<img src="/static/images/' + exam_code + '/'+ questions[next_question]['answer']['c']['image'] + '" style=" height:140px;" />';
    }    
  $('#divOptionC').html(option_c_text + "</a>");

  var option_d_text = '<a href="javascript:void(0)"><span></span>' + questions[next_question]['answer']['d']['text'] + '<br>';
  if (questions[next_question]['answer']['d']['image'] != undefined && questions[next_question]['answer']['d']['image'] != ''){
          option_d_text= option_d_text + '<img src="/static/images/' + exam_code + '/' + questions[next_question]['answer']['d']['image'] + '" style=" height:140px;" />';
    }
  $('#divOptionD').html(option_d_text + "</a>");  

    sel = $('#liAns'+ (next_question)).html();
    if (sel !='NA'){
      if (sel=='A'){
        $('#a').css("background","#58c026");      
        $('#b').css("background","none");      
        $('#c').css("background","none");      
        $('#d').css("background","none");      
      }
      else if (sel=='B'){
        $('#b').css("background","#58c026");      
        $('#a').css("background","none");      
        $('#c').css("background","none");      
        $('#d').css("background","none");       
      }
      else if (sel=='C'){
        $('#c').css("background","#58c026");      
        $('#a').css("background","none");      
        $('#b').css("background","none");      
        $('#d').css("background","none");       
      }
      else if (sel=='D'){
        $('#d').css("background","#58c026");      
        $('#a').css("background","none");      
        $('#c').css("background","none");      
        $('#b').css("background","none");       
      }
    }
    else{
        $('#a').css("background","none");      
        $('#b').css("background","none");       
        $('#c').css("background","none");      
        $('#d').css("background","none");      
    }
  MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}

$('.loadNext').click(function(){
       ans_html = $('#myAnswers').html();
       ans_html = ans_html + '<button style="border: 0px; background: #fff;display:inline;"" href="#" id="aHref"' + String(current_question_number)+ ' onclick="load_question('+ current_question_number +')">' + String(current_question_number+1) + '. <li class="danger badge" id="liAns'+ String(current_question_number) +'">' + 'NA' + '</li></button>';
       if ((ans_list.indexOf(current_question_number) > -1)==false)  {
           $('#myAnswers').html(ans_html);
          ans_list.push(current_question_number);
          ret_value = save_answer(exam_code, question_id, 'NA', current_question_number);
          
        }
        else{
          try{
            var clicked = this.children[1].id.substr(9,this.children[1].id.length);
            $('#liAns'+String(current_question_number)).html(clicked);
          }
          catch(err){

          }
        }
       
      if(current_question_number+1 < max_questions_number){            
       load_question(parseInt(current_question_number)+1);
       /*$('#aHref'+ String(current_question_number+1)).click();*/
      }
});


$('#loadPrev').click(function(){
    if(current_question_number != 0){                  
      load_question(current_question_number-1);
      /*$('#aHref'+ String(current_question_number-1)).click();*/
    }
});
/*$('.li-height').hover(function(){
  $(this).toggleClass('forum_hover');
});*/

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


$(document).ready(function(){
  ans_html = $('#myAnswers').html();
  var q_no = []
  for (var i = 0; i < all_answers.length; i++){
    q_no.push(all_answers[i]['q_no']);
  }
  for (var i = 0; i < max_questions_number; i++ ){
    ans_list.push(i);      
      if (q_no.indexOf(i) > -1){
        if (all_answers[q_no.indexOf(i)]['selected_ans'] == 'NA'){
          ans_html = ans_html + '<button style="border: 0px; background: #fff;display:inline;"" href="#" id="aHref' + String(all_answers[q_no.indexOf(i)]['q_no']) + '" onclick="load_question('+ String(all_answers[q_no.indexOf(i)]['q_no']) +')">' + String(all_answers[q_no.indexOf(i)]['q_no']+1) + '. <li class="danger badge" id="liAns'+ String(all_answers[q_no.indexOf(i)]['q_no']) +'">' + 'NA' + '</li></button>';      
        }
        else{
          var last_selected_answer  = all_answers[q_no.indexOf(i)]['attempt_details'][all_answers[q_no.indexOf(i)]['attempt_details'].length-1]['selected_ans'];
          ans_html = ans_html + '<button style="border: 0px; background: #fff;display:inline;"" href="#" id="aHref' + String(all_answers[q_no.indexOf(i)]['q_no']) + '"onclick="load_question('+ String(all_answers[q_no.indexOf(i)]['q_no']) +')">' + String(all_answers[q_no.indexOf(i)]['q_no']+1) + '. <li class="success badge" id="liAns'+ String(all_answers[q_no.indexOf(i)]['q_no']) +'">' + last_selected_answer.toUpperCase() + '</li></button>';      
        }                             
      }    
    else{    
        ans_html = ans_html + '<button style="border: 0px; background: #fff;display:inline;"" href="#" id="aHref' + String(i) + '" onclick="load_question('+ String(i) +')">' + String(i+1) + '. <li class="danger badge" id="liAns'+ String(i) +'">' + 'NA' + '</li></button>';
    }
  }
  $('#myAnswers').html(ans_html);
});