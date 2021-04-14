// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 53.3498, lng: 6.2603 },
    zoom: 12,
  });
  infoWindow = new google.maps.InfoWindow();
  new google.maps.Marker({
    position: { lat: 53.382528, lng: -6.276624 },
    map,
  });
  new google.maps.Marker({
    position: { lat: 53.369185, lng: -6.254670 },
    map,
  });
  new google.maps.Marker({
    position: { lat: 53.350244, lng: -6.281777 },
    map,
  });
  new google.maps.Marker({
    position: { lat: 53.322316, lng: -6.265711 },
    map,
  });
  new google.maps.Marker({
    position: { lat: 53.324547, lng: -6.395470 },
    map,
  });
  new google.maps.Marker({
    position: { lat: 53.288162, lng: -6.356774 },
    map,
  });
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };
      infoWindow.setPosition(pos);
      infoWindow.setContent("Location found.");
      infoWindow.open(map);
      map.setCenter(pos);
    },
    () => {
      handleLocationError(true, infoWindow, map.getCenter());
    }
  );

  // Browser doesn't support Geolocation
  handleLocationError(false, infoWindow, map.getCenter());

}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}
