<template>
    <Bar
      :data="chartData"
      :options="chartOptions"
    />
  </template>
  
  <script>
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  export default {
    name: 'BarChart',
    components: { Bar },
    data() {
      return {
        chartData: {
          labels: [ 'January', 'February', 'March', 'April', 'May', 'June', 'July'],
          datasets: [ { data: [0.8, 0.2, 0.3, 0.6, 0.55, 0.23, 0.95] } ],
          type: Object,
          required: true
        },
        chartOptions: {
          type: Object,
          default: () => {}
        }
      }
    }
  }
  </script>