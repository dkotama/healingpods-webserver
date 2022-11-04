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
    $.getJSON('/api/heartrate/_rand',

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

const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
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