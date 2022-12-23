<template>
    <div>
        <v-tooltip
            bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    @click="$emit('open-createphase-dialog')"
                    icon
                    class="ml-2"
                    small
                    v-bind="attrs"
                    v-on="on">
                    <v-icon
                        color="primary"
                        small>mdi-plus</v-icon>
                </v-btn>
            </template>
            <span>Create Phase</span>
        </v-tooltip>
        <v-menu
            offset-y>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    class="pa-0 grey--text text-capitalize"
                    text
                    v-bind="attrs"
                    v-on="on">
                    <span>Phases</span>
                </v-btn>
            </template>

            <v-list>
                <v-list-item
                    v-for="(phase, index) in selectedPlan.phases"
                    :key="index"
                    @click="menuActionClick(phase, index)">
                    <v-list-item-title>{{ phase.name }}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
    </div>
</template>
<script>
export default {
    name: 'PhaseMenu',
    data() {
        return {
        }
    },
    computed: {
        selectedPlan: {
            get() {
                return this.$store.state.selectedPlan
            }
        },
    },
    methods: {
        menuActionClick(phase, index) {
            this.$emit('open-phase-card', phase, index)
        },
    }
}
</script>