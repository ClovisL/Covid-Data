// var url = '././data/countrylist'
var url = 'https://covid-data-site.herokuapp.com/data/countrylist'
fetch(url)
    .then(response => response.json())
    .then(data => console.log(data))

const param = {start_date: "2021-01-01", end_date: "2021-01-31", id: "MEX"}

var url2 = `https://covid-data-site.herokuapp.com/data/coviddata?id=${param.id}&start_date=${param.start_date}&end_date=${param.end_date}`

fetch(url2)
    .then(response => response.json())
    .then(data => console.log(data))

var url3 = `https://covid-data-site.herokuapp.com/data/countrydemo?id=${param.id}`

fetch(url3)
    .then(response => response.json())
    .then(data => console.log(data))