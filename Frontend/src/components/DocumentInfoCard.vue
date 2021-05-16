<template>
  <v-col cols="6" class="" v-if="document">
    <v-card class="mx-auto documentInfoCard" outlined
      ><div class="title">
        <button @click="$emit(`show-company-page`, document.company)">
          <h3>{{ document.company }}</h3>
        </button>
        <br />
        <a :href="document.link"> Complete Document </a>
      </div>

      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>
            {{ "Item 1" }}
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            {{ items["item 1"] }}
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            {{ "Item 7" }}
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            {{ items["item 7"] }}
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            {{ "Financial Summary" }}
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            {{ items["Financial Summary"] }}
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            {{ "Tables" }}
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-expansion-panels>
              <v-expansion-panel
                v-for="(table, table_name) in tables"
                :key="table_name"
              >
                <v-expansion-panel-header>
                  {{ table_name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <button
                    class="expandButton"
                    @click="$emit(`show-info-table`, table_name, table)"
                  >
                    <v-icon>mdi-arrow-expand</v-icon>
                  </button>
                  <div class="table">
                    <InfoTable class="table" :table="table" />
                  </div>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-expansion-panel-content>
        </v-expansion-panel> </v-expansion-panels
    ></v-card>
  </v-col>
</template>

<script>
import InfoTable from "./InfoTable.vue";
const axios = require("axios");

export default {
  components: { InfoTable },
  props: {
    document: Object,
  },
  asyncComputed: {
    async tables() {
      if (this.$props.document == null) return [];
      console.log("computing");
      let tables = (
        await axios.post("http://localhost:3000/get_tables_of_doc", {
          doc_id: this.$props.document.doc_id,
        })
      ).data.tables;
      console.log("computed");
      return tables;
    },
    async items() {
      if (this.$props.document == null)
        return { "item 1": "", "item 7": "", "Financial Summary": "" };
      console.log(this.$props.document.doc_id);
      return {
        "item 1": (
          await axios.post("http://localhost:3000/get_summary", {
            doc_id: this.$props.document.doc_id,
            item_no: 1,
          })
        ).data.summary,
        "item 7": (
          await axios.post("http://localhost:3000/get_summary", {
            doc_id: this.$props.document.doc_id,
            item_no: 7,
          })
        ).data.summary,
        "Financial Summary": (
          await axios.post("http://localhost:3000/get_financial_summary", {
            company: this.$props.document.company,
            date: this.$props.document.date_filled,
          })
        ).data.financialSummary,
      };
    },
  },
};
</script>

<style>
.documentInfoCard {
  position: fixed;
  top: 25vh;
  right: 2vw;
  width: 45vw;
  max-height: 70vh;
  /* height: 70vh; */
  overflow-y: scroll;
  padding: 1vh;
}

.title {
  text-align: center;
}

.table {
  height: 30vh;
  overflow: scroll;
}

.expandButton {
  float: right;
}
</style>
