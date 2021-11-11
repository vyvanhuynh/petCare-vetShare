'use strict';
let map, infoWindow, bounds, service, places, currentInfoWindow
let markers = []
function initMap() {
  bounds = new google.maps.LatLngBounds();
  infoWindow = new google.maps.InfoWindow();
  currentInfoWindow = infoWindow;
  map = new google.maps.Map(document.querySelector("#map"), {
    center: {
      lat: 44.954445,
      lng: -93.091301,
    },
    zoom:10,
  });

  // Get the user's location; display on the map the user's location and nearby vets 
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      // the pass function
      currLocation => {
        alert('Going to your location now!');
        const pos = {
          lat: currLocation.coords.latitude,
          lng: currLocation.coords.longitude,
        };

        infoWindow.setPosition(pos);
        infoWindow.setContent("Your current location.");
        infoWindow.open(map);
        
        map.setCenter(pos);
        map.setZoom(12);
      
        // Call the function that displays the nearby vets
        getVetNearby(pos);
      },
      // the fail function
      (fail) => {
        alert('Unable to get your location :(');
      }
    );
  } 
  else {
    alert(`Your browser doesn't support geolocation`);
  }

}

// Performs nearby search based on the keyword list; 
// display places within the window frame
function getVetNearby(position){
  let nearbyRequest = {
    location: position,
    bounds: map.getBounds(),
    keyword: ['vet', 'veterinary clinic', 'animal hospital', 'pet hospital'],
  }

  service = new google.maps.places.PlacesService(map);
  service.nearbySearch(nearbyRequest, nearbyCallback);
}

// The callback func for nearbySearch; 
// check if the status is OK then create a marker
function nearbyCallback(nearbyResults, nearbyStatus){
  if( nearbyStatus == google.maps.places.PlacesServiceStatus.OK){
    createMarker(nearbyResults);
  }
}

// Create a marker and set at each nearby place found 
function createMarker(places){
  places.forEach(place => {
    let marker = new google.maps.Marker({
      position: place.geometry.location,
      map: map,
      title: place.name,
    });
    // Add an envent listener to each marker
    google.maps.event.addListener(marker, "click", () => {
      let detailRequest = { 
        placeId: place.place_id,
        fields: ['name', 'formatted_address', 'geometry', 'rating',
                'website']
      };
      // Get the details only when user clicks on marker
      service.getDetails(detailRequest, (detailResult, detailStatus)=> {
        showDetails(detailResult, marker, detailStatus)
      });
      // Center the marker when clicked
      map.setCenter(place.geometry.location);
    });
    // Adjust map bounds to include the location of this marker
    bounds.extend(place.geometry.location);
  });
  // Adjust the bound to show all the markers
  map.fitBounds(bounds);

}

// Show place details in content window when a marker is clicked
function showDetails(placeResult, marker, placeStatus){
  if (placeStatus == google.maps.places.PlacesServiceStatus.OK) {
    let placeInfoWindow = new google.maps.InfoWindow();
    let placeRating = "None";
    // Check if the place has any rating
    if (placeResult.rating) {
      placeRating = placeResult.rating
      };
    // Set the content in the info window 
    placeInfoWindow.setContent('<div><strong>' + placeResult.name + '</strong><br>' 
                                  + 'Rating: ' + placeRating + '<br>'  
                                  + 'Address: ' + placeResult.formatted_address + '<br>'
                                  + 'Website: ' + '<a href="' + placeResult.website + '">' + placeResult.website + '</a>' 
                                  + '</div>');
    placeInfoWindow.open(marker.map, marker);
    currentInfoWindow.close();
    currentInfoWindow = placeInfoWindow;
  } 
  else {
    console.log("showDetails failed: " + placeStatus);
  }
}
