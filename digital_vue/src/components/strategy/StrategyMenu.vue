<template>
    <div>
        <v-tooltip
            bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    @click="$emit('open-createstrategy-dialog')"
                    icon
                    small
                    v-bind="attrs"
                    v-on="on">
                    <v-icon
                        color="primary"
                        small>mdi-plus</v-icon>
                </v-btn>
            </template>
            <span>Create Strategy</span>
        </v-tooltip>
        <v-menu
            offset-y>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    class="pa-0 grey--text text-capitalize"
                    text
                    v-bind="attrs"
                    v-on="on">
                    <span>Strategies</span>
                </v-btn>
            </template>

            <v-list>
                <v-list-item
                    v-for="(strategy, index) in selectedPhase.strategies"
                    :key="index"
                    @click="menuActionClick(strategy, index)">
                    <v-list-item-title>{{ strategy.name }}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
    </div>
</template>
<script>
export default {
    name: 'StrategyMenu',
    data() {
        return {
        }
    },
    computed: {
        selectedPhase: {
            get() {
                return this.$store.state.selectedPhaseData.phase
            }
        },
        selectedStrategy: {
            get() {
                return this.$store.state.selectedStrategyData.strategy
            }
        },
    },
    methods: {
        menuActionClick(strategy, index) {
            this.$emit('open-strategy-card', strategy, index)
        },
    }
}
</script>