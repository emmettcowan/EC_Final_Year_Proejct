
var userData = [];
var formateData = [];

var Today = new Date();
var startTime = 0;
var endTime = Today.getTime();
//set date inputs max to todays date
var dd = Today.getDate() + 1;
var mm = Today.getMonth() + 1; //January is 0!
var yyyy = Today.getFullYear();
if (dd < 10) {
    dd = '0' + dd
}
if (mm < 10) {
    mm = '0' + mm
}
Today = yyyy + '-' + mm + '-' + dd;
document.getElementById("start").setAttribute("max", Today);
document.getElementById("end").setAttribute("max", Today);



//get date from inputs on change event
//start date change
const startInput = document.getElementById('start');

startInput.addEventListener('change', (event) => {
    var selectedDate = event.target.value;
    startTime = new Date(selectedDate).getTime() / 1000;
});

//end date change
const endInput = document.getElementById('end');

endInput.addEventListener('change', (event) => {
    var selectedDate = event.target.value;
    endTime = new Date(selectedDate).getTime() / 1000;
    formateData = [];
    userData.forEach(element => {
        if(element['Start_time'] > startTime && element['End_Time'] < endTime){
            formateData.push(element);
        }
    });
    console.log(formateData);
    Chartdata(formateData);
});



fetch('/userData')
    .then(
        function (response) {
            if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                    response.status);
                return;
            }
            response.json().then(function (data) {
                userData = data;
                formateData = data;
                Chartdata(formateData);
            });
        }
    )
    .catch(function (err) {
        console.log('Fetch Error :-S', err);
    });

/*
*   Code for dynamicly chaning colors is from the following article
*   https://codenebula.io/javascript/frontend/dataviz/2019/04/18/automatically-generate-chart-colors-with-chart-js-d3s-color-scales/
*   uses D3 interpolation
*/
function calculatePoint(i, intervalSize, colorRangeInfo) {
    var { colorStart, colorEnd, useEndAsStart } = colorRangeInfo;
    return (useEndAsStart
        ? (colorEnd - (i * intervalSize))
        : (colorStart + (i * intervalSize)));
}


function interpolateColors(dataLength, colorScale, colorRangeInfo) {
    var { colorStart, colorEnd } = colorRangeInfo;
    var colorRange = colorEnd - colorStart;
    var intervalSize = colorRange / dataLength;
    var i, colorPoint;
    var colorArray = [];

    for (i = 0; i < dataLength; i++) {
        colorPoint = calculatePoint(i, intervalSize, colorRangeInfo);
        colorArray.push(colorScale(colorPoint));
    }

    return colorArray;
}


function Chartdata(data) {
    var headings = [];
    var values = [];
    data.forEach(entry => {
        if (headings.includes(entry.App)) {
        for (let index = 0; index < headings.length; index++) {
            if (headings[index] == entry.App) {
                values[index] = values[index] + entry.Total_time;
            }
        }
    }
    else {
        headings.push(entry.App);
            values.push(entry.Total_time);
    }
    });
    const chartData = {
        labels: headings,
        data: values,
    };
    const dataLength = chartData.data.length;

    const colorScale = d3.interpolateCool;

    const colorRangeInfo = {
        colorStart: 0,
        colorEnd: 0.65,
        useEndAsStart: true,
    };

    /* Create color array */
    var COLORS = interpolateColors(dataLength, colorScale, colorRangeInfo);

    createChart(chartData, COLORS);
}


function createChart( data, colors) {
    myChart = document.getElementById("bar").getContext("2d");
    myChart = new Chart(myChart, {
        type: 'horizontalBar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Time (Seconds)",
                    backgroundColor: colors,
                    data: data.data
                }
            ]
        },
        options: {
            legend: { display: false },
            title: {
                display: true,
                text: 'Time spent on diffrent applications (Seconds)'
            }
        }
    });

    myChart = document.getElementById("pie").getContext("2d");
    myChart = new Chart(myChart, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Time (Seconds)",
                    backgroundColor: colors,
                    data: data.data
                }
            ]
        },
        options: {
            legend: { display: false },
            title: {
                display: true,
                text: 'Time spent on diffrent applications (Seconds)'
            }
        }
    });
}





