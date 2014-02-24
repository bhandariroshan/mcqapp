
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
			



var map_controls = [];
function reload_connections()
{
	for(var i = 0;i<map_controls.length;i++)
	{
		map.removeLayer(map_controls[i]);
	}
	if(map_controls.length>0)
	{
		connections = new_connections;
	}
	connections.concat(customers);
	map_controls =[];
	var max_lat = parseFloat(map_lat);
	var min_lat = parseFloat(map_lat);
	var max_lon = parseFloat(map_lon);
	var min_lon = parseFloat(map_lon);
		for(var i=0;i<connections.length;i++)
		{
			var con = connections[i];

			var name = con.name;
			// var name = con.business_org_name;
			var description = con.description;
			var photo =  con.photo;
			var username = con.username;
			var type = con.type;
			var relation = con.relation;
			var latitude =  con.latitude;
         	var longitude =  con.longitude;


			var current_lat = parseFloat(latitude);
			var current_lon = parseFloat(longitude);
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



			color = '#890D2F';
			if(relation=="buyer")
			{
				color = "#FC8628";
			}
			var polyline = L.polyline([
			[parseFloat(map_lat), parseFloat(map_lon)],
			[parseFloat(latitude), parseFloat(longitude)]
			],{
				color: color,
				weight: 2,
				opacity: 0.8
			}).addTo(map);
			map_controls.push(polyline);
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

			var ctrl = L.marker([parseFloat(current_lat), parseFloat(current_lon)], {icon: redIcon}).addTo(map).bindPopup(card_str);
			
			map_controls.push(ctrl);

}






for(var j=0;j<customers.length;j++)
		{
			var con1 = customers[j];
			
			var latitude =  con1.latitude;
         	var longitude =  con1.longitude;


			var current_lat = parseFloat(latitude);
			var current_lon = parseFloat(longitude);
			// if(current_lat>max_lat)
			// {
			// 	max_lat = current_lat;
			// }
			// if(current_lat<min_lat)
			// {
			// 	min_lat = current_lat;
			// }

			
			// if(current_lon>max_lon)
			// {
			// 	max_lon = current_lon;
			// }

			// if(current_lon<min_lon)
			// {
			// 	min_lon = current_lon;
			// }




			var dot = L.circleMarker([parseFloat(latitude), parseFloat(longitude)],  {
			
			color: '#100',
			opacity:1,
			weight:1,
			fill:1,
			radius: 3,
			fillColor: "#600",
			fillOpacity: 0.8,

		}).addTo(map);
			map_controls.push(dot);

}





	if(max_lat == min_lat && max_lon==min_lon)
		{
			var padding = 0.3
			max_lat += padding;
			min_lat -= padding;
			max_lon += padding;
			min_lon -= padding;
		}


					  map.fitBounds([
    [min_lat, min_lon],
    [max_lat, max_lon]
]);
		}


setTimeout(function(){reload_connections()},3000);