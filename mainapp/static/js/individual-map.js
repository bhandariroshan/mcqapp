
var map = L.map('map').setView([map_lat,map_lon], 7);

 
		L.tileLayer('http://{s}.tile.cloudmade.com/0c670d97b5984ce79b34deb902915b3e/110167/256/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>'
		}).addTo(map);


L.circle([map_lat,map_lon], 24140.2, {
			stroke: 1,
			color: '#00cc00',
			opacity:0.8,
			weight:1,
			fill: 0,
		}).addTo(map);
L.circle([map_lat,map_lon], 48280.3, {
			stroke: 1,
			color: '#ff9900',
			opacity:0.8,
			weight:1,
			fill: 0,
		}).addTo(map);
	
L.circle([map_lat,map_lon], 160934, {
			stroke: 1,
			color: '#444',
			opacity:0.8,
			weight:1,
			fill: 0,
		}).addTo(map);

var card_str = '<div class="card-box"><div class="content"><div class="pull-left"><a href="/profile/'+username+'"><img src="'+photo+'" alt="'+name+'" class="img-rounded img-responsive" style="width:40px;" /></a>';

                
                      card_str += '</div><div class="text"><h5><a href="/profile/'+username+'">'+name+'</a></h5>';

                      card_str += '<p class="small">'+description+'</p></div></div>';
                      if(type.length>0)
                      {
                    card_str += '<div class="numbers clearfix"><div class="tags tags-biztype pull-left">';
                    for(var j=0;j<type.length;j++)
                    {  
                      
                      card_str +=  '<a href="/activity/?q='+type[j]+'">'+type[j]+'</a>';
                     }
                      card_str += '</div></div>';
                }
                  card_str += '</div> ';

		 L.marker([parseFloat(map_lat), parseFloat(map_lon)], {icon: redIcon}).addTo(map).bindPopup(card_str);