<template>
    <v-card
        class="px-3"
        flat
        tile
        outlined>
        <v-card-title>
            <v-row class="">
                <v-col md="4" sm="12" class="mt-3 px-2">
                    <v-text-field
                        v-model="strategy.name"
                        class="rounded-0"
                        label="Name"
                        hide-details
                        readonly
                        dense
                        outlined>
                    </v-text-field>
                </v-col>
                <v-col md="2" sm="12" class="mt-3 px-2">
                    <v-text-field
                        v-model="strategy.start_date"
                        class="rounded-0"
                        label="Start Date"
                        hide-details
                        readonly
                        dense
                        outlined>
                    </v-text-field>
                </v-col>
                <v-col md="2" sm="12" class="mt-3 px-2">
                    <v-text-field
                        v-model="strategy.end_date"
                        class="rounded-0"
                        label="End Date"
                        hide-details
                        readonly
                        dense
                        outlined>
                    </v-text-field>
                </v-col>
            </v-row>
        </v-card-title>
        <v-card-text class="py-1">
            <v-row>
                <v-col md="12" sm="12" class="px-2 ">
                    <v-text-field
                        v-model="strategy.description"
                        class="rounded-0"
                        label="Description"
                        hide-details
                        readonly
                        dense
                        outlined>
                    </v-text-field>
                </v-col>
            </v-row>
        </v-card-text>
        <v-card-actions class="pb-2 justify-start">
            <v-btn
                class="mr-1 secondary darken-3 rounded-0 text-capitalize"
                dark
                @click="openCountryDialog()"
                depressed>
                <v-icon small class="mr-2 ">mdi-flag-plus</v-icon>
                <span>Link Countries</span>
            </v-btn>
            <v-btn
                class="mr-1 secondary darken-3 rounded-0 text-capitalize"
                dark
                @click="openCountryChannelDialog()"
                depressed>
                <v-icon small class="mr-2 ">mdi-instagram</v-icon>
                <span>Link Channels</span>
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
                class="mr-1 secondary darken-3 rounded-0 text-capitalize"
                dark
                @click="openEditStrategyDialog()"
                depressed>
                <v-icon small class="mr-2 ">mdi-pencil</v-icon>
                <span>Edit Strategy</span>
            </v-btn>
        </v-card-actions>
    </v-card>


</template>
<script>
export default {
    name: 'StrategyCard',
    props: {
        strategy: Object,
    },
    data() {
        return {
            valid: false,
            strategy_name: '',
        }
    },
    methods: {
        openEditStrategyDialog(strategy) {
            this.$emit("open-editstrategy-dialog", strategy);
        },
        openCountryDialog(strategy) {
            this.$emit("open-country-dialog", strategy);
        },
        openCountryChannelDialog(strategy) {
            this.$emit("open-countrychannel-dialog", strategy);
        }
    },
}
</script>