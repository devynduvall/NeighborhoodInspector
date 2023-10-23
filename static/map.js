 // Sets the view and map object
 const map = L.map('map').setView([47.60923991620634, -122.33245780856687], 13);

 // Initiallizes the map with the given layer
 L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
 }).addTo(map);

 function addMarker(id, lat, lon){
   // Add marker to map at click location; add popup window
   var newMarker = new L.marker([lat, lon]).addTo(map).on('click', function() {
     $.post("/", {
       marker_id: id
     });

     fetchMarkerPoints(id);

   });
 }
 let lastLayer;

 function fetchMarkerPoints(markerId) {
   if (lastLayer) {
     map.removeLayer(lastLayer);
   }
   
   fetch(`/marker/${markerId}/points`)
     .then(response => response.json())
     .then(data => {
         const layerStyle = {
         fillColor: 'red' // Change the color to red
       };
       
       // Add the additional points to the Leaflet map
       lastLayer = L.geoJSON(data, {
         style: layerStyle // Apply the style to the new layer
       }).addTo(map);

     })
     .catch(error => {
       console.error('Error fetching marker points:', error);
     });
 }

 function navigateToMarker(markerId) {
   
   fetch(`/search/${markerId}`)
     .then(response => response.json())
     .then(data => {
       // Update the map view to the marker's location
       map.setView([data.lat, data.lon], 13);
     })
     .catch(error => {
       console.error('Error fetching marker points:', error);
     });

 }


 function onMarkerSelected(markerId) {
   // Get the ID of the selected marker
   print(markerId)
   // Make an HTTP request to Flask to get updated data
   fetch('/marker-selected/' + markerId)
     .then(function(response) {
       return response;
     })
     .then(function(data) {
       print(data)
       // Update the HTML template with the updated data
       // (Assuming you have a function called "updateTemplate" that updates the HTML)
       // updateTemplate(data);
     });
 }

 function updateTemplate(data) {
   // Update a <div> element with the "name" property of the data
   var nameDiv = document.getElementById("name");
   nameDiv.innerHTML = data.name;
 }

 {% for point in markers %}
   addMarker({{point.id}}, {{point.lat}}, {{point.lon}});
 {% endfor %}