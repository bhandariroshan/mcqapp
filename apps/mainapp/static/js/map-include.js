
var base_layer = L.tileLayer('https://{s}.tiles.mapbox.com/v3/foodtrade.i26pc0n5/{z}/{x}/{y}.png', {
maxZoom: 18,
attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>'
});
var openspaceLayer = L.tileLayer.osopenspace("F481BBF739A6038DE0430B6CA40AB6D2", {debug: true}); 

      // map.addLayer(openspaceLayer);
      var show_os_map = true;

// if(map_lat>49.89193 && map_lat<61.08466 && map_lon>-9.38053 && map_lon<2.07316&&show_os_map)
// {
// 	var default_csr = L.OSOpenSpace.getCRS();
// 	current_base_layer = openspaceLayer;
// 	var default_zoom = 4;
// }
// else
// {
// 	var default_csr = L.CRS.EPSG3857;
// 	current_base_layer = base_layer;
// 	var default_zoom = 9;
// }

var default_csr = L.CRS.EPSG3857;
	var current_base_layer = base_layer;
 
	var default_zoom = 9;





$("#map").on('click dblclick keyup mousedown mousewheel mousemove', function() {
       
    	var current_center = map.getCenter();
    	var cent_lon = current_center.lng;
    	var cent_lat = current_center.lat;
    	var current_zoom_level = map.getZoom();

    	var is_current_base = (map.options.crs == L.CRS.EPSG3857);
    	var switching_zoom_level = 7;
// Check if the view is set to UK 
	if(cent_lat>49.89193 && cent_lat<61.08466 && cent_lon>-9.38053 && cent_lon<2.07316&&show_os_map)
    {
    	// Check if it is showing non OS map
    	if(is_current_base)
    	{

    		if(current_zoom_level > 17)
    		{
    			map.options.crs=L.OSOpenSpace.getCRS();
	    		map.removeLayer(base_layer)
	    		map.addLayer(openspaceLayer);
				map.setView([cent_lat,cent_lon],9);

    		}
    		var over_zoom = current_zoom_level-5;
    // 		if(over_zoom>9)
    // 		{
    // 			over_zoom = 9;
    // 		}
    // 		if(over_zoom - switching_zoom_level>0)
    // 		{
    // 			map.options.crs=L.OSOpenSpace.getCRS();
	   //  		map.removeLayer(base_layer)
	   //  		map.addLayer(openspaceLayer);
				// map.setView([cent_lat,cent_lon],over_zoom);

    // 		}
    	}
    	 else
	    {

	    	if(current_zoom_level<9)
	    	{
	    		map.options.crs=L.CRS.EPSG3857;
	    		map.removeLayer(openspaceLayer)
	    		map.addLayer(base_layer);
    			map.setView([cent_lat,cent_lon],18+current_zoom_level-9);
	    	}
	    	// if(current_zoom_level<switching_zoom_level+1)
	    	// {
	    			    	
	    	// 	map.options.crs=L.CRS.EPSG3857;
	    	// 	map.removeLayer(openspaceLayer)
	    	// 	map.addLayer(base_layer);
    		// 	map.setView([cent_lat,cent_lon],current_zoom_level+5);
	    	// }
	    	
	    }
    }
    else
    {
   //  	if(current_zoom_level<1+switching_zoom_level&&(!is_current_base))
   //  	{
   //  		map.options.crs=L.CRS.EPSG3857;
   //  		map.removeLayer(openspaceLayer)
   //  		map.addLayer(base_layer);
			// map.setView([cent_lat,cent_lon],current_zoom_level+5);
   //  	}
    	if((!is_current_base))
    	{
    		map.options.crs=L.CRS.EPSG3857;
    		map.removeLayer(openspaceLayer)
    		map.addLayer(base_layer);
			map.setView([cent_lat,cent_lon],9);
    	}
    }        
});