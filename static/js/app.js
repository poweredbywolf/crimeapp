
// App Class was imported from Google APIs
// The API into google imports class and has a call back which is the function below
// i.e. initMap()

// *-------------Call Back Function to Initialise map  ------------------------------------*
"use strict";
  
let map;
let position_playful;

let latlong_lastClick = ""

function initMap() {

// Creates map object 
  map = new google.maps.Map(document.getElementById("map"), {
    center: {
      lat: -26.397,
      lng: 28
    },
    zoom: 8  // when it instaniates the object it will do it at this zoom level

  });

  // *-------------Call Back Function- End --------------------------------------------*



// Create the initial InfoWindow.

var myLatlng = {lat: -25.363, lng: 28};
var infoWindow = new google.maps.InfoWindow(
    {content: 'Click the map to get Lat/Lng!', position: myLatlng});
infoWindow.open(map);


// Configure the click listener.
map.addListener('click', function(mapsMouseEvent) {
  // Close the current InfoWindow.
  infoWindow.close();

  // Create a new InfoWindow.
  infoWindow = new google.maps.InfoWindow({position: mapsMouseEvent.latLng});
  infoWindow.setContent(mapsMouseEvent.latLng.toString());
  infoWindow.open(map);
  // {lat: -25.344, lng: 131.036};

  // leaving a marker
  var marker = new google.maps.Marker({position: mapsMouseEvent.latLng, map: map});
  latlong_lastClick = mapsMouseEvent.latLng.toString()
  
  position_playful = mapsMouseEvent.latLng;

  console.log(latlong_lastClick);
 

  // adding clicked position to form 
  document.getElementById("latitude").value = position_playful.lat()
  document.getElementById("longitude").value = position_playful.lng()



});

}




// // Create the script tag, set the appropriate attributes
// var script = document.createElement('script');
// script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyDQ4N5IuJnVknSMLxO2ZO4rOujEKJHjVrw&callback=initMap';
// script.defer = true;

// // Attach your callback function to the `window` object
// window.initMap = function() {
//   // JS API is loaded and available
// };

// // Append the 'script' element to 'head'
// document.head.appendChild(script);