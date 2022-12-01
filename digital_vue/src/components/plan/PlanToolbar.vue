<template>
    <!-- <v-row align="center" class="mt-3 mb-3 pa-0"> -->
    <v-sheet outlined class="mt-2 primary elevation-2">
        <v-toolbar
            flat
            dense
            class="text-h3 ">
            <v-col cols="4">

            </v-col>
            <v-col cols="4" class="d-flex justify-center">
                <v-toolbar-title>
                    <span class="font-weight-bold">Plan: </span><span>{{ selectedPlan.name }}&nbsp &nbsp &nbsp</span>
                    <span class="font-weight-bold">Selected Phase: </span><span>{{ phaseName }}</span>
                </v-toolbar-title>
            </v-col>
            <v-col cols="4" class="pr-0 d-flex justify-end">
                <v-menu
                    left
                    offset-y>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            icon
                            v-bind="attrs"
                            v-on="on">
                            <v-icon class="black--text">mdi-dots-vertical</v-icon>
                        </v-btn>
                    </template>
                    <v-list>
                        <v-list-item
                            v-for="(menuItem, i) in menuItems"
                            :key="i"
                            @click="menuActionClick(i)">
                            <v-btn text class="text-capitalize">{{ menuItem.text }}</v-btn>
                        </v-list-item>
                    </v-list>
                </v-menu>
            </v-col>
        </v-toolbar>
    </v-sheet>
    <!-- </v-row> -->
</template>
<script>
export default {
    name: 'PlanToolbar',
    props: {
        phaseName: '',
    },
    data() {
        return {
            menuItems: [
                { text: "Add Phase", click() { this.$emit("open-newphase-dialog") } },
                { text: "Hide/Show Calendar", click() { this.$emit("showPlanCalendar") } },
                { text: "Hide/Show Phases", click() { this.$emit("showPhaseTabs") } },
            ],
        }
    },
    computed: {
        selectedPlan() {
            return this.$store.state.selectedPlan
        },
    },
    methods: {
        menuActionClick(index) {
            this.menuItems[index].click.call(this)
        }
    }
}
</script>