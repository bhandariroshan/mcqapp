$('.li-height').click(function(){
  $(this).effect("highlight", {}, 3000);
   /*$(this).effect( selectedEffect, options, 500, setTimeout(function() {}, 2000 ) );*/
  var clicked = this.children[1].id.substr(9,this.children[1].id.length);
  var check_id = "#inputoption"+clicked;
  $(check_id).trigger('gumby.check');

  ans_html = $('#myAnswers').html();  
      if (click_count%4 ==0){          
           ans_html = ans_html  + '<a href="#"onclick="load_another_question('+ current_question_number +')">' + String(current_question_number+1) +
           '. <li id="liAns"' + String(current_question_number) +'" class="success badge">' + clicked + '</li>&nbsp;&nbsp;&nbsp;</a><br/>';

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
      }
      else{            
            if ((ans_list.indexOf(current_question_number) > -1)==false)  {
              ans_html = ans_html  + '<a href="#" onclick="load_another_question('+ current_question_number +')">' + String(current_question_number+1) + '. <li id="liAns' + + String(current_question_number) +'" class="success badge">' + clicked + '</li></a>&nbsp;&nbsp;&nbsp;';
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
                          $('#liAns'+String(current_question_number)).removeClass('danger');
                          $('#liAns'+String(current_question_number)).addClass('success');
                          $('#aHref'+String(current_question_number)).removeAttr('onclick');
                  //}              

            }
            
          if(current_question_number+1 < max_questions_number){            
           load_another_question(parseInt(current_question_number)+1);
          }
      }
});
 
function load_another_question(q_no){
  var next_question = parseInt(q_no);
  current_question_number = next_question;
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
  
      if (click_count%4 == 0){          
           ans_html = ans_html + '<a href="#" id="aHref"' + String(current_question_number)+ ' onclick="load_another_question('+ current_question_number +')">' + String(current_question_number+1) + '. <li class="danger badge" id="liAns'+ String(current_question_number) +'">' + 'NA' + '</li></a>&nbsp;&nbsp;&nbsp;<br/>';
           if ((ans_list.indexOf(current_question_number) > -1)==false)  {
               $('#myAnswers').html(ans_html);
              click_count = click_count + 1;
              ans_list.push(current_question_number);
              saved_answers[current_question_number] = 'NA';
            }
            else{
              var clicked = this.children[1].id.substr(9,this.children[1].id.length);
              $('#liAns'+String(current_question_number)).html(clicked);
              saved_answers[current_question_number] = clicked;
            }
           
          if(current_question_number+1 < max_questions_number){            
           load_another_question(parseInt(current_question_number)+1);
          }
  }
  else{
        ans_html = ans_html + '<a href="#" id="aHref' + String(current_question_number) +'" onclick="load_another_question('+ current_question_number +')">' + String(current_question_number+1) + '. <li class="danger badge" id="liAns' + String(current_question_number) +'">' + 'NA' + '</li></a>&nbsp;&nbsp;&nbsp;';
        if ((ans_list.indexOf(current_question_number) > -1)==false)  {
            $('#myAnswers').html(ans_html);
            click_count = click_count + 1;
            ans_list.push(current_question_number);
            ans_na.push(String(current_question_number));
            saved_answers[current_question_number] = 'NA';
          }
          else{
            }
        
        if(current_question_number+1 < max_questions_number){            
           load_another_question(parseInt(current_question_number)+1);
          }
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
