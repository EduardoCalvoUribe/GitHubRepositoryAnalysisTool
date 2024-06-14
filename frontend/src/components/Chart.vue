<template>
  <div>
    <Bar v-if="isBar"
      :data="chartData"
      :options="chartOptions"
    />
    <Line v-else
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script>
import { Bar, Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js'
import { ref, watchEffect } from 'vue';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement)

export default {
  name: 'Chart',
  components: { Bar, Line },
  props: {
    chartData: {
      type: Object,
      required: true
    },
    chartOptions: {
      type: Object,
      default: () => {}
    },
    isBar: {
      type: Boolean,
      default: true
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