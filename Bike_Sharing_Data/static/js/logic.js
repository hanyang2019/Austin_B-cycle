//////////////////////////////
// JS Code for Heatmap
/////////////////////////////
function makeheatLayer(array) {
    var heatArray=array.map(s=>[s["Latitude"],s["Longitude"],s["Count"]/1000]);
    //console.log(heatArray);
    var heatMaplayer = L.heatLayer(heatArray, {radius: 45, blur: 35});
    return heatMaplayer;
};

function makemarkerLayer(array) {
    var markerArray=array.map(s=>L.marker([s["Latitude"],s["Longitude"]]).bindPopup(`<h3 align="center">Location: ${s["Kiosk Name"]}</h3><hr><h3 align="center">Usage: ${s["Count"]}</h3>`));
    var markerLayer=L.layerGroup(markerArray);
    return markerLayer;
};


d3.json("/data").then(data=>{
    //console.log(data);
    
    
    var base=L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: apiKey
    });

    var array2014=data.filter(s=>s["Year"]===2014);
    var array2015=data.filter(s=>s["Year"]===2015);
    var array2016=data.filter(s=>s["Year"]===2016);

    var heat2014=makeheatLayer(array2014);
    var heat2015=makeheatLayer(array2015);
    var heat2016=makeheatLayer(array2016);

    var marker2014=makemarkerLayer(array2014);
    var marker2015=makemarkerLayer(array2015);
    var marker2016=makemarkerLayer(array2016);
    

    //console.log(array2014);


    //var heatArray=array2014.map(s=>[s["Latitude"],s["Longitude"],s["Count"]/1000]);
    //console.log(heatArray);
    //var heatMaplayer = L.heatLayer(heatArray, {radius: 25, blur: 15});

    //var markerArray=array2014.map(s=>L.marker([s["Latitude"],s["Longitude"]]).bindPopup(`<h3 align="center">Location: ${s["Kiosk Name"]}</h3><hr><h3 align="center">Usage: ${s["Count"]}</h3>`));
    //var markerLayer=L.layerGroup(markerArray);



    var baseMaps={Base: base};
    var overlayMaps={Heat2014: heat2014, Marker2014: marker2014,Heat2015: heat2015, Marker2015: marker2015,Heat2016: heat2016, Marker2016: marker2016};

    var myMap=L.map("map",{
        center: [30.267153, -97.7430608],
        zoom: 15,
        layers:[base]
    });
    L.control.layers(baseMaps, overlayMaps).addTo(myMap);
    
    


})