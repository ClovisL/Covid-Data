// Perform an API call to the Our world in data 
d3.json("https://covid.ourworldindata.org/data/owid-covid-data.json").then(function(data){

    var data = Object.entries(data);
    
    var countries = [];

    data.forEach((d) => {
        var info = {};

        var dates = d[1].data;
        if(coor(d[1].location) != null)
        {
            info.location = d[1].location;
            var dates = d[1].data;
            info.total_cases = +d[1].data[dates.length-1].total_cases;
            if(d[1].data[dates.length-1].total_vaccinations == null)
                info.total_vaccinations = 0;
            else 
                info.total_vaccinations = +d[1].data[dates.length-1].total_vaccinations;
            info.coordinates = coor(info.location);
            info.lastDate = d[1].data[dates.length-1].date;
            countries.push(info);
        }
    });

    console.log(countries);

    createMap(countries);
});

function coor(c){
    switch(c){
        case "United States":
            return [39.106667, -94.676392];
            break;
        case "India":
            return [23.152790, 79.947327];
            break;
        case "Brazil":
            return [-9.8850, -56.0857];
            break;
        case "Russia":
            return [56.501040, 84.97437];
            break;
        case "France":
            return [47.082508, 2.399341];
            break;
        case "UK":
            return [53.478062, -2.244666];
            break;
        case "Turkey":
            return [38.734802, 35.467987];
            break;
        case "Argentina":
            return [-36.216700, -65.43400];
            break;
        case "Colombia":
            return [4.624335, -74.063644];
            break;
        case "Italy":
            return [43.1122, 12.3888];
            break;
        case "Canada":
            return [55.0000, -106.0000];
            break;
        case "Spain":
            return [40.416729, -3.703339];
            break;
        case "Germany":
            return [50.979571, 10.314687];
            break;
        case "Saudi Arabia":
            return [24.65, 46.766667];
            break;
        case "Poland":
            return [52.233333, 21.016667];
            break;
        default:
            return null;
            break;  
    }

}

function caseMarkerSize(value)
{
    return value / 50;
}

function vaccMarkerSize(value)
{
    return value / 200;
}

function createMap(countries)
{
    var casesMarkers = [];
    var vaccinationMarkers = [];
    var casesHeatArray = [];
    var vaccinationsHeatArray = [];

    for (var c = 0; c < countries.length; c++) {
        // Setting the marker 
        casesMarkers.push(
            L.circle(countries[c].coordinates, {
                stroke: false,
                fillOpacity: 0.75,
                color: "red",
                fillColor: "red",
                radius: caseMarkerSize(countries[c].total_cases)
            }).bindPopup("<center>" + countries[c].location + "<hr>Total COVID-19 Cases as of "+
                countries[c].lastDate + ": <b>" + 
                countries[c].total_cases + "</b></center>")
        );

        vaccinationMarkers.push(
            L.circle(countries[c].coordinates, {
                stroke: false,
                fillOpacity: 0.75,
                color: "orange",
                fillColor: "orange",
                radius: vaccMarkerSize(countries[c].total_vaccinations)
            }).bindPopup("<center>" + countries[c].location + "<hr>Total COVID-19 Vaccinations as of "
            + countries[c].lastDate +": <b>" + 
            countries[c].total_vaccinations + "</b></center>")
        );

        for (var i = 0; i < countries[c].total_cases / 10000; i++)
        {
            casesHeatArray.push(
                countries[c].coordinates
            );
        }

        for (var i = 0; i < countries[c].total_vaccinations / 10000; i++)
        {
            vaccinationsHeatArray.push(
                countries[c].coordinates
            );
        }
    }

    // Streetmap Layer
    var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
        tileSize: 512,
        maxZoom: 18,
        zoomOffset: -1,
        id: "mapbox/streets-v11",
        accessToken: API_KEY
    });
  
  var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "dark-v10",
    accessToken: API_KEY
  });
  
  var cases = L.layerGroup(casesMarkers);
  var vaccinations = L.layerGroup(vaccinationMarkers);
  var casesHeat = L.heatLayer(casesHeatArray, {
      radius: 70,
      blur: 35
  });
  var vaccinationsHeat = L.heatLayer(vaccinationsHeatArray, {
    radius: 70,
    blur: 35
    });

  // Create a baseMaps object
    var baseMaps = {
        "Street Map": streetmap,
        "Dark Map": darkmap
    };
  
    var overlayMaps = {
        "Cases": cases,
        "Vaccinations": vaccinations,
        "Covid Cases Heat Map": casesHeat,
        "Vaccination Heat Map": vaccinationsHeat
      };

    // Define a map object
    var myMap = L.map("map", {
        center: [15, 0],
        zoom: 2,
        layers: [streetmap, cases]
    });
  
  // Pass our map layers into our layer control
  // Add the layer control to the map
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(myMap);
}