
$(".reply_text").on('focus', '.reply_input', function(e) {
  var that = e.target;
     if(validate_login()['status'] == '1'){
    if($(that).val()=="")
    {
      var mentions = $(that).attr("data-mentions");
    $(that).val(mentions + " ");
    }
  }
  else{
    window.location='/accounts/twitter/login/?process=login'
  }
});



$(".reply_text").on('blur', '.reply_input', function(e) {
  var that = e.target;
     if($(that).val().trim()==$(that).attr("data-mentions")){
    $(that).val("");
  }
});




$(".reply_text").on("click",".deletetweet",function(e){

  
 
  var that = $(this);
  $.ajax({
    type: "POST",
    url: "/ajax-handler/activity_handle",
    data: {'changeID':that.attr("data-tweet-id"), 'task':'delete'},
    success: function(data) {
      var data_json = jQuery.parseJSON(data);
      if(data_json['status'] == '1')
      {
        that.parent().parent().parent().parent().parent().remove();
      }
      
    }
    });
  
});

var result_mouseout = true;
$(".reply_text").on("mouseover",".singleresult",function(e){
 var result_id = $(this).attr("data-id");
   // console.log(result_id);
 for(var i = 0; i<map_controls.length;i++)
 {
    // console.log(map_controls[i].options.tweet_id);
  if(String(map_controls[i].options.tweet_id).trim() == String(result_id).trim())
  {
    result_mouseout = false;

    map_controls[i].openPopup();
  }
 }
  
});

$(".reply_text").on("mouseout",".singleresult",function(e){
 var result_id = $(this).attr("data-id");
   // console.log(result_id);
 for(var i = 0; i<map_controls.length;i++)
 {
    // console.log(map_controls[i].options.tweet_id);
  if(String(map_controls[i].options.tweet_id).trim() == String(result_id).trim())
  {
    result_mouseout = true;
    highlighted_marker = map_controls[i];
    setTimeout(function() {   
        if(result_mouseout)
        {
          highlighted_marker.closePopup();
        }
    }, 1000);
    break;
    
  }
 }
  
});

var nnn;
$("#filtered_content").on('keypress', '.reply_input', function(e) {
  if(validate_login()['status'] == '1'){
    var code = e.keyCode || e.which;
     if(code == 13) { //Enter keycode

       //Do something
       status_msg =this.value;
       if(status_msg=="")
       {
          return;
       }
        var tweet_id = $(this).attr("data-tweet-id");
       ajax_request("post_tweet", 'make_search', {message: status_msg, parentid:tweet_id});
       // this.value = "";

  // activity_html = $('#status_template').html();
  // activity_html = activity_html.replace('===status===',status_msg);
  // var input_type = $(this).attr("data-main");
  // if(input_type=="reply")
  // {
  //   $(this).parent().parent().html($(this).parent().parent().html()+activity_html);

  // }
  // else
  // {
  //   $(this).parent().parent().next().children().html($(this).parent().parent().next().children().html()+activity_html);
  // }
  
      
  //   $(this).focus();
     
  }
}
  else{
    /*$('#btn_must_be_logged').click();*/
    /*$('#' + String(this.attributes.id.value)).tooltip('show');*/
      /*alert("roshan");*/
      window.location = '/accounts/twitter/login/?process=login';
  }
});


function single_post_content_new_post(){

       var status_msg = $("#main_post_input").val();
       if(status_msg=="")
       {
          return;
       }
        var tweet_id = $("#main_post_input").attr("data-tweet-id");
       ajax_request("post_tweet", 'update_single_post_content', {message: status_msg, parentid:tweet_id});

}

$("#single_post_content").on('keypress', '.reply_input', function(e) {
  if(validate_login()['status'] == '1'){
    var code = e.keyCode || e.which;
     if(code == 13) { //Enter keycode
      status_msg = this.value;
       if(status_msg=="")
       {
          return;
       }
        var tweet_id = $(this).attr("data-tweet-id");
       ajax_request("post_tweet", 'update_single_post_content', {message: status_msg, parentid:tweet_id});

     
  }
}
  else{

      window.location = '/accounts/twitter/login/?process=login';
  }
});

function update_single_post_content()
{
  var tweet_id = $("#main_post_input").attr("data-tweet-id");
  ajax_request("single_post_ajax", 'ajax_update_single_post', {parentid:tweet_id});
}

function ajax_update_single_post(data)
{
  var data_json = jQuery.parseJSON(data);
  $("#main_post_input").val('');
  if(data_json.status == 1)
  {
     $('#update_content').html(data_json.result);
      connections = new_connections;
      reload_controls();

  }
}


