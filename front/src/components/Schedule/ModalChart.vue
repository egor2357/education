<template>
  <a-modal
    :visible="true"
    title="Распределение занятий по видам деятельности за неделю"
    @cancel="$emit('close')"
    :footer="null"
    width="700px"
    :dialog-style="{ top: '40px' }"
  >
    <BarChart ref="chart" :options="chartOptions" :chartData="chartData" />
    <a-divider />
    <div style="text-align: center">
      <span
        >{{ stat["sum"].name }}: <b>{{ stat["sum"].count }}</b></span
      >
    </div>
  </a-modal>
</template>

<script>
import { mapGetters } from "vuex";
import BarChart from "@/components/BarChart";
export default {
  name: "ModalChart",
  components: {
    BarChart,
  },
  data() {
    return {
      chartOptions: {
        responsive: true,
        legend: {
          display: false,
        },
        maintainAspectRatio: false,
        scales: {
          yAxes: [
            { ticks: { beginAtZero: true, min: 0, max: 10, stepSize: 1 } },
          ],
        },
      },
      chartData: {},
    };
  },
  created() {
    this.prepareData();
  },
  methods: {
    prepareData() {
      this.chartData.labels = ["Количество занятий в неделю"];
      this.chartData.datasets = [];
      for (let key in this.stat) {
        if (key !== "sum") {
          this.chartData.datasets.push({
            label: this.stat[key].name,
            backgroundColor: `${this.stat[key].color}99`,
            data: [this.stat[key].count],
          });
        }
      }
      this.chartOptions.scales.yAxes[0].ticks.max = this.stat["sum"].max + 1;
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.$refs.chart.renderChart(this.chartData, this.chartOptions);
    });
  },
  computed: {
    ...mapGetters({
      stat: "schedule/getJobsStat",
    }),
  },
};
</script>

<style scoped></style>
