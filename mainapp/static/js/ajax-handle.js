global_this = '';
vouch_this = '';
var friends;
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

function tweetlistener(input, counter, button){
    $('#'+input).change(function(){
        checktweet(input, counter, button);
    });
    $('#'+input).keyup(function(){
        checktweet(input, counter, button);
    });
}

function save_favourites(profile_id, user_id){
	if($('#favourite_btn').prop('checked')==true){
		if(profile_id!=user_id){
			ajax_request("save_favourites", 'empty', {data: "{'profile_id': " + parseInt(profile_id) + ",'useruid': " + parseInt(user_id) +"}"});
		}	
	}
	else{
		if(profile_id!=user_id){
				ajax_request("save_favourites", 'empty', {data: "{'profile_id': " + parseInt(profile_id) + ",'useruid': " + parseInt(user_id) +",'delete': " + 1 +"}"});
			}		
	}
	

}

function add_org_to_biz(member_id, orguid){
	// var org_ids_list = $('#org_chosen').val();
	// for(i=0;i<org_ids_list.length;i++){
	ajax_request("third_party_add_org", 'org_ajax', {data: "{'memberuid': " + member_id + ",'orguid': " + parseInt(orguid) +"}"});
	// }
}
// get business tags
function get_business_tags(){
ajax_request("get_business_tags", 'signup_tags_ajax', {data: "{'abc': 'abc' }"});
}

function signup_tags_ajax(data){
$('#business_tags_id').html(data);
$("#business_tags_id").trigger('chosen:updated');
}

function del_org_from_biz(member_id, org_id){
ajax_request("third_party_delete_org", 'org_ajax', {data: "{'memberuid': " + member_id + ",'orguid': " + org_id +"}"});
}

function org_ajax(data){
$('.search-choice').remove();
$("#org_chosen").val('').trigger('chosen:updated');
$('#organisations_list').html(data);
}
function conn_handler(value, prof_id, conn_id)
{
	conn_id = typeof conn_id !== 'undefined' ? conn_id : 0;
	if (validate_login()['status'] == '1'){
				if (value == 'buy_from'){
					var buy = document.getElementById('buy_from').checked
					if (buy==true){
						// create connection of logged in user and profile user
						// ajax_request("add_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'}"});
						ajax_request("add_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'}"});
					}
					else{
						// delete connection
						// ajax_request("del_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'}"})
						ajax_request("del_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'}"})
					}
				}
				else if(value == "sell_to")
				{
					var sell = document.getElementById('sell_to').checked
					if (sell==true){
						// create connection of logged in user and profile user
						// ajax_request("add_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'}"});
						ajax_request("add_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'}"});
					}
					else{
						// delete connection
						// ajax_request("del_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +",'status': 'sell_to'}"});
						ajax_request("del_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +",'status': 'buy_from'}"});
					}

				}
				else if(value == "close_buy_from"){
					
					ajax_request("profile_user_delete_conn", 'stockists_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'" + ", 'conn_id': " + conn_id +"}"});
				}
				else if(value == "close_sell_to"){
					
					ajax_request("profile_user_delete_conn", 'suppliers_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'" + ", 'conn_id': " + conn_id +"}"});
				}				
	}
	else{
		$('#ad_cons_id').tooltip('show');
	}
}

function third_party_connection(prof_id, buss_var, link_type){
	// var business_id = $('#buss_chosen').val().join('');
	// var business_ids_list = $('#buss_chosen').val();

	// for(i=0;i<business_ids_list.length;i++){
	// buyer checked

	if(link_type=='stockists' && buss_var!=""){
		// var conn_data = {prof_id: prof_id, status: 'buy_from', buss_id: businesses_id };
		ajax_request("third_party_conn", 'stockists_ajax', {conn_data: "{'prof_id': " + prof_id + ",'buss_id': " + parseInt(buss_var) + ",'status': 'buy_from'}"});
		
	}
	// seller checked
	if(link_type=='suppliers' && buss_var!=""){
		// var conn_data = {prof_id: prof_id, status: 'sell_to', buss_id: businesses_id };
		ajax_request("third_party_conn", 'suppliers_ajax', {conn_data: "{'prof_id': " + prof_id + ",'buss_id': " + parseInt(buss_var) + ",'status': 'sell_to'}"});
	}
	// }
	
}
function stockists_ajax(data){
// clear selected choice
$('.search-choice').remove();
// $("#buss_chosen").val('').trigger('chosen:updated');

$('#all-stockists').html(data);
reload_connections();
}

function suppliers_ajax(data){
// clear selected choice
$('.search-choice').remove();
// $("#buss_chosen").val('').trigger('chosen:updated');

$('#all-suppliers').html(data);
reload_connections();
}

function create_conn(){
	location.reload();
}

function invite_connect(prof_username, logged_username){
	var message = "Hey, "+ prof_username + " - you may like @foodtradeHQ - the 'dating site for food businesses' #realfood. We're there [http://foodtrade.com/profile/"+logged_username+"]";
	ajax_request("post_tweet_admin", 'create_conn', {message: message});
}

function add_food(prof_id, we_buy){
	if (validate_login()['status'] == '1'){
		
		// var elements = document.getElementsByClassName('search-choice');
	    // var food = elements[0].children[0].innerHTML;
	    var food = $('.search-choice').children()[0].innerHTML;
	    we_buy = typeof we_buy !== 'undefined' ? we_buy : '';
	    var data = {useruid: prof_id, food_name: food};
	    data['we_buy'] = we_buy== '' ? 0 : 1;
	    if(data['we_buy']==1){
			ajax_request("addfood", 'webuy_food_ajax', {data: JSON.stringify(data)});
	    }
	    else{
			ajax_request("addfood", 'food_ajax', {data: JSON.stringify(data)});
		}
	}
	else{
		$('#adfoo_id').tooltip('show');
	}

}

