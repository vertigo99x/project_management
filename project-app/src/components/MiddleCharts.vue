<script setup>
import { ref, defineProps, defineEmits, onMounted, watch, nextTick } from 'vue'
import moment from 'moment';


const chartBars = ref(null);
const chartLineTasks = ref(null);
const chartLine = ref(null);



const props = defineProps({
  userData: {
    type: Object,
    required: true,
  },
  chartData: {
    type: Object,
    required: true,
  },
  
  
});


const enableChartBars = () => {
    if (chartBars.value) {
    const ctx = chartBars.value.getContext('2d'); // Get the 2D context of the canvas

    // Initialize the Chart.js bar chart
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        datasets: [{
          label: "Created Projects",
          tension: 0.4,
          borderWidth: 0,
          borderRadius: 4,
          borderSkipped: false,
          backgroundColor: "rgba(255, 255, 255, .8)",
          data: props.chartData ? props.chartData.data.created_count:[] ,
          maxBarThickness: 6
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5],
              color: 'rgba(255, 255, 255, .2)',
            },
            ticks: {
              suggestedMin: 0,
              suggestedMax: 500,
              beginAtZero: true,
              padding: 10,
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2,
              },
              color: "#fff"
            },
          },
          x: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5],
              color: 'rgba(255, 255, 255, .2)',
            },
            ticks: {
              display: true,
              color: '#f8f9fa',
              padding: 10,
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2,
              },
            }
          },
        },
      },
    });
  }
}

const enableChartLine = () => {
  if(chartLine.value){
    const ctx2 = chartLine.value.getContext("2d");

    new Chart(ctx2, {
      type: "line",
      data: {
        labels: [ "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        datasets: [{
          label: "Assigned Projects",
          tension: 0,
          borderWidth: 0,
          pointRadius: 5,
          pointBackgroundColor: "rgba(255, 255, 255, .8)",
          pointBorderColor: "transparent",
          borderColor: "rgba(255, 255, 255, .8)",
          borderColor: "rgba(255, 255, 255, .8)",
          borderWidth: 4,
          backgroundColor: "transparent",
          fill: true,
          data: props.chartData ? props.chartData.data.assigned_count:[] ,
          maxBarThickness: 6

        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5],
              color: 'rgba(255, 255, 255, .2)'
            },
            ticks: {
              display: true,
              color: '#f8f9fa',
              padding: 10,
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              color: '#f8f9fa',
              padding: 10,
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
        },
      },
    });
  }
}

const enableChartLineTasks = () => {
  const ctx3 = chartLineTasks.value.getContext("2d");

    new Chart(ctx3, {
      type: "line",
      data: {
        labels: [ "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        datasets: [{
          label: "Completed Projects",
          tension: 0,
          borderWidth: 0,
          pointRadius: 5,
          pointBackgroundColor: "rgba(255, 255, 255, .8)",
          pointBorderColor: "transparent",
          borderColor: "rgba(255, 255, 255, .8)",
          borderWidth: 4,
          backgroundColor: "transparent",
          fill: true,
          data: props.chartData ? props.chartData.data.completed_count:[] ,
          maxBarThickness: 6

        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: true,
              drawOnChartArea: true,
              drawTicks: false,
              borderDash: [5, 5],
              color: 'rgba(255, 255, 255, .2)'
            },
            ticks: {
              display: true,
              padding: 10,
              color: '#f8f9fa',
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
              borderDash: [5, 5]
            },
            ticks: {
              display: true,
              color: '#f8f9fa',
              padding: 10,
              font: {
                size: 14,
                weight: 300,
                family: "Roboto",
                style: 'normal',
                lineHeight: 2
              },
            }
          },
        },
      },
    });
}




const getTodayPercent = (value) => {
  let percentage;
  const today = new Date().getDay()
  if(today > 0){
    percentage = ((value[today] - value[today - 1]) * 100) / value[today - 1]
  }
  return percentage
}



watch(
  () => props.chartData,
  (newVal) => {
    if (newVal && newVal.data) {
      nextTick(() => {
        if (newVal.data.created_count) {
          enableChartBars();
        }
        if (newVal.data.assigned_count) {
          enableChartLine();
        }
        if (newVal.data.completed_count) {
          enableChartLineTasks();
        }
      });
    }
  },
  { immediate: true }
);

onMounted(() => {
  nextTick(() => {
    if (props.chartData && props.chartData.data) {
      if (props.chartData.data.created_count) {
        enableChartBars();
      }
      if (props.chartData.data.assigned_count) {
        enableChartLine();
      }
      if (props.chartData.data.completed_count) {
        enableChartLineTasks();
      }
    }
  });
});

</script>

<template>
  <div class="col-lg-4 col-md-6 mt-4 mb-4">
    <div class="card z-index-2 ">
      <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2 bg-transparent">
        <div class="bg-gradient-primary shadow-primary border-radius-lg py-3 pe-1">
          <div class="chart">
            <canvas id="chart-bars" ref='chartBars' class="chart-canvas" height="170"></canvas>
          </div>
        </div>
      </div>
      <div class="card-body" v-if="props.chartData">
        <h6 class="mb-0 ">Created Projects</h6>
        <p class="text-sm ">Projects created this week</p>
        <hr class="dark horizontal">
        <div class="d-flex ">
          <i class="material-icons text-sm my-auto me-1">event</i>
          <p class="mb-0 text-sm"> From {{moment(chartData.data.week_start).format("Do MMM, YYYY")}} - {{moment(chartData.data.week_end).format("Do MMM, YYYY")}}</p>
        </div>
      </div>
    </div>
  </div>
  <div class="col-lg-4 col-md-6 mt-4 mb-4">
    <div class="card z-index-2  ">
      <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2 bg-transparent">
        <div class="bg-gradient-success shadow-success border-radius-lg py-3 pe-1">
          <div class="chart">
            <canvas id="chart-line" ref="chartLine"  class="chart-canvas" height="170"></canvas>
          </div>
        </div>
      </div>
      <div class="card-body" v-if="props.chartData">
        <h6 class="mb-0 "> Assigned Projects </h6>
        <p class="text-sm "> (<span class="font-weight-bolder">{{getTodayPercent(props.chartData.data.assigned_count)}}%</span>) increase in assigned Projects </p>
        <hr class="dark horizontal">
    
      </div>
    </div>
  </div>
  <div class="col-lg-4 mt-4 mb-3">
    <div class="card z-index-2 ">
      <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2 bg-transparent">
        <div class="bg-gradient-dark shadow-dark border-radius-lg py-3 pe-1">
          <div class="chart">
            <canvas id="chart-line-tasks" ref="chartLineTasks" class="chart-canvas" height="170"></canvas>
          </div>
        </div>
      </div>
      <div class="card-body" v-if="props.chartData">
        <h6 class="mb-0 ">Completed Projects</h6>
        <p class="text-sm ">Completed Projects by Users</p>
        <hr class="dark horizontal">
       
      </div>
    </div>
  </div>
  
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
