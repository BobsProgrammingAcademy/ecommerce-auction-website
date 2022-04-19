// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Bar Chart Example
var ctx = document.getElementById('myBarChart');
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Food', 'Books', 'Clothes', 'Electronics', 'Films', 'Toys', 'Health'],
    datasets: [{
      label: 'Categories',
      backgroundColor: 'rgba(2,117,216,1)',
      borderColor: 'rgba(2,117,216,1)',
      data: [5, 3, 2, 1, 0, 0, 0],
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'month'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 6
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 6,
          maxTicksLimit: 5
        },
        gridLines: {
          display: true
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
