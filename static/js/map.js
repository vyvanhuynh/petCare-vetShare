'use strict';

function initMap() {
  let map = new google.maps.Map(document.querySelector("#map"), {
    center: {
      lat: 44.954445,
      lng: -93.091301,
    },
    zoom:10,
  });

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      currLocation => {
        alert('Going to your location now!');

        map.setCenter({
          lat: currLocation.coords.latitude,
          lng: currLocation.coords.longitude,
        });
        map.setZoom(18);
      },
      (err) => {
        alert('Unable to get your location :(');
        
      }
    );
  } 
  else {
    alert(`Your browser doesn't support geolocation`);
  }

}
  
