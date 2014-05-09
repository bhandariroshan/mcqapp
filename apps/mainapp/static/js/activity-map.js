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
      if (typeof(con.user.business_org_name) == undefined){
        var name = (con.sign_up_as =="Business" || con.sign_up_as == "Organisation") && con.user.business_org_name!= '' ? con.user.business_org_name: con.user.name;
      }
      else{
        var name = con.user.name;
      }
      var status =  con.status;
      var profile_img = con.user.profile_img;
      var username = con.user.username;
      var banner = con.user.banner_url;
      var description = con.user.description;
      var type_user = con.type_user;
      var sign_up_as = con.sign_up_as;
      if(!type_user)
      {
        type_user = [];
      }
      // if(sign_up_as != "Business")
      // {
      //  continue;
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

var card_str = '<div class="card-box"><div class="content text-center"><div class=""><a href="/profile/'+username+'"><img src="'+profile_img+'" alt="'+name+'" class="img-circle img-thumbnail img-responsive" style="width:73px;" /></a>';
    card_str += '</div><div class="text"><h3><a href="/profile/'+username+'">'+name+'</a></h3>';

    if(type_user.length>0)
    {
      card_str += '<div class="  clearfix">';
      for(var j=0;j<type_user.length;j++)
      {  
        
        card_str +=  '<a class="" href="/activity/?b='+type_user[j]+'">'+type_user[j]+'</a>';
       }
        card_str += '</div>';
    }

    card_str += '<p>'+description+'</p></div>';
    card_str += '<a href="/profile/'+username+'" class="btn btn-primary btn-sm">View profile &raquo;</a></div> </div>';

var tweet_id = (con.result_type == username)?con.tweetuid:username;
var ctrl = L.marker([parseFloat(current_lat), parseFloat(current_lon)],{tweet_id:tweet_id,icon: redIcon}).addTo(map).bindPopup(card_str);
      
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


//  MAKES MAP ZOOM TO EXTENT OF ALL CONNECTIONS 
//      map.fitBounds([
//     [min_lat, min_lon],
//     [max_lat, max_lon]
// ]);
      
}




setTimeout(function(){reload_controls()},3000);
