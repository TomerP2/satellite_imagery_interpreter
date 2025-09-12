const map = L.map('map').setView([52.1, 5.3], 7); // Center on NL

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// FeatureGroup to store drawn shapes
const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

// Drawing controls
const drawControl = new L.Control.Draw({
    edit: { featureGroup: drawnItems },
    draw: { polygon: true, rectangle: false, circle: false, marker: false, polyline: false }
});
map.addControl(drawControl);

// Handle created polygon
map.on(L.Draw.Event.CREATED, function (event) {
    const layer = event.layer;
    drawnItems.addLayer(layer);

    const bounds = layer.getBounds(); // get bounding box
    const rectangle = [
        bounds.getWest(),
        bounds.getSouth(),
        bounds.getEast(),
        bounds.getNorth()
    ];

    fetch("/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ coords: rectangle })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert("GeoTIFF download started!");
        } else {
            alert("Error: " + data.error);
        }
    });
});
