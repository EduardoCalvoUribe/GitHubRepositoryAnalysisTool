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

// Register the required components from Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement)

export default {
  name: 'Chart',
  components: { Bar, Line },
  props: {
    /**
     * The data to be displayed in the chart.
     * @type {Object}
     * @required
     */
    chartData: {
      type: Object,
      required: true
    },
    /**
     * The options for configuring the chart.
     * @type {Object}
     * @default {}
     */
    chartOptions: {
      type: Object,
      default: () => { }
    },
    /**
     * Boolean flag to determine if the chart should be a Bar chart.
     * If false, a the chart will be a Line chart.
     * @type {Boolean}
     * @default true
     */
    isBar: {
      type: Boolean,
      default: true
    }
  },
  emits: ['bar-click'],
  setup(props, { emit }) {
    const chartData = ref(props.chartData);
    const chartOptions = ref(props.chartOptions);

    /**
     * Handles click events on the chart.
     * Emits a 'bar-click' event with the label of the clicked bar.
     *
     * @param {Event} event - The click event.
     * @param {Array} elements - The elements that were clicked.
     */
    const onClick = (event, elements) => {
      if (elements.length > 0) {
        const firstElement = elements[0];
        const label = chartData.value.labels[firstElement.index];
        const value = chartData.value.datasets[firstElement.datasetIndex].data[firstElement.index];
        emit('bar-click', { label });
      }
    };

    /**
     * Watches for changes in the chart data and options, and updates them accordingly.
     */
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
