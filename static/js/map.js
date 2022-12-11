// Function to format the date into month/day/year
function formatDate(date) {
    var year = date.getFullYear()
    var month = (1 + date.getMonth()).toString()
    var day = date.getUTCDate()
    return month + "/" + day + "/" + year
}

function loadPopulationChart() {
    Highcharts.getJSON('http://127.0.0.1:5000/data/countrydemo', function (data) {
        console.log('import map')
        console.log(data);

        var map_data = [];

        for (var i = 0; i < data.length; i++) {
            map_data.push({
                code3: data[i].country_id,
                value: data[i].population
            })
        }

        console.log(map_data)

        var popData = data.filter(point => point.population > 0).map(point => point.population);
        var maxPop = Math.max.apply(null, popData);
        var minPop = Math.min.apply(null, popData);


        Highcharts.mapChart('container', {
            chart: {
                borderWidth: 1,
                map: 'custom/world'
            },

            title: {
                text: 'World population by country'
            },

            legend: {
                enabled: false
            },

            mapNavigation: {
                enabled: true,
                buttonOptions: {
                    verticalAlign: 'bottom'
                }
            },
            colorAxis: {
                min: 1000000,
                max: maxPop,
                type: 'logarithmic'
            },


            series: [{
                data: map_data,
                joinBy: ['iso-a3', 'code3'],
                name: 'Population',
                states: {
                    hover: {
                        color: '#a4edba'
                    }
                }
            }]
        })
    })
}

function loadDailyCaseChart() {
    Highcharts.getJSON('http://127.0.0.1:5000/data/coviddata?most_recent=1', function (data) {
        console.log('import map')
        console.log(data);

        var mapData = [];
        var bubbleData = [];

        var date = formatDate(new Date(data[0].date))

        for (var i = 0; i < data.length; i++) {
            mapData.push({
                code3: data[i].country_id,
                value: data[i].total_cases
            })

            bubbleData.push({
                code3: data[i].country_id,
                z: data[i].new_cases
            })
        }

        bubbleData = bubbleData.filter(point => point.z > 0)

        console.log(mapData)


        console.log()
        Highcharts.mapChart('map-container', {
            chart: {
                borderWidth: 1,
                map: 'custom/world',
            },

            title: {
                text: `New Cases by Country for ${date}`
            },

            legend: {
                enabled: false
            },

            mapNavigation: {
                enabled: true,
                buttonOptions: {
                    verticalAlign: 'bottom'
                }
            },


            series: [{
                name: 'Countries',
                color: '#E0E0E0',
                enableMouseTracking: false
            },
                {
                    data: bubbleData,
                    type: 'mapbubble',
                    marker: {
                        fillColor: {
                            radialGradient: {cx: 0.4, cy: 0.3, r: 0.7},
                            stops: [
                                [0, 'rgba(255,255,255,0.5)'],
                                [1, 'rgba(69,114,167,0.5)']
                            ]
                        }
                    },
                    joinBy: ['iso-a3', 'code3'],
                    name: 'New Cases',
                    minSize: 4,
                    maxSize: '40%',
                    point: {
                        events: {
                            click: function() {
                                document.getElementById("selDataset").value = this.code3
                                optionChanged(this.code3)
                            }
                        }
                    }
                }]
        })
    })
}
