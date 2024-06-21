<!-- Copyright 2024 Radboud University, Modern Software Development Techniques

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. -->

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
