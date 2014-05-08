var map = new L.map('map', {
    center: new L.LatLng(map_lat,map_lon),
    crs: default_csr,
    zoom: default_zoom,
	continuousWorld: false,
    worldCopyJump: false,
    layers: [current_base_layer]
});



L.circle([map_lat,map_lon], 24140.2, {
			stroke: 1,
			color: '#00cc00',
			opacity:0.5,
			weight:2,
			fill: 0,
		}).addTo(map);
L.circle([map_lat,map_lon], 48280.3, {
			stroke: 1,
			color: '#ff9900',
			opacity:0.5,
			weight:2,
			fill: 0,
		}).addTo(map);
	
L.circle([map_lat,map_lon], 160934, {
			stroke: 1,
			color: '#999',
			opacity:0.9,
			weight: 1,
			fill: 0,
		}).addTo(map);

 var name = self_info.user.name;
			var status =  self_info.status;
			var profile_img = self_info.user.profile_img;
			var username = self_info.user.username;
			var description = self_info.user.description;
			var type_user = self_info.type_user;
			var sign_up_as = self_info.sign_up_as;
			if(!type_user)
			{
				type_user = [];
			}
			// if(sign_up_as != "Business")
			// {
			// 	continue;
			// }

var card_str = '<div class="card-box"><div class="content"><div class="pull-left"><a href="/profile/'+username+'"><img src="'+profile_img+'" alt="'+name+'" class="img-rounded img-responsive" style="width:40px;" /></a>';

                
                      card_str += '</div><div class="text"><h5><a href="/profile/'+username+'">'+name+'</a></h5>';

                      card_str += '<p class="small">'+description+'</p></div></div>';
                      if(type_user.length>0)
                      {
                    card_str += '<div class="numbers clearfix"><div class="tags tags-biztype pull-left">';
                    for(var j=0;j<type_user.length;j++)
                    {  
                      
                      card_str +=  '<a href="/activity/?b='+type_user[j]+'">'+type_user[j]+'</a>';
                     }
                      card_str += '</div></div>';
                }
                  card_str += '</div> ';

			var ctrl = L.marker([map_lat,map_lon], {icon: redIcon}).addTo(map).bindPopup(card_str);
var map_controls = [];



function reload_controls()
{
	for(var i = 0;i<map_controls.length;i++)
	{
		map.removeLayer(map_controls[i]);
	}
	map_controls =[];
	var max_lat = parseFloat(map_lat);
	var min_lat = parseFloat(map_lat);
	var max_lon = parseFloat(map_lon);
	var min_lon = parseFloat(map_lon);
		for(i=0;i<connections.length;i++)
		{
			var con = connections[i];
			// var name = self_info.user.name;
			var name = self_info.sign_up_as =="Business" || self_info.sign_up_as == "Organisation" ? self_info.user.business_org_name: self_info.user.name;
			var status =  self_info.status;
			var profile_img = self_info.user.profile_img;
			var username = self_info.user.username;
			var description = self_info.user.description;
			var type_user = self_info.type_user;
			var sign_up_as = self_info.sign_up_as;
			if(!type_user)
			{
				type_user = [];
			}
			// if(sign_up_as != "Business")
			// {
			// 	continue;
			// }

			var current_lat = parseFloat(con.location.coordinates[1]);
			var current_lon = parseFloat(con.location.coordinates[0]);

			if(current_lon == def_lon && current_lat == def_lat)
         	{
         		continue;
         	}
			if(current_lat>max_lat)
			{
				max_lat = current_lat;
			}
			if(current_lat<min_lat)
			{
				min_lat = current_lat;
			}

			
			if(current_lon>max_lon)
			{
				max_lon = current_lon;
			}

			if(current_lon<min_lon)
			{
				min_lon = current_lon;
			}

var card_str = '<div class="card-box"><div class="content"><div class="pull-left"><a href="/profile/'+username+'"><img src="'+profile_img+'" alt="'+name+'" class="img-rounded img-responsive" style="width:40px;" /></a>';

                
                      card_str += '</div><div class="text"><h5><a href="/profile/'+username+'">'+name+'</a></h5>';

                      card_str += '<p class="small">'+description+'</p></div></div>';
                      if(type_user.length>0)
                      {
                    card_str += '<div class="numbers clearfix"><div class="tags tags-biztype pull-left">';
                    for(var j=0;j<type_user.length;j++)
                    {  
                      
                      card_str +=  '<a href="/activity/?b='+type_user[j]+'">'+type_user[j]+'</a>';
                     }
                      card_str += '</div></div>';
                }
                  card_str += '</div> ';

			var ctrl = L.marker([parseFloat(current_lat), parseFloat(current_lon)], {icon: redIcon}).addTo(map).bindPopup(card_str);
			
			map_controls.push(ctrl);

		}



		if(max_lat == min_lat && max_lon==min_lon)
		{
			var padding = 0.3
			max_lat += padding;
			min_lat -= padding;
			max_lon += padding;
			min_lon -= padding;
		}



// 		  map.fitBounds([
//     [min_lat, min_lon],
//     [max_lat, max_lon]
// ]);
		


}




setTimeout(function(){reload_controls()},3000);
