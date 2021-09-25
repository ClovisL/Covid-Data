// COUNTRY NAMES AND ID SECTION

// URL to get dictionary of country codes and country codes
function init() {
    var urlCountry = 'https://covid-data-site.herokuapp.com/data/countrylist';
// JSON fetch. File is each country and their corresponding code
    fetch(urlCountry)
        .then(response => response.json())
        .then(data => {
            // // Variables
            countryNames = data.map(obj => obj.country)
            countryId = data.map(obj => obj.country_id)
            // Displays the currect selection in the dropdownlist
            d3.select("#selDataset")
                .selectAll("options")
                .data(data)
                .enter()
                .append('option')
                // text showed in the menu
                .text(function (d) {
                    return d.country;
                })
                // corresponding value returned by the button
                .attr("value", function (d) {
                    return d.country_id;
                })

            // Default metadata for the first option on the list
            var defaultId = document.getElementById("selDataset").value;
            var defaultName = countryNames[countryId.indexOf(defaultId)];
            // Enter data into text box
            let ele = document.getElementById("sample-metadata");
            ele.innerHTML += defaultName + "<br />";
            ele.innerHTML += defaultId + "<br />";

            loadDailyCaseChart();

            optionChanged(countryId[0])

        })
}

// COVID DATA SECTION

function getCovidData(countryId) {
// URL to get daily covid data for each country
    var urlData = `https://covid-data-site.herokuapp.com/data/coviddata?most_recent=1&id=${countryId}`
// JSON fetch. File is of every countries data per day
    fetch(urlData)
        .then(response => response.json())
        .then(data => {
            // Variables
            countryIdDaily = data.map(obj => obj.country_id)
            date = data.map(obj => obj.date)
            totalCases = data.map(obj => obj.total_cases)
            totalDeaths = data.map(obj => obj.total_deaths)
            totalVaccinations = data.map(obj => obj.people_vaccinated)
            // Get last index of default ID
            var defaultId = document.getElementById("selDataset").value;
            index = countryIdDaily.lastIndexOf(defaultId)
            // Default metadata for current day for the default option on the list
            var defaultCurrentDate = formatDate(new Date(date[index]))
            var defaultCurrentCases = totalCases[index]
            var defaultCurrentDeaths = totalDeaths[index]
            var defaultCurrentVaccinations = totalVaccinations[index]
            // Turn any null values to the last recorded number
            if (defaultCurrentCases == null) {
                defaultCurrentCases = totalCases[index-1]
            }
            if (defaultCurrentDeaths == null) {
                defaultCurrentDeaths = totalDeaths[index-1]
            }
            if (defaultCurrentVaccinations == null) {
                defaultCurrentVaccinations = totalVaccinations[index-1]
            }
            // Enter data into text box
            let ele = document.getElementById("sample-metadata");
            ele.innerHTML += "Date: " + defaultCurrentDate + "<br />";
            ele.innerHTML += "Covid Cases: " + defaultCurrentCases + "<br />";
            ele.innerHTML += "Total Deaths: " + defaultCurrentDeaths + "<br />";
            ele.innerHTML += "People Vaccinated: " + defaultCurrentVaccinations + "<br />";

            // COUNTRY POPULATION SECTION

            // URL to get current population for each country
            var urlPopulation = `https://covid-data-site.herokuapp.com/data/countrydemo?id=${countryId}`
            // JSON fetch. File is of every countries data per day
            fetch(urlPopulation)
                .then(response => response.json())
                .then(data => {
                    // Variables
                    countryPopulation = data.map(obj => obj.population)
                    countryId = data.map(obj => obj.country_id)
                    // Default metadata for the first option on the list
                    var defaultId = document.getElementById("selDataset").value;
                    var defaultPopulation = countryPopulation[countryId.indexOf(defaultId)];
                    // Enter data into text box
                    let ele = document.getElementById("sample-metadata");
                    ele.innerHTML += "Population: " + defaultPopulation + "<br />";

                    // Gauge
                    var gaugeData = [{
                        domain: {x: [0, 1], y: [0, 1]},
                        value: defaultCurrentVaccinations,
                        title: "<b>Population Vaccinated:<br />" +
                            Number(defaultCurrentVaccinations / defaultPopulation * 100).toFixed(2) + "%</b>",
                        type: "indicator",
                        mode: "gauge",
                        gauge: {
                            axis: {range: [null, defaultPopulation], tickmode: "array"}
                        }
                    }];

                    var layout3 = {width: 300, height: 250, margin: {t: 75, b: 10, r: 40, l: 0}};
                    Plotly.newPlot('gauge', gaugeData, layout3);

                })
        })
}

