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

 var i = 0;
 var MAX_BARS = 20;

 function update_values() {
    // console.log('test');
    $.getJSON('/api/heartrate/latest',

        function(data) {
            $('#result').text(data.result);
            temp = data.result;
            console.log(data)
        }
    );

    // c++;
    // console.log(c);
    // console.log(temp);
    
    // heartChart.data.datasets.forEach((dataset) => {
    //     console.log(dataset);
    //     dataset.data.push(temp);
    // })

    // console.log(heartChart.data);


    // for (var key in response) {

    // if (data.labels.length > MAX_BARS) {
    //     data.labels.shift();
    //     data.datasets[0].data.shift();
    // }

    data.labels[i] = i;
    data.datasets[0].data[i] = temp;
    i++;
    
    // }

    heartChart.update()
 }

// Chart Data
var data = {
   labels: [],
   datasets: [
        {
            label: [],
            data: [],
        }
    ]
};

var heartrate = document.getElementById('heartrate').getContext('2d');
var heartChart = new Chart(heartrate,{
    type: 'bar',
    data: data,
    // options: {
    //      scales: {
    //         x: {
    //             type: 'linear',
    //             min: 0,
    //             max: MAX_BARS 
    //         }
    //     }
    // },
    animation:{ 
       animateScale:true
    }
 });