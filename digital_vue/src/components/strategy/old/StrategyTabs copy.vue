<template>
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
                        <span>{{ selectedPlan.name }} : Strategies</span>
                    </v-col>
                    <v-col cols="4" class="d-flex justify-end align-center">
                        <!-- <v-chip @click="openNewStrategyDialog" outlined class="secondary mr-2"> -->
                        <v-icon @click="openNewStrategyDialog" class="black--text">mdi-plus</v-icon>
                        <!-- <v-icon class="black--text">mdi-alpha-s-circle-outline</v-icon> -->
                        <!-- </v-chip> -->
                        <v-btn icon @click="toggleStrategyTabs">
                            <v-icon v-if="showStrategyTabs" class="black--text">mdi-eye-outline</v-icon>
                            <v-icon v-else class="black--text">mdi-eye-off-outline</v-icon>
                        </v-btn>
                    </v-col>
                </v-row>
            </v-card-title>
            <v-divider></v-divider>
            <div v-if="showStrategyTabs">
                <v-tabs
                    v-model="tab"
                    class="mt-1 rounded-0 "
                    background-color="grey lighten-4"
                    center-active
                    show-arrows
                    slider-size=6>
                    <v-tabs-slider color="grey"></v-tabs-slider>
                    <v-tab
                        v-for="(strategy, index) in selectedPhase.strategies"
                        :key="strategy.id"
                        :href="'#' + strategy.get_absolute_url"
                        :to="`${strategy.slug}`"
                        @click="onTabClick(strategy, index)"
                        class="secondary text-capitalize black--text font-weight-regular">
                        {{ strategy.name }}
                    </v-tab>
                    <v-spacer></v-spacer>
                </v-tabs>
                <v-tabs-items
                    v-model="tab">
                    <v-tab-item
                        v-for="(strategy, index) in selectedPhase.strategies"
                        :key="strategy.id"
                        :id="strategy.slug">
                        <!-- <router-view v-if="tab === strategy.slug" /> -->
                        <StrategyCard
                            :strategy="strategy"
                            @open-editstrategy-dialog="openEditStrategyDialog(strategy)"
                            @open-country-dialog="openEditCountryDialog(strategy)"
                            @open-countrychannel-dialog="openEditCountryChannelDialog(strategy)" />
                    </v-tab-item>
                </v-tabs-items>
            </div>
        </v-card>
    </v-sheet>
</template>
<script>
import StrategyCard from '@/components/strategy/StrategyCard'

export default {
    name: 'StrategyTabs',
    components: {
        StrategyCard,
    },
    props: {
        showStrategyTabs: Boolean
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
            }
        },
        selectedStrategy: {
            get() {
                return this.$store.state.selectedStrategyData.strategy;
            }
        },
        selectedStrategyIndex: {
            get() {
                return this.$store.state.selectedStrategyData.index
            }
        },
    },
    watch: {
        tab(newTabURL, oldTabURL) {
            // Set the name of the tab name variable to the first tab in the tablist when the tabs are first shown.
            // oldTabURL will be empty as there will be no previous tab
            if (!oldTabURL) {
                var strategyPayload = { strategy: this.selectedPhase.strategies[0], index: 0 }
                this.$store.dispatch('selectStrategyData', strategyPayload)
            }
            else {
                console.log('new tabs urls:', newTabURL)
                console.log('new tabs urls:', oldTabURL)
                // If Phase tab changed then selected the first Strategy
                var newPhase = newTabURL.split("/")[1]
                var oldPhase = oldTabURL.split("/")[1]

                if (newPhase != oldPhase) {
                    this.tab = this.selectedPhase.strategies[0].slug
                }
            }
        },
    },
    methods: {
        openNewStrategyDialog() {
            this.$emit("open-newstrategy-dialog")
        },
        openEditStrategyDialog(strategy) {
            this.$emit("open-editstrategy-dialog", strategy)
        },
        openEditCountryDialog(strategy) {
            this.$emit("open-editcountry-dialog", strategy)
        },
        openEditCountryChannelDialog(strategy) {
            // console.log('StrategyTabs: ', strategy)
            this.$emit("open-editcountrychannel-dialog", strategy)
        },
        onTabClick(strategy, index) {
            // Refresh Stored Phase
            console.log(strategy.get_absolute_url)
            const payload = { strategy: strategy, index: index }
            this.$store.dispatch('selectStrategyData', payload)
        },
        toggleStrategyTabs() {
            this.$store.dispatch('toggleStrategyTabs')
        },
    }

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