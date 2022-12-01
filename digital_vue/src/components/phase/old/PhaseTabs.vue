<template>
    <div>
        <v-sheet
            class="mb-3 secondary elevation-0"
            outlined>
            <v-card
                class=""
                flat
                tile>
                <v-card-title class="py-1 justify-center grey lighten-1">
                    <v-row dense class="mt-1 align-center">
                        <v-col cols="4" class="">
                        </v-col>
                        <v-col cols="4" class="d-flex justify-center">
                            <span>{{ selectedPlan.name }} : Phases</span>
                        </v-col>
                        <v-col cols="4" class="d-flex justify-end align-center">
                            <!-- <v-chip @click="openNewPhaseDialog" outlined class="secondary mr-2"> -->
                            <v-icon @click="openNewPhaseDialog" class="black--text">mdi-plus</v-icon>
                            <!-- <v-icon class="black--text">mdi-alpha-p-circle-outline</v-icon> -->
                            <!-- </v-chip> -->
                            <v-btn icon @click="togglePhaseTabs">
                                <v-icon v-if="showPhaseTabs" class="black--text">mdi-eye-outline</v-icon>
                                <v-icon v-else class="black--text">mdi-eye-off-outline</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card-title>
                <v-divider></v-divider>
                <div v-if="showPhaseTabs">
                    <v-tabs
                        ref="tabs"
                        v-model="tab"
                        class="mt-1 rounded-0 "
                        background-color="grey lighten-4"
                        center-active
                        show-arrows
                        slider-size=6>
                        <v-tabs-slider color="grey"></v-tabs-slider>
                        <v-tab
                            v-for="(phase, index) in selectedPlan.phases"
                            :key="phase.id"
                            :href="'#' + phase.slug"
                            :to="`${phase.get_absolute_url}`"
                            @click="onTabClick(phase, index)"
                            class="secondary text-capitalize black--text font-weight-regular">
                            {{ phase.name }}
                        </v-tab>
                        <v-spacer></v-spacer>
                    </v-tabs>
                    <v-tabs-items
                        v-model="tab">
                        <v-tab-item
                            v-for="(phase, index) in selectedPlan.phases"
                            :key="phase.id"
                            :id="phase.get_absolute_url">
                            <router-view v-if="tab === phase.slug" />
                            <PhaseCard
                                :phase="phase"
                                @open-editphase-dialog="openEditPhaseDialog(phase)" />
                        </v-tab-item>
                    </v-tabs-items>
                </div>
            </v-card>
        </v-sheet>

    </div>
</template>
<script>
import PhaseCard from '@/components/phase/PhaseCard'

export default {
    name: 'PhaseTabs',
    components: {
        PhaseCard,
    },
    props: {
        showPhaseTabs: Boolean
    },
    data() {
        return {
            tab: '',
        }
    },
    computed: {
        selectedPlan: {
            get() {
                return this.$store.state.selectedPlan;
            }
        },
        selectedPhase: {
            get() {
                return this.$store.state.selectedPhaseData.phase;
            },
        },
        selectedPhaseIndex: {
            get() {
                return this.$store.state.selectedPhaseData.index
            },
        },
    },
    watch: {
        tab(newTabURL, oldTabURL) {
            // Set the name of the tab name variable to the first tab in the tablist when the tabs are first shown.
            // oldTabURL will be empty as there will be no previous tab
            if (!oldTabURL) {
                const phaseDataPayload = { phase: this.selectedPlan.phases[0], index: 0 }
                this.$store.dispatch('selectPhaseData', phaseDataPayload)
            }
        },
    },
    methods: {
        changeTab() {
            console.log('tab change event:')
        },
        openNewPhaseDialog() {
            this.$emit("open-newphase-dialog")
        },
        openEditPhaseDialog(phase) {
            this.$emit("open-editphase-dialog", phase)
        },
        onTabClick(phase, index) {

            // Refresh Stored Phase
            const phasePayload = { phase: phase, index: index }
            this.$store.dispatch('selectPhaseData', phasePayload)

            // Refresh Stored Phase
            const strategyPayload = { strategy: this.selectedPhase.strategies[0], index: 0 }
            this.$store.dispatch('selectStrategyData', strategyPayload)
            console.log(this.$store.state.selectedStrategyData.strategy.get_absolute_url)
        },
        togglePhaseTabs() {
            this.$store.dispatch('togglePhaseTabs')
        },
    },
}
</script>
<style scoped lang='scss'>
.v-tab--active {
    color: white !important;
    font-weight: bolder;
}

.v-tab {
    text-transform: none !important;
}
</style>