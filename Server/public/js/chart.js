
var userData = [];
var Today = new Date();
var startTime = 0;
var endTime = Today.getTime();
var formateData = [];


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
    BarChart(formateData);
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
                //console.log(formateData);
                BarChart(formateData);
            });
        }
    )
    .catch(function (err) {
        console.log('Fetch Error :-S', err);
    });


function BarChart(data) {
    var headings = [];
    var chartData = [];
    data.forEach(entry => {
        headings.push(entry.App);
        chartData.push(entry.Total_time);
    });
    console.log(data);
    new Chart(document.getElementById("myChart"), {
        type: 'horizontalBar',
        data: {
            labels: headings,
            datasets: [
                {
                    label: "Population (millions)",
                    backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"],
                    data: chartData
                }
            ]
        },
        options: {
            legend: { display: false },
            title: {
                display: true,
                text: 'Predicted world population (millions) in 2050'
            }
        }
    });
}






