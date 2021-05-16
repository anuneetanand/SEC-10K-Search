<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <h2>SEC 10K Documents Power Search</h2>
    </v-app-bar>

    <v-main class="main">
      <v-flex
        style="text-align: center; width: 80vw;  margin-top: 5vh; margin-left: 10vw"
        class="d-flex align-center flex-row justify-center align-content-center"
      >
        <v-combobox
          :items="items"
          label="Enter Query or Company Name"
          :search-input.sync="searchInput"
          style="margin-right: 10px;"
        ></v-combobox>
        <v-btn depressed color="primary" @click="getCompany">
          Search
        </v-btn>
      </v-flex>
      <p
        style="text-align: center; width: 80vw;  margin-top: 5vh; margin-left: 10vw"
        v-if="this.loading"
      >
        Loading...
      </p>
      <v-flex class="align-center searchResults">
        <v-col cols="6">
          <div class="results">
            <div v-for="document in searchResults" :key="document.doc_id">
              <CompanyCard :document="document" @selected="showDocumentInfo" />
            </div>
          </div>
        </v-col>
        <DocumentInfoCard
          :document="document"
          @show-company-page="showCompanyPage"
          @show-info-table="showInfoTable"
        />
        <modal
          name="CompanyPage"
          :scrollable="true"
          :height="`auto`"
          :width="`100%`"
        >
          <button class="closeButton" @click="$modal.hide(`CompanyPage`)">
            <v-icon>mdi-close</v-icon>
          </button>
          <CompanyPage
            :companyName="companyPageName"
            @close="$modal.hide(`CompanyPage`)"
          />
        </modal>
        <modal
          :name="`InfoTable`"
          :scrollable="true"
          :height="`auto`"
          :width="`100%`"
        >
          <button class="closeButton" @click="$modal.hide(`InfoTable`)">
            <v-icon>mdi-close</v-icon>
          </button>
          <h1>{{ infoTableName }}</h1>
          <InfoTable :table="infoTable" />
        </modal>
      </v-flex>
    </v-main>
  </v-app>
</template>

<script>
const axios = require("axios");

import Vue from "vue";
import VueRouter from "vue-router";
import vmodal from "vue-js-modal";
Vue.use(vmodal);
import CompanyCard from "./components/CompanyCard";
import DocumentInfoCard from "./components/DocumentInfoCard.vue";
import CompanyPage from "./components/CompanyPage.vue";
import "vue-js-modal/dist/styles.css";
import AsyncComputed from "vue-async-computed";
import InfoTable from "./components/InfoTable.vue";

Vue.use(AsyncComputed);
Vue.use(VueRouter);

export default {
  data() {
    return {
      items: [],
      searchInput: "",
      searchResults: [],
      document: null,
      loading: false,
      companyPageName: undefined,
      infoTable: undefined,
      infoTableName: undefined,
    };
  },
  created() {
    axios
      .get("http://localhost:3000/get_companies")
      .then((response) => (this.items = response.data.companies));
  },
  methods: {
    getCompany() {
      this.loading = true;
      this.searchResults = [];
      const request = {
        query: this.searchInput,
        number_of_records: null,
        page_no: null,
      };
      axios
        .post("http://localhost:3000/retrieve_documents_from_query", request)
        .then((response) => {
          this.searchResults = response.data.documents;
          this.loading = false;
        });
    },
    showDocumentInfo(document) {
      this.document = document;
    },
    showCompanyPage(companyName) {
      this.companyPageName = companyName;
      this.$modal.show("CompanyPage");
    },
    showInfoTable(tableName, table) {
      this.infoTableName = tableName;
      this.infoTable = table;
      this.$modal.show("InfoTable");
    },
  },
  name: "App",

  components: {
    CompanyCard,
    DocumentInfoCard,
    CompanyPage,
    InfoTable,
  },
};
</script>

<style scoped>
.main {
  /* background-color: aliceblue; */
}
.searchResults {
  overflow: scroll;
  height: 75vh;
  position: relative;
}
.closeButton {
  top: 0;
  right: 0;
  position: absolute;
  padding: 1vh;
}
</style>
