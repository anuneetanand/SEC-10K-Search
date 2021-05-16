<template>
  <v-card
    class="mx-auto"
    outlined
    @click="$emit(`selected`, document)"
    style="width: 500px; margin: 10px;"
  >
    <v-list-item three-line>
      <v-list-item-content>
        <div class="overline mb-4">
          Document: {{ document.doc_id }}, Score:
          {{ Math.round(document.score * 10000) / 10 }}, Date of Publish:
          {{ document.date_filled }}
        </div>
        <v-list-item-title class="headline mb-1">
          {{ document.company }}
        </v-list-item-title>
        <span>
          {{
            document.sentences
              .slice(0, 3)
              .join("...")
          }}
          ...
        </span>
      </v-list-item-content>
    </v-list-item>
  </v-card>
</template>
<script>
export default {
  data() {
    return {};
  },
  props: {
    document: Object,
  },
};
</script>
