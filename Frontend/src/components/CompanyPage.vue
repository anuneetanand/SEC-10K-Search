<template>
  <div class="companyPage">
    <h1>{{ companyName }}</h1>
    <div
      class="graph"
      v-for="(plotData, feature) in this.graphData"
      :key="feature"
    >
      <h4>{{ feature }}</h4>
      <graph-bar
        :width="400"
        :height="200"
        :axis-min="0"
        :labels="plotData[0]"
        :values="plotData[1]"
      >
      </graph-bar>
    </div>
  </div>
</template>
<script>
const axios = require("axios");
import Vue from "vue";
import VueGraph from "vue-graph";
Vue.use(VueGraph);
export default {
  data() {
    return {
      graphData: {},
    };
  },
  props: {
    companyName: String,
  },
  mounted() {
    axios
      .post("http://localhost:3000/get_company_modal_data", {
        companyName: this.$props.companyName,
      })
      .then((data) => {
        this.graphData = data.data;
        console.log(this.graphData, "what dtaaa");
      });
  },
};
</script>

<style scoped>
.companyPage {
  text-align: center;
}

.graph {
  display: inline-block;
}
</style>
