// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
const ctxPieChart = document.getElementById('myPieChart');
const myPieChart = new Chart(ctxPieChart, {
  type: 'pie',
  data: {
    labels: ['Auction 3', 'Auction 8', 'Auction 4', 'Auction 7'],
    datasets: [{
      data: [21.22, 15.58, 11.25, 8.32],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
    }],
  },
});
