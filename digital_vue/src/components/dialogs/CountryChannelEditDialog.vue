<template>
    <v-form
        ref="form">
        <v-dialog
            v-model="show"
            persistent
            :width="width">
            <v-card>
                <v-card-title>
                    Select Country / Channel combinations
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
                                        <td>
                                            {{ item.channelCode }}
                                        </td>
                                        <template v-for="(labels, labelIndex) in tableItemLabels">
                                            <td>
                                                <v-checkbox
                                                    v-model="item[labels.checked]"
                                                    color="secondary"
                                                    dense
                                                    hide-details
                                                    @change="checkBoxChange(item, labels, labelIndex, itemIndex)"></v-checkbox>
                                            </td>
                                            <td>
                                                <v-text-field
                                                    :disabled="!item[labels.checked]"
                                                    v-model="item[labels.budget]"
                                                    @input="budgetFieldChange(item, labelIndex, $event)"
                                                    label="Country / Channel Budget"
                                                    type="number"
                                                    dense
                                                    hide-details
                                                    class="shrink rounded-0"
                                                    outlined>
                                                </v-text-field>
                                            </td>
                                        </template>
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
            tableHeaders: [],
            tableItems: [],
            tableItemLabels: [],
            budgetValues: [],
            countryChannelData: [],
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
                    case 'lg': return 1200
                    case 'xl': return 1600
                }
            }
        },
    },
    mounted() {
        // We need an unknown number of headers and data item columns - depends on the number of countries
        // These functions create th ebespoke, unique headers / column names and data and capture the user choices in 
        // "countryChannelData" - which is then passed back to the parent to update the database    
        this.createTableHeaders()
        this.createTableItemLabels()
        this.createDataItems()
    },
    methods: {
        createTableHeaders() {
            // Header 1: Create Channel Header
            var channelCodeHeader = {
                text: 'Channel',
                align: 'start',
                sortable: false,
                value: 'channelCode',
                class: "secondary white--text text-subtitle-1 font-weight-bold",
            }
            this.tableHeaders.push(channelCodeHeader)

            // Headers 2 to nnn (2 header per country: 
            var index = 0
            this.storedCountries.forEach((country) => {
                // Create a header for each country - where we'll place a checkbox 
                var countryHeader = {
                    text: country.code,
                    align: 'start',
                    sortable: false,
                    value: 'checked' + country.code + index,
                    class: "secondary white--text text-subtitle-1 font-weight-bold",
                }
                this.tableHeaders.push(countryHeader)

                // Create a header for each country budget - where we'll place a budget field
                var budgetHeader = {
                    text: 'Budget',
                    align: 'center',
                    sortable: false,
                    value: "budget" + country.code + index,
                    class: "secondary white--text text-subtitle-1 font-weight-bold",
                }
                this.tableHeaders.push(budgetHeader)

                // Increment the count used to make the value field name unique
                // This must match the field name in the actual table row
                index += 1
            })
            // console.log('tableHeaders: ', this.tableHeaders)
        },
        createTableItemLabels() {
            // Create a label for each country and each country budget
            // County Labels
            // Used to unqiuely identify a country per channel - and the set the value of the checkbox when
            // We create the data items
            var index = 0
            this.storedCountries.forEach((country) => {
                var checkBoxBudgetLabel = {
                    checked: 'checked' + country.code + index,
                    budget: 'budget' + country.code + index
                }
                this.tableItemLabels.push(checkBoxBudgetLabel)

                // Increment the count used to make the value field name unique
                // This must match the field name in the header row
                index += 1
            })
            // console.log('tableItemLabels: ', this.tableItemLabels)
            // Reset count for every country
            index = 0
        },
        createDataItems() {
            // Table Data
            // Cycle through each country for every channel - creating:
            // Value 1 per channel and a value per
            // Value 2 & 2+1 per country (checkbox - with the checkboxValue label e.g. checkedDE01, checkedGB01)
            this.storedChannels.forEach((channel) => {
                // Value 1: Channel
                var item = {
                    'channelCode': channel.code,
                }
                // Values 2 to nnn: Country check box AND budget field for each channel / country combination
                var index = 0
                this.storedCountries.forEach((country) => {

                    // Set country / channel checkbox value
                    item = Object.assign({
                        [this.tableItemLabels[index].checked]: false,
                    }, item)

                    // Set country / channel budget value
                    item = Object.assign({
                        [this.tableItemLabels[index].budget]: '',
                    }, item)

                    index += 1
                })
                this.tableItems.push(item)
            })
            // console.log('tableItems: ', this.tableItems)
        },
        checkBoxChange(currentItem, labels, labelIndex, itemIndex) {
            if (currentItem[labels.checked]) {
                var countryChannelObj = {
                    channelId: this.storedChannels[itemIndex].id,
                    channelCode: currentItem.channelCode,
                    channelName: this.storedChannels[itemIndex].name,
                    countryId: this.storedCountries[labelIndex].id,
                    countryCode: this.storedCountries[labelIndex].code,
                    countryName: this.storedCountries[labelIndex].name,
                    countryChannelBudget: 0,
                }
                this.countryChannelData.push(countryChannelObj)
            } else {
                let currentCountry = this.storedCountries[index].code
                this.countryChannelData = this.countryChannelData.filter(function (savedItem) {
                    return !(savedItem.channelCode === currentItem.channelCode && savedItem.countryCode === currentCountry)
                })
            }
            this.displayChanges()
        },
        budgetFieldChange(currentItem, index, event) {
            let currentCountryCode = this.storedCountries[index].code
            let savedObj = this.countryChannelData.find((savedItem) =>
                savedItem.channelCode === currentItem.channelCode && savedItem.countryCode === currentCountryCode)
            savedObj.countryChannelBudget = +event
            this.displayChanges()
        },
        save() {
            // Build array of countries
            var selectedCountries = []
            this.countryChannelData.forEach((item) => {
                var countryObj = {
                    id: item.countryId,
                }
                selectedCountries.push(countryObj)
            })
            var selectedChannels = []
            this.countryChannelData.forEach((item) => {
                var countryChannelObj = {
                    countryId: item.countryId,
                    channelId: item.channelId,
                    countryChannelBudget: item.countryChannelBudget
                }
                selectedChannels.push(countryChannelObj)
            })
            var savePayload = {
                strategy: this.strategy,
                countryChannelData: this.countryChannelData,
            }
            this.$emit('update-strategy-country-channel', savePayload)
        },
        displayChanges() {
            console.log('# items: ', this.countryChannelData.length)
            this.countryChannelData.forEach((item) => {
                console.log('item: ', item)
            })
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
