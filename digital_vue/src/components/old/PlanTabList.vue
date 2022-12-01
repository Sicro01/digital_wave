<template>
  <div>
    <v-row>
      <v-col
        md="12"
        sm="12">
        <v-card>
          <v-tabs
            dark
            background-color="secondary"
            v-model="tab"
            hide-slider
            center-active>
            <v-tabs-slider></v-tabs-slider>
            <v-tab
              v-for="plan in plans"
              :key="plan.id">
              {{ plan.name }}
            </v-tab>
          </v-tabs>
        </v-card>
        <v-tabs-items v-model="tab">
          <v-tab-item
            v-for="plan in plans"
            :key="plan.id">
            <v-sheet
              class="pb-4 sheet-border"
              outlined>
              <v-card
                class="px-3"
                flat
                tile>
                <v-row>
                  <v-col cols="3">
                    <v-text-field
                      v-model="plan.description"
                      :rules="[rules.required]"
                      class="rounded-0 mt-3"
                      label="Plan Description"
                      outlined
                      type="text"
                      required>
                    </v-text-field>
                  </v-col>
                </v-row>
                <PhaseCard v-for="phase in plan.phases" :key="phase.id" :phase="phase" />
              </v-card>
            </v-sheet>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import PhaseCard from '@/components/PhaseCard'
export default {
  name: 'PlanTabList',
  props: {
    plans: Array,
  },
  components: {
    PhaseCard,
  },
  data() {
    return {
      tab: null,
      rules: {
        required: value => !!value || 'Required.',
      },
    }
  },
}
</script>
<style scoped>
.sheet-border {
  border: 1px solid var(--v-secondary);
}
</style>