const chartData = window.chartData || {
  states: [],
  stateValues: [],
  areaValues: [],
};

// 1️⃣ STATE-WISE BAR CHART
if (chartData.states.length > 0 && chartData.stateValues.length > 0) {
  const stateCtx = document.getElementById('stateChart').getContext('2d');
  new Chart(stateCtx, {
    type: 'bar',
    data: {
      labels: chartData.states,
      datasets: [{
        label: 'Avg Unemployment (%)',
        data: chartData.stateValues,
        backgroundColor: '#3498db',
        borderRadius: 5
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'State-wise Average Unemployment Rate',
          font: {
            size: 18
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Unemployment Rate (%)'
          }
        }
      }
    }
  });
}

// 2️⃣ AREA-WISE DOUGHNUT CHART
if (chartData.areaValues.length > 0) {
  const areaCtx = document.getElementById('areaChart').getContext('2d');
  new Chart(areaCtx, {
    type: 'doughnut',
    data: {
      labels: ['Urban', 'Rural'],
      datasets: [{
        label: 'Unemployment by Area',
        data: chartData.areaValues,
        backgroundColor: ['#2ecc71', '#e67e22'],
        borderColor: '#fff',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Urban vs Rural Unemployment',
          font: {
            size: 18
          }
        },
        legend: {
          position: 'bottom'
        }
      }
    }
  });
}

// 3️⃣ YEAR-WISE TREND CHART (REAL DATA)
const yearCtx = document.getElementById('yearTrendChart').getContext('2d');
new Chart(yearCtx, {
  type: 'line',
  data: {
    labels: ["2016", "2017", "2018", "2019", "2020", "2021", "2022"],
    datasets: [{
      label: 'National Unemployment Rate (%)',
      data: [5.0, 5.2, 5.8, 6.1, 7.1, 6.3, 5.6],
      borderColor: '#185a9d',
      backgroundColor: 'rgba(24, 90, 157, 0.2)',
      borderWidth: 2,
      tension: 0.3,
      fill: true,
      pointRadius: 5,
      pointBackgroundColor: '#185a9d',
    }]
  },
  options: {
    plugins: {
      title: {
        display: true,
        text: 'Year-wise Unemployment Trend (India)',
        font: {
          size: 18
        }
      },
      tooltip: {
        callbacks: {
          label: context => `${context.parsed.y}%`
        }
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        title: {
          display: true,
          text: 'Unemployment Rate (%)'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Year'
        }
      }
    }
  }
});
