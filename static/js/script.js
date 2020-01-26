console.log("Hello from app.js!");

function drawgraph(id, values) {
  var pieData = {
    labels: ['Democrats', 'Republicans', 'Independents'],
    datasets : [{
        data: values,
        backgroundColor: [
            'blue',
            'red',
            'gray',
        ]
    }]
  }
  var mychart = document.getElementById(id).getContext("2d");
  var myBarChart = new Chart(mychart, {
    type: 'pie',
    data: pieData
   });
}
