<template>
  <v-row>
    <v-col
      md="3"
      sm="6">
      <v-select
        v-model="firstPlan"
        :items="plans"
        item-text="name"
        :menu-props="{ bottom: true, offsetY: true }"
        label="Select Plan"
        dense
        outlined
        tile
        color="secondary"></v-select>
    </v-col>
  </v-row>
</template>
<script>
export default {
  name: 'PlanSelectList',
  props: {
    plans: Array,
  },
  computed: {
    firstPlan: {
      get() {
        return this.plans[0].name
      }
    }
  },
}
</script>
<style lang="">
    
</style>