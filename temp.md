# Prompt for getting a basic flask - leaflet - html/js script for getting input polygon.

I have built a function, get_geotiff_from_rectangle(rectangle: List of 4 floats), that takes in four coordinates in CRS: RD New, and downloads arial data in the netherlands for that square. I want to create a simple local website, using Flask, Leaflet, Javascript, HTML and CSS, that:
1. Displays a map and asks the user to draw a polygon.
2. When user draws a polygon, call get_geotiff_from_rectangle using that polygon.

The website is meant to run locally by the user. So make it open in the browser if someone runs main.py.

Some requirments:
- Use the flask best practices: https://auth0.com/blog/best-practices-for-flask-api-development/
- Use leaflet best practices: https://infinitejs.com/posts/avoiding-leaflet-pitfalls-java/ and https://leafletjs.com/reference.html
- Use the best practices project structure from https://auth0.com/blog/best-practices-for-flask-api-development/
- Keep the code as simple as possible.
- Use leaflet.draw: https://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html
