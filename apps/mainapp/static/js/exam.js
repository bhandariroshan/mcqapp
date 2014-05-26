$('.li-height').click(function(){
  /*$(this).effect("highlight", {}, 2000);*/
  save_answer(exam_code, question_id, this.id, current_question_number);

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
              $('#aHref'+String(current_question_number)).removeAttr('onclick');
      //}
    }
  if(current_question_number+1 < max_questions_number){
    $('#aHref'+ String(current_question_number+1)).click();
   /*load_question(parseInt(current_question_number)+1);*/
  }

});
 
function load_question(q_no){
  next_question = parseInt(q_no);
  current_question_number = next_question;
  question_id = questions[current_question_number]['uid']['id'];
  $('#loadNext').attr('id', 'loadNext' + questions[current_question_number]['uid']['id']);
    var question_text = '<span><p><strong style="color:blue;">' + String(String(current_question_number+1)) + '. </strong><strong>' +  questions[next_question]['question']['text'] + '</strong></p> </span>';

      if (questions[next_question]['question']['image'] != undefined){
        question_text = question_text + '<img src="/static/images/'+ exam_code + '/' + String(questions[next_question]['question']['image']) + '" style="margin-left:15%; height:140px;" />'; 
      }
  $('#questionText').html(question_text);

  var option_a_text = '<span></span>' + questions[next_question]['answer']['a']['text'] + '<br></div>';
  if (questions[next_question]['answer']['a']['image'] != undefined){
        option_a_text= option_a_text + '<img src="/static/images/' + exam_code + '/'+ questions[next_question]['answer']['a']['image'] + '" style="margin-left:15%; height:140px;" />';
    }
  $('#divOptionA').html(option_a_text);
    var option_b_text = '<span></span>' + questions[next_question]['answer']['b']['text'] + '<br></div>';
    if (questions[next_question]['answer']['b']['image'] != undefined){
        option_b_text= option_b_text + '<img src="/static/images/' + exam_code +'/'+ questions[next_question]['answer']['b']['image'] + '" style="margin-left:15%; height:140px;" />';
    }
  $('#divOptionB').html(option_b_text);
      var option_c_text = '<span></span>' + questions[next_question]['answer']['c']['text'] + '<br></div>';
      if (questions[next_question]['answer']['c']['image'] != undefined){
          option_c_text = option_c_text + '<img src="/static/images/' + exam_code + '/'+ questions[next_question]['answer']['c']['image'] + '" style="margin-left:15%; height:140px;" />';
      }
  $('#divOptionC').html(option_c_text);
    var option_d_text = '<span></span>' + questions[next_question]['answer']['d']['text'] + '<br></div>';
    if (questions[next_question]['answer']['d']['image'] != undefined){
          option_d_text= option_d_text + '<img src="/static/images/' + exam_code + '/' + questions[next_question]['answer']['d']['image'] + '" style="margin-left:15%; height:140px;" />';
    }

  $('#divOptionD').html(option_d_text);  
  MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}

$('.loadNext').click(function(){
       ans_html = $('#myAnswers').html();
       ans_html = ans_html + '<button style="border: 0px; background: #fff;display:inline;"" href="#" id="aHref"' + String(current_question_number)+ ' onclick="load_question('+ current_question_number +')">' + String(current_question_number+1) + '. <li class="danger badge" id="liAns'+ String(current_question_number) +'">' + 'NA' + '</li></button>';
       if ((ans_list.indexOf(current_question_number) > -1)==false)  {
           $('#myAnswers').html(ans_html);
          ans_list.push(current_question_number);
          save_answer(exam_code, question_id, 'NA', current_question_number);
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
       /*load_question(parseInt(current_question_number)+1);*/
       $('#aHref'+ String(current_question_number+1)).click();
      }
});


$('#loadPrev').click(function(){
    if(current_question_number != 0){      
      /*load_question(current_question_number-1);*/
      $('#aHref'+ String(current_question_number-1)).click();
    }
});
/*$('.li-height').hover(function(){
  $(this).toggleClass('forum_hover');
});*/

var hour_rem = exam_duration/60;
var min_rem = parseInt(exam_duration)%60;
var sec_rem = min_rem * 60;
var toal_time = parseInt(exam_duration) * 60;

var myVar=setInterval(function(){
    if (toal_time !=0 ){
        toal_time = toal_time-1;  
        hour_rem  = parseInt(toal_time/3600);
        min_rem   = parseInt(toal_time/60) - hour_rem *60;
        sec_rem   = toal_time - hour_rem*3600 - min_rem*60;
        myTimer();
    }
},1000);

function myTimer() {    
    $("#timeRemained").html('<i class="icon-bell"></i><strong> '+ hour_rem + 'h ' + min_rem + 'm ' + sec_rem  +'s</strong>')
}


$(document).ready(function(){
  ans_html = $('#myAnswers').html();
  var q_no = []
  for (var i = 0; i < all_answers.length; i++ ){
    q_no.push(all_answers[i]['q_no']);
  }
  for (var i = 0; i < max_questions_number; i++ ){
    ans_list.push(i);      
      if (q_no.indexOf(i) > -1){
        if (all_answers[q_no.indexOf(i)]['selected_ans'] == 'NA'){
          ans_html = ans_html + '<button style="border: 0px; background: #fff;display:inline;"" href="#" id="aHref' + String(all_answers[q_no.indexOf(i)]['q_no']) + '" onclick="load_question('+ String(all_answers[q_no.indexOf(i)]['q_no']) +')">' + String(all_answers[q_no.indexOf(i)]['q_no']+1) + '. <li class="danger badge" id="liAns'+ String(all_answers[q_no.indexOf(i)]['q_no']) +'">' + 'NA' + '</li></button>';      
        }
        else{
          ans_html = ans_html + '<button style="border: 0px; background: #fff;display:inline;"" href="#" id="aHref' + String(all_answers[q_no.indexOf(i)]['q_no']) + '"onclick="load_question('+ String(all_answers[q_no.indexOf(i)]['q_no']) +')">' + String(all_answers[q_no.indexOf(i)]['q_no']+1) + '. <li class="success badge" id="liAns'+ String(all_answers[q_no.indexOf(i)]['q_no']) +'">' + all_answers[q_no.indexOf(i)]['selected_ans'].toUpperCase() + '</li></button>';      
        }                             
      }    
    else{    
        ans_html = ans_html + '<button style="border: 0px; background: #fff;display:inline;"" href="#" id="aHref' + String(i) + '" onclick="load_question('+ String(i) +')">' + String(i+1) + '. <li class="danger badge" id="liAns'+ String(i) +'">' + 'NA' + '</li></button>';
    }
  }
  $('#myAnswers').html(ans_html);
});