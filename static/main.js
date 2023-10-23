// Sets the view and map object
const map = L.map('map').setView([47.60923991620634, -122.33245780856687], 13);

// Initiallizes the map with the given layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

