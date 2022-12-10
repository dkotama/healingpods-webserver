/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 *
 */

 "use strict";

 var interval =setInterval(update_values, 1000);
 var c = 0;
 var temp ;

 var riceData = {
    type: 'line',
    data: {
        labels: [c],
        datasets: [{
            label: 'Heart rate',
            data: [temp],
            backgroundColor: [
                'rgba(102, 255, 153, 1)',
            ],
            borderColor: [
                'rgba(255, 0, 0, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
      responsive: true,
      scales: {
        yAxes: [{
            ticks: {
                beginAtZero: true
            }
        }]
      }
    },
 };


 function update_values() {
    $.getJSON('/api/heartrate/latest',

        function(data) {
            $('#result').text(data.result);
            temp = data.result;
            console.log(data)
        }
    );

    c++;
    console.log(c);
    console.log(temp);
    
    heartChart.data.datasets.forEach((dataset) => {
        dataset.data.push(temp);
    })

    heartChart.update()
 }

var heartrate = document.getElementById('heartrate').getContext('2d');
var heartChart = new Chart(heartrate, {
    type: 'line',
    data: {
        labels: [c],
        datasets: [{
            label: 'Heart rate',
            data: [temp],
            backgroundColor: [
                'rgba(102, 255, 153, 1)',
            ],
            borderColor: [
                'rgba(255, 0, 0, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
      scales: {
        y: {
            beginAtZero: true
        }
      }
    }
 });