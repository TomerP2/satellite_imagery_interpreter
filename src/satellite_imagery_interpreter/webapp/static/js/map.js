const map = L.map('map').setView([52.1, 5.2], 8);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

const drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

const drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
    },
    draw: {
        polygon: true,
        rectangle: true,
        circle: false,
        marker: false,
        polyline: false,
    },
});
map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function (event) {
    const layer = event.layer;
    drawnItems.addLayer(layer);

    const bounds = layer.getBounds();
    const rectangle = [
        bounds.getSouthWest().lng,
        bounds.getSouthWest().lat,
        bounds.getNorthEast().lng,
        bounds.getNorthEast().lat,
    ];

    fetch('/api/get_geotiff', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rectangle }),
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
