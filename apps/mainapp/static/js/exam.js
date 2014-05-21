var question_id = '';
$('.li-height').click(function(){
  question_id = this.parentNode.id;
  $(this).effect("highlight", {}, 2000);
  save_answer(exam_code, question_id, this.id);
  var clicked = this.children[1].id.substr(9,this.children[1].id.length);
  var check_id = "#inputoption"+clicked;
  $(check_id).trigger('gumby.check');

  ans_html = $('#myAnswers').html();  
           ans_html = ans_html  + '<button  style="border: 0px;background: #fff; display:inline;" href="#"onclick="load_another_question('+ current_question_number +')">' + String(current_question_number+1) +
           '. <li id="liAns' + String(current_question_number) +'" class="success badge">' + clicked + '</li>&nbsp;&nbsp;&nbsp;</button>';

           if ((ans_list.indexOf(current_question_number) > -1)==false)  {
              $('#myAnswers').html(ans_html);
              click_count = click_count + 1;
              ans_list.push(current_question_number);
              saved_answers[current_question_number] = clicked;
              attempted.push(current_question_number);
            }
            else{
              //if((ans_na.indexOf(current_question_number) > -1)==false){
                      var clicked = this.children[1].id.substr(9,this.children[1].id.length);
                      $('#liAns'+String(current_question_number)).html(clicked);
                      saved_answers[current_question_number] = clicked;
                      attempted.push(current_question_number);
                      $('#liAns'+String(current_question_number)).removeClass('danger');
                      $('#liAns'+String(current_question_number)).addClass('success');
                      $('#aHref'+String(current_question_number)).removeAttr('onclick');
              //}
            }
          if(current_question_number+1 < max_questions_number){            
           load_another_question(parseInt(current_question_number)+1);
          }      
});
 
function load_another_question(q_no){
  var next_question = parseInt(q_no);
  current_question_number = next_question;
  $('#'+question_id).attr('id',questions[current_question_number]['uid']['id']);
    var question_text = '<span><p><strong style="color:blue;">' + String(String(current_question_number+1)) + '. </strong><strong>' +  questions[next_question]['question']['text'] + '</strong></p> </span>';

      if (questions[next_question]['question']['image'] != undefined){
        question_text = question_text + '<img src="/static/images/'+ exam_code + '/' + String(questions[next_question]['question']['image']) + '" style="margin-left:15%; height:140px;" />'; 
      }
  $('#questionText').html(question_text);

  var option_a_text = '<span></span>' +
                questions[next_question]['answer']['a']['text'] + '<br></div>';
               if (questions[next_question]['answer']['a']['image'] != undefined){
                option_a_text= option_a_text + '<img src="/static/images/' + exam_code + '/'+ questions[next_question]['answer']['a']['image'] + '" style="margin-left:15%; height:140px;" />';
               }
  $('#divOptionA').html(option_a_text);

    var option_b_text = '<span></span>'+
                questions[next_question]['answer']['b']['text'] + '<br></div>';
               if (questions[next_question]['answer']['b']['image'] != undefined){
                option_b_text= option_b_text + '<img src="/static/images/' + exam_code +'/'+ questions[next_question]['answer']['b']['image'] + '" style="margin-left:15%; height:140px;" />';
               }
  $('#divOptionB').html(option_b_text);

      var option_c_text = '<span></span>'+
                questions[next_question]['answer']['c']['text'] + '<br></div>';
               if (questions[next_question]['answer']['c']['image'] != undefined){
                option_c_text = option_c_text + '<img src="/static/images/' + exam_code + '/'+ questions[next_question]['answer']['c']['image'] + '" style="margin-left:15%; height:140px;" />';
               }
  $('#divOptionC').html(option_c_text);

      var option_d_text = '<span></span>'+
                questions[next_question]['answer']['d']['text'] + '<br></div>';
               if (questions[next_question]['answer']['d']['image'] != undefined){
                option_d_text= option_d_text + '<img src="/static/images/' + exam_code + '/' + questions[next_question]['answer']['d']['image'] + '" style="margin-left:15%; height:140px;" />';
               }
  $('#divOptionD').html(option_d_text);  
  MathJax.Hub.Queue(["Typeset",MathJax.Hub]);

}

$('#loadNext').click(function(){
  ans_html = $('#myAnswers').html();
           ans_html = ans_html + '<button style="border: 0px; background: #fff;display:inline;"" href="#" id="aHref"' + String(current_question_number)+ ' onclick="load_another_question('+ current_question_number +')">' + String(current_question_number+1) + '. <li class="danger badge" id="liAns'+ String(current_question_number) +'">' + 'NA' + '</li></button>';
           if ((ans_list.indexOf(current_question_number) > -1)==false)  {
               $('#myAnswers').html(ans_html);
              click_count = click_count + 1;
              ans_list.push(current_question_number);
              saved_answers[current_question_number] = 'NA';
            }
            else{
              try{
                var clicked = this.children[1].id.substr(9,this.children[1].id.length);
                $('#liAns'+String(current_question_number)).html(clicked);
                 saved_answers[current_question_number] = clicked;
              }
              catch(err){

              }
            }
           
          if(current_question_number+1 < max_questions_number){            
           load_another_question(parseInt(current_question_number)+1);
          }
});


$('#loadPrev').click(function(){
    if(current_question_number != 0){      
      load_another_question(current_question_number-1);
    }
});
$('.li-height').hover(function(){
  $(this).toggleClass('forum_hover');
});
var toal_time = 60;
var myVar=setInterval(function(){
    if (toal_time !=0 ){
    toal_time = toal_time-1;  
    myTimer();
    }
},1000);

function myTimer() {    
    $("#timeRemained").html('<strong>Time Remained: '+ toal_time +'min</strong>')
}