function getCovidTimeGraphs(countryId) {
    var url = `https://covid-data-site.herokuapp.com/data/coviddata?id=${countryId}`
    console.log(url);

    fetch(url)
        .then(response => response.json())
        .then(data => {

            console.log("time series")
            console.log(data);
            var datesX = data.map(obj => formatDate(new Date(obj.date)));
            var totalCasesY = data.map(obj => obj.total_cases);
            var totalDeathsY = data.map(obj => obj.total_deaths);

            var y1_max = Math.max(totalCasesY);
            var y2_max = Math.max(totalDeathsY);

            var dataCases = {
                x: datesX,
                y: totalCasesY,
                name: "Covid Cases",
                type: 'scatter'
            };

            var dataDeath = {
                x: datesX,
                y: totalDeathsY,
                yaxis: 'y2',
                name: "Covid Deaths",
                type: 'scatter'
            }

            trace = [dataCases, dataDeath]

            var layout = {
                title: "Total Covid Cases and Deaths",
                yaxis: {
                    title: "Covid Cases",
                    side: 'left',
                    range: [0, y1_max]
                },
                yaxis2: {
                    title: {
                        text: "Covid Deaths",
                        standoff: 60
                    },
                    overlaying: "y",
                    range: [0, y2_max],
                    side: "right"
                },
                xaxis: {
                    tickmode: "linear",
                    tick0: '2020-01-01',
                    dtick: 90
                },
                margin: {
                    l: 100,
                    r: 20,
                    top: 0,
                    bottom: 0
                },
                height: 600,
                width: 900,
                showlegend: true,
                legend: {xanchor: 'center', x: 0.5, orientation: 'h'}
            }

            Plotly.newPlot('caseGraph', trace, layout);
        })
}

function getVariantData(countryId) {
    var url = `https://covid-data-site.herokuapp.com/data/variantdata?most_recent=1&id=${countryId}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
                console.log(data);

                data = data.filter(obj => obj.variant != "non_who");

                var variantData = data.map(({variant, num_sequences, perc_sequences}) => ({
                    'Variant': variant,
                    'Sequenced Samples Count': num_sequences,
                    'Sequenced Samples Percentage': perc_sequences
                }));

                var subHeader = d3.select("#variant").select('h4');

                subHeader.text("")
                console.log(variantData)
                if (data.length == 0) {
                    subHeader.text("No variant statistics available for country")
                } else {
                    var date = formatDate(new Date(data.map(obj => obj.date)[0]))
                    subHeader.text(`Variant Data Observation Date ${date}`)
                        .style("margin-left", "10px")
                }


                var sortAscending = true;
                d3.select("#variant-table").selectAll("table").remove()
                var table = d3.select('#variant-table').append('table').attr("id", "variant-table");
                var titles = d3.keys(variantData[0]);
                var headers = table.append('thead').append('tr')
                    .selectAll('th')
                    .data(titles).enter()
                    .append('th')
                    .text(function (d) {
                        return d;
                    })
                    .on('click', function (d) {
                        headers.attr('class', 'header');

                        if (sortAscending) {
                            rows.sort(function (a, b) {
                                return b[d] < a[d];
                            });
                            sortAscending = false;
                            this.className = 'aes';
                        } else {
                            rows.sort(function (a, b) {
                                return b[d] > a[d];
                            });
                            sortAscending = true;
                            this.className = 'des';
                        }

                    });

                var rows = table.append('tbody').selectAll('tr')
                    .data(variantData).enter()
                    .append('tr');
                rows.selectAll('td')
                    .data(function (d) {
                        return titles.map(function (k) {
                            return {'value': d[k], 'name': k};
                        });
                    }).enter()
                    .append('td')
                    .attr('data-th', function (d) {
                        return d.name;
                    })
                    .text(function (d) {
                        return d.value;
                    });

                var data = [{
                    values: data.filter(obj => obj.num_sequences > 0).map(obj => obj.num_sequences),
                    labels: data.filter(obj => obj.num_sequences > 0).map(obj => obj.variant),
                    type: "pie"
                }];

                var layout = {
                    height: 600,
                    width: 600
                }

                Plotly.newPlot("variant-pie", data, layout)

            }
        )
}

// COUNTRY SELECTION CHANGED SECTION

// Function to run whenever an option is changed
function optionChanged(value) {
    // Delete text in box to create new text
    document.getElementById("sample-metadata").innerHTML = "";
    // Get values of data
    getCovidData(value)
    getCovidTimeGraphs(value)
    getVariantData(value)
}

// Function to format the date into month/day/year
function formatDate(date) {
    var year = date.getFullYear()
    var month = (1 + date.getMonth()).toString()
    var day = date.getUTCDate()
    return month + "/" + day + "/" + year
}

init()
