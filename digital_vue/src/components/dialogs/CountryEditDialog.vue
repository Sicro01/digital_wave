<template>
    <v-form
        ref="form">
        <v-dialog
            v-model="show"
            persistent
            :width="width">
            <v-card>
                <v-card-title>
                    Select Countries and Set Budgets
                </v-card-title>
                <v-card-text>
                    <v-sheet
                        class="mb-3 black elevation-2"
                        outlined>

                        <v-data-table
                            :headers="tableHeaders"
                            :items="tableItems"
                            hide-default-footer
                            class="pb-3">

                            <template v-slot:body="{ items }">
                                <tbody>

                                    <tr v-for="(item, itemIndex) in items" :key="itemIndex">
                                        <td>{{ item.country }}</td>

                                        <td class="d-flex justify-center">
                                            <v-checkbox
                                                v-model="item.include"
                                                color="secondary"
                                                dense
                                                hide-details
                                                @change="checkBoxChange(item, itemIndex)"></v-checkbox>
                                        </td>
                                        <td>
                                            <v-text-field
                                                :disabled="!item.include"
                                                v-model="item.budget"
                                                @input="budgetFieldChange(item, itemIndex, $event)"
                                                label="Country / Channel Budget"
                                                type="number"
                                                dense
                                                hide-details
                                                class="shrink rounded-0"
                                                outlined>
                                            </v-text-field>
                                        </td>
                                        <td class="d-flex justify-center">
                                            <v-checkbox
                                                v-model="item.autoallocate"
                                                color="secondary"
                                                dense
                                                hide-details></v-checkbox>
                                        </td>
                                    </tr>
                                </tbody>
                            </template>
                        </v-data-table>
                    </v-sheet>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        class="grey lighten-1 mr-3 rounded-0 text-capitalize"
                        light
                        depressed
                        @click="show = false">
                        Cancel
                    </v-btn>
                    <v-btn
                        class="mr-3 success rounded-0 text-capitalize"
                        depressed
                        @click="save">
                        Save
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-form>
</template>
<script>
import axios from 'axios'

export default {
    props: {
        value: Boolean,
        strategy: Object,
    },
    data() {
        return {
            tableHeaders: [
                {
                    text: 'Country',
                    align: 'start',
                    sortable: false,
                    value: 'country',
                    class: "secondary white--text text-subtitle-1 font-weight-bold",
                },
                { text: 'Include?', align: 'center', value: 'include', class: "secondary white--text text-subtitle-1 font-weight-bold" },
                { text: 'Budget', align: 'center', value: 'budget', class: "secondary white--text text-subtitle-1 font-weight-bold", },
                { text: 'Autoallocate?', align: 'center', value: 'autoallocate', class: "secondary white--text text-subtitle-1 font-weight-bold", },
            ],
            tableItems: [],
            tableItemLabels: [],
            budgetValues: [],
        }
    },
    computed: {
        show: {
            get() {
                return this.value
            },
            set(value) {
                this.$emit('input', value)
            },
        },
        storedCountries: {
            get() {
                return this.$store.state.storedCountries
            }
        },
        storedChannels: {
            get() {
                return this.$store.state.storedChannels
            }
        },
        // Hack to set width of v-dialog
        width: {
            get() {
                switch (this.$vuetify.breakpoint.name) {
                    case 'xs': return 220
                    case 'sm': return 600
                    case 'md': return 800
                    case 'lg': return 800
                    case 'xl': return 800
                }
            }
        },
    },
    mounted() {
        this.createDataItems()
    },
    methods: {
        createDataItems() {
            // Table Data - check box AND budget field for each country
            var index = 0
            this.storedCountries.forEach((country) => {
                var item = {
                    'id': country.id,
                    'country': country.name,
                    'include': false,
                    'budget': '',
                    'autoallocate': false,
                }
                this.tableItems.push(item)
            })
            // console.log('tableItems: ', this.tableItems)
        },
        budgetFieldChange(currentItem, index, event) {
            let currentCountryCode = this.storedCountries[index].code
            let savedObj = this.countryChannelData.find((savedItem) =>
                savedItem.channelCode === currentItem.channelCode && savedItem.countryCode === currentCountryCode)
            savedObj.countryChannelBudget = +event
        },
        save() {
            // Build array of countries
            var selectedCountries = []
            this.tableItems.forEach((item) => {
                if (item.include) {
                    selectedCountries.push(item.id)
                }
            })
            // console.log(selectedCountries)
            this.$emit('update-strategy-country', this.strategy, selectedCountries)
        },
    }

}
</script>
<style scoped>
/* @media screen and (max-width: 1200px) {
    .theme--light.v-data-table thead tr:last-child th,
    .theme--light.v-data-table tbody tr:not(:last-child) td:last-child,
    .theme--light.v-data-table tbody tr td,
    .theme--light.v-data-table tbody tr:not(:last-child) td:not(.v-data-table__mobile-row) {
        border-bottom: medium solid rgba(212, 7, 7, 0.957);
    }
} */
</style>
