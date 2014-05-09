

// Location autosuggestions

var placeCord;
function initialize() {

  // Create the search box and link it to the UI element.
  var input = /** @type {HTMLInputElement} */(
      document.getElementById('pac-input'));

  var searchBox = new google.maps.places.SearchBox(
    /** @type {HTMLInputElement} */(input));

  // [START region_getplaces]
  // Listen for the event fired when the user selects an item from the
  // pick list. Retrieve the matching places for that item.
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    loading_latlng = true;
  var places = searchBox.getPlaces();
    placeCord = places[0].geometry.location;
    $("#lon").val(placeCord.lng());
    $("#lat").val(placeCord.lat());
  });
}
google.maps.event.addDomListener(window, 'load', initialize);