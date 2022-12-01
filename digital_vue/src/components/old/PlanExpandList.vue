<template>
  <v-row>
    <v-col
      md="3"
      sm="6">
      <v-expansion-panels inset>
        <v-expansion-panel
          v-for="(plan,i) in plans"
          :key="i"
          flat
          tile>
          <v-expansion-panel-header>{{ plan.name }}</v-expansion-panel-header>
          <v-expansion-panel-content>
            {{ plan.description}}
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-col>
  </v-row>
</template>
<script>
export default {
  name: 'PlanExpandList',
  props: {
    plans: Array,
  },
  // computed: {
  //   firstPlan: {
  //     get() {
  //       return this.plans[0].name
  //     }
  //   }
  // },
}
</script>
<style lang="">
    
</style>