function post_new_status()
{
       message = $('#newstatus').val();
  if(message=="")
  {
    alert("You can't post empty status.");
    return;
  }

  if($('#post_to_twitter').prop('checked'))
  {
    var foodtrade_only = "false";

  }
  else
  {
    var foodtrade_only = "true";
  }
  if(validate_login()['status'] == '1'){
    ajax_request("post_tweet", 'clear_input', {message: message,foodtrade_only:foodtrade_only});
  }
  else{
    /*$('#btn_must_be_logged').click();*/
    /*$('#btn_update_activity').tooltip('show');*/
    window.location('/accounts/twitter/login/?process=?login');
  }
}

$('#newstatus').bind('keypress', function(e) {
  
    var code = e.keyCode || e.which;
     if(code == 13) { //Enter keycode
       //Do something
   
      post_new_status();
     }
  
  
});

function clear_input()
{
  $('#newstatus').val('');
  make_search();

}

 function login_redirect(){
            window.location = '/accounts/twitter/login/?process=login';
          }

        
          

          function food_value_changed(more_no)
          {
                   var results = [];
       var query = $("#food_filter").val().toLowerCase();
        for(var i = 0; i < food_filters.length;i++)
        {
          var element  = food_filters[i].uid.toLowerCase();
          if(element.indexOf(query)>-1)
          {
            results.push(food_filters[i]);
          }
        }

            show_food_filters(results,more_no);
          }

          function show_food_filters(filters, more_no)
          {
            if(more_no == 0){
            $('#food_filter_results').html('');
            }
            else
            {
              $("#food_more_"+(more_no-5)).remove();
            }
            for(var i = more_no;i<filters.length && i<(more_no+5); i++)
            {
              var checked = '';
              if(filters[i].prev)
              {
                checked = "checked='checked'";
              }
 if(filters[i].uid!="")
              {
            var row = '<li data-id="15" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" '+checked+' onClick="foods_changed(this,\''+filters[i].uid+'\')" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text"> '+filters[i].uid+'</div><div class="foodtrade-tag-count">'+filters[i].value+'</div></li>';
            $('#food_filter_results').append(row);
          }
           
          }
           if(filters.length>more_no+5)
            {
              $('#food_filter_results').append('<li class="foodtrade-tag-showmore" id="food_more_'+more_no+'" onClick="food_value_changed('+(more_no+5)+')">show more</li>');
            }
          }





            function foods_changed(ref,food)
          {
for(var i = 0; i < food_filters.length;i++){
          if(food_filters[i].uid==food)
          {
            var status = ref.checked;
            //console.log(status);
            food_filters[i].prev = status;
          }
          }
          make_search();
        }









          

          function business_value_changed(more_no)
          {
                   var results = [];
       var query = $("#business_filter").val().toLowerCase();
        for(var i = 0; i < business_filters.length;i++)
        {
          var element  = business_filters[i].uid.toLowerCase();
          if(element.indexOf(query)>-1)
          {
            results.push(business_filters[i]);
          }
        }

            show_business_filters(results,more_no);
          }

          function show_business_filters(filters, more_no)
          {
            if(more_no == 0){
            $('#business_filter_results').html('');
            }
            else
            {
              $("#business_more_"+(more_no-5)).remove();
            }
            for(var i = more_no;i<filters.length && i<(more_no+5); i++)
            {
              var checked = '';
              if(filters[i].prev)
              {
                checked = "checked='checked'";
              }
 if(filters[i].uid!="")
              {
            var row = '<li data-id="15" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" '+checked+' onClick="business_changed(this,\''+filters[i].uid+'\')"   class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text"> '+filters[i].uid+'</div><div class="foodtrade-tag-count">'+filters[i].value+'</div></li>';
            $('#business_filter_results').append(row);
          }
           
          }
           if(filters.length>more_no+5)
            {
              $('#business_filter_results').append('<li class="foodtrade-tag-showmore" id="business_more_'+more_no+'" onClick="business_value_changed('+(more_no+5)+')">show more</li>');
            }
          }





            function business_changed(ref,business)
          {
for(var i = 0; i < business_filters.length;i++){
          if(business_filters[i].uid==business)
          {
            var status = ref.checked;
            //console.log(status);
            business_filters[i].prev = status;
          }
          }
          make_search();
        }







          

          function organisation_value_changed(more_no)
          {
                   var results = [];
       var query = $("#organisation_filter").val().toLowerCase();
        for(var i = 0; i < organisation_filters.length;i++)
        {
          var element  = organisation_filters[i].uid.toLowerCase();
          if(element.indexOf(query)>-1)
          {
            results.push(organisation_filters[i]);
          }
        }

            show_organisation_filters(results,more_no);
          }

          function show_organisation_filters(filters, more_no)
          {
            if(more_no == 0){
            $('#organisation_filter_results').html('');
            }
            else
            {
              $("#organisation_more_"+(more_no-5)).remove();
            }
            for(var i = more_no;i<filters.length && i<(more_no+5); i++)
            {
              var checked = '';
              if(filters[i].prev)
              {
                checked = "checked='checked'";
              }
              if(filters[i].uid!="")
              {
            var row = '<li data-id="15" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" '+checked+' onClick="organisation_changed(this,\''+filters[i].uid+'\')"   class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text"> '+filters[i].uid+'</div><div class="foodtrade-tag-count">'+filters[i].value+'</div></li>';
            $('#organisation_filter_results').append(row);
          }
           
          }
           if(filters.length>more_no+5)
            {
              $('#organisation_filter_results').append('<li class="foodtrade-tag-showmore" id="organisation_more_'+more_no+'" onClick="organisation_value_changed('+(more_no+5)+')">show more</li>');
            }
          }





            function organisation_changed(ref,organisation)
          {
          for(var i = 0; i < organisation_filters.length;i++){
          if(organisation_filters[i].uid==organisation)
          {
            var status = ref.checked;
            //console.log(status);
            organisation_filters[i].prev = status;
          }
          }
          make_search();
        }








       function make_search()
       {
        var foods = [];
        var flag = false;
        
          for(var i = 0; i < food_filters.length;i++){
          if(food_filters[i].prev)
          {
            flag = true;
            foods.push(food_filters[i].uid);
          }
          }

          if(flag)
        {
           $('#all_foods').prop('checked', false);
          }
          else
          {
            $('#all_foods').prop('checked', true);
          }
          flag = false;
       


          var businesses = [];
          
          
          for(var i = 0; i < business_filters.length;i++){
          if(business_filters[i].prev)
          {
            flag =true;
            businesses.push(business_filters[i].uid);
          }
        }
        if(flag)
        {
           $('#all_businesses').prop('checked', false);
          }
          else
          {
            $('#all_businesses').prop('checked', true);
          }
          flag = false;




            var organisations = [];
          
          for(var i = 0; i < organisation_filters.length;i++){
          if(organisation_filters[i].prev)
          {
            flag = true;
            organisations.push(organisation_filters[i].uid);
          }
          }
          if(flag)
        {
           $('#all_organisations').prop('checked', false);
          }
          else
          {
            $('#all_organisations').prop('checked', true);
          }
          flag = false;
       
          var keyword = $("#keyword").val();
          var s_lon = $("#lon").val();
          var s_lat = $("#lat").val();
          var sort_type = $("#current_sort_order").val();


           ajax_request("ajax_search", 'show_ajax_results', {q:keyword, lon:s_lon, lat:s_lat, foods:JSON.stringify(foods), businesses:JSON.stringify(businesses), organisations:JSON.stringify(organisations), sort: sort_type});
       }


       function show_ajax_results(data)
       {
        var data_json = jQuery.parseJSON(data);
         $('#activity_updates').html(data_json.updates);
         $('#activity_biz').html(data_json.biz);
         $('#activity_org').html(data_json.org);
         $('#update_count').html(data_json.results_updates_count);
         $('#business_count').html(data_json.results_business_count);
         $('#organisation_count').html(data_json.results_organisation_count);
         connections = ajax_connections;
         reload_controls();

       }
