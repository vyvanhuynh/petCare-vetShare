'use strict';

function initMap() {
  console.log("start initMap func");
  const map = new google.maps.Map(document.querySelector("#map"), {
    center: {
      lat: 37.601773,
      lng: -122.20287,
    },
    zoom:10,
  });
  console.log(map);
}