<template>
  <Line
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'
import { ref, watchEffect } from 'vue';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement)

export default {
  name: 'Chart',
  components: { Line },
  props: {
    chartData: {
      type: Object,
      required: true
    },
    chartOptions: {
      type: Object,
      default: () => {}
    }
  },
  setup(props) {
    const chartData = ref(props.chartData);
    const chartOptions = ref(props.chartOptions);

    watchEffect(() => {
      chartData.value = props.chartData;
      chartOptions.value = props.chartOptions;
    });

    return {
      chartData,
      chartOptions
    };
  }
}
</script>