$('#food_filter').keyup( function() {
            food_value_changed(0);
        });


$('#business_filter').keyup( function() {
            business_value_changed(0);
        });

$('#organisation_filter').keyup( function() {
            organisation_value_changed(0);
        });




function click_activity(activity, changeID){
  ajax_request('activity_handle','success_activity_handle',{'user':'{{userinfo.username}}', 'changeID':changeID, 'task':activity});

}
function success_activity_handle(data){
  data = jQuery.parseJSON(data);
  if(data['status'] == 1 && data['activity'] == 'deleteTweet'){
    $('#' + String(data['_id'])).hide();
  }
  if(data['activity'] == 'follow' ){
    alert(data['message']);
  }
  if((data['activity'] == 'buyFrom' && data['status'] == 0) || 
    (data['activity'] == 'sellTo' && data['status'] ==0) || 
    (data['activity'] == 'markMember' && data['status'] == 0) ||
    (data['activity'] == 'spam' && data['status'] == 0)){
   alert(data['message']); 
  }

}


function sort_by(sort,that)
{
   $("#current_sort_order").val(sort);
   make_search();
  
   $("#current_sort_text").html($(that).html());
   

}
function switch_text_area(){
  $('#update-small').hide();
  $('#update-big').attr('class', 'well well-sm clearfix');
}
function check_limit(){
  tweet = $('#newstatus').val();
  if(tweet.length > 120){
    $('#charsRem').html( 'Max of 120 characters exceeded.');
  }
  else{
    $('#charsRem').html(String(120-tweet.length) + ' characters remaining.');
  }
}