function food_ajax(data){
$('.search-choice').remove();
$("#myselect").val('').trigger('chosen:updated');
$('#foods').html(data);
var $container1 = $('#foods').isotope({itemSelector: '.food'});
}

function webuy_food_ajax(data){
$('.search-choice').remove();
$("#webuy_select").val('').trigger('chosen:updated');
$('#webuy_foods').html(data);
var $container1 = $('#webuy_foods').isotope({itemSelector: '.food'});
}

function recommend_food(logged_in_id, food_name, prof_id, username, my_this){
	var data = {recommender_id: logged_in_id, food_name: food_name, business_id: prof_id, action: 'add'};
	vouch_this = my_this;
	if(vouch_this.checked){
		var url = window.location.href;
		msg = "I've just vouched for #" + food_name.toLocaleLowerCase() + " from " + username + " " + url;
		$('#tweet-recomm').val(msg);
	}
	else{
		data['action'] = 'remove';
	}
	ajax_request("vouch_for_food", 'food_ajax', {data: JSON.stringify(data)});
}

function empty(){}


function delete_food(prof_id, food_name, my_this){
	var data = {useruid: prof_id, food_name: food_name};
	ajax_request("deletefood", 'empty', {data: JSON.stringify(data)});
	global_this = my_this;
	console.log(global_this)
	// var del_id = global_this.parentElement.parentElement.parentElement.parentElement.getAttribute('id');
	var del_id = global_this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('id');
	$('#'+del_id).remove();
}

function add_customer(prof_id, c_id){
	var checked = $('#customer-chkbx').is(':checked');
	var data = {useruid: prof_id, customeruid: c_id};
	if (checked){
		// add customer
		ajax_request("addcustomer", 'create_conn', {data: JSON.stringify(data)});
	}
	else{
		// delete that customer
		ajax_request("deletecustomer", 'create_conn', {data: JSON.stringify(data)});
	}
	
}

function add_member(org_id, mem_id, action){
	var data = {orguid: org_id, memberuid: parseInt(mem_id)};
	if(action == 'self'){
		var checked = $('.member-chkbx').is(':checked');
		if (checked){
			// add member
			ajax_request("addmember", 'member_ajax', {data: JSON.stringify(data)});
		}
		else{
			// delete that member
			ajax_request("deletemember", 'member_ajax', {data: JSON.stringify(data)});
		}
	}
	else if(action == 'third_add'){
		ajax_request("addmember", 'member_ajax', {data: JSON.stringify(data)});
	}
	else if(action == 'third_delete'){
		ajax_request("deletemember", 'member_ajax', {data: JSON.stringify(data)});
	}
	
	
}

function member_ajax(data){
	$('#member_ajax').html(data);
}
function add_team(org_id, team_id){
	// var data = {orguid: org_id, memberuid: team_id};
	// ajax_request("addteam", 'create_conn', {data: JSON.stringify(data)});
	var checked = $('#team-chkbx').is(':checked');
	var data = {orguid: org_id, memberuid: team_id};
	if (checked){
		// add member
		ajax_request("addteam", 'create_conn', {data: JSON.stringify(data)});
	}
	else{
		// delete that member
		ajax_request("deleteteam", 'create_conn', {data: JSON.stringify(data)});
	}
}

function PostStatus(status_val)
{
	ajax_request("post_tweet", 'CloseNewPostModal', {message: status_val});
}

// function CreateConnection(b_useruid, c_useruid)
// {
// 	ajax_request("add_connection", 'create_conn', {conn_data: {'b_useruid'; b_useruid, 'c_useruid': c_useruid}});
// }

// function DeleteConnection(b_useruid, c_useruid)
// {
// 	ajax_request("del_connection", 'del_conn', {conn_data: {'b_useruid'; b_useruid, 'c_useruid': c_useruid}});
// }

function UpdateStatus(id_name, noappend)
{
	noappend = typeof noappend !== 'undefined' ? noappend : '';
	message = $('#'+id_name).val();
	if(message=="")
	{
		alert("You can't post empty status.");
		return;
	}
	if(noappend == 'noappend'){
		ajax_request("post_tweet", 'CloseNewPostModal', {message: message, noappend: 'noappend'});
	}
	else{
		ajax_request("post_tweet", 'CloseNewPostModal', {message: message});
	}
}

var loggedIn = '';
function UpdateActivity(id_name)
{
	message = $('#'+id_name).val();
	if(message=="")
	{
		alert("You can't post empty status.");
		return;
	}
	if(validate_login()['status'] == '1'){
		ajax_request("post_tweet", 'update_activity', {message: message});
	}
	else{
		/*$('#btn_must_be_logged').click();*/
		/*$('#btn_update_activity').tooltip('show');*/
		window.location('/accounts/twitter/login/?process=?login');
	}	
}

function update_activity(status_id)
{
	message = $('#newstatus').val();
	activity_html = $('#status_template').html();
	activity_html = activity_html.replace('===status===',message);
	$('ul.chat').prepend(activity_html);
	$('#newstatus').val("");
}



function CloseNewPostModal()
{
	$('#newtwitterpost').modal('hide');
}















/*function ajax_success_validate_logged_in(data){
	alert(data);
	data = jQuery.parseJSON(data);
	loggedIn = data['status'];
 }*/
