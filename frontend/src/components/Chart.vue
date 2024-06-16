<template>
  <div>
    <Bar v-if="isBar" :data="chartData" :options="chartOptions" />
    <Line v-else :data="chartData" :options="chartOptions" />
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
      default: () => { }
    },
    isBar: {
      type: Boolean,
      default: true
    }
  },
  emits: ['bar-click'],
  setup(props, { emit }) {
    const chartData = ref(props.chartData);
    const chartOptions = ref(props.chartOptions);

    const onClick = (event, elements) => {
      if (elements.length > 0) {
        const firstElement = elements[0];
        const label = chartData.value.labels[firstElement.index];
        const value = chartData.value.datasets[firstElement.datasetIndex].data[firstElement.index];
        emit('bar-click', { label })
      }
    };

    watchEffect(() => {
      chartData.value = props.chartData;
      chartOptions.value = {
        ...props.chartOptions,
        onClick,
      };
    });

    return {
      chartData,
      chartOptions
    };
  }
}
</script>
