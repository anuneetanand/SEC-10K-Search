<template>
  <table>
    <tr v-for="(row, row_no) in table" :key="row_no">
      <td class="tableCell" v-for="(element, col_no) in row" :key="col_no">
        {{ element }}
      </td>
    </tr>
  </table>
</template>

<script>
export default {
  props: {
    table: Array,
  },
};
</script>

<style scoped>
.tableCell {
  border: solid;
}
</style>
