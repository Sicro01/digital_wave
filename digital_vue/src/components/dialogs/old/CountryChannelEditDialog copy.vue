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
                            hide-default-header
                            hide-default-footer>

                            <template v-slot:header="{ props: { headers } }">
                                <thead>
                                    <tr>
                                        <th v-for="h in headers" class=" ">
                                            <span>{{ h.text }}</span>
                                        </th>
                                    </tr>
                                </thead>
                            </template>

                            <template v-slot:body="{ items }">
                                <tbody>
                                    <tr v-for="(item, propertyName, itemIndex) in items" :key="itemIndex">
                                        <td>
                                            {{ item.channelCode }}
                                        </td>
                                        <td v-for="(checked, checkedIndex) in checkboxValues" :key="checkedIndex">
                                            <v-checkbox
                                                :value="item[checked]"
                                                @change="checkChange(item, checked, checkedIndex, $event)"
                                                @click="checkClick(item, checked, checkedIndex)"></v-checkbox>
                                        </td>
                                        <td>
                                            <v-text-field
                                                @input="$emit('input', $event)"
                                                label="Budget"
                                                dense
                                                hide-details
                                                class="shrink rounded-0"
                                                outlined>
                                            </v-text-field>
                                            {{ propertyName }}{{ itemIndex }}
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
            checkBox: [],
            tableHeaders: [],
            tableItems: [],
            tableItemLabels: [],
            checkboxValues: [],
            budgetValues: [],
            checked: []
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
        this.getCountries()
        this.getChannels()
        this.createTableHeaders()
        this.createTableItemLabels()
        this.createTableItems()
    },
    methods: {
        async getCountries() {
            var response = ''
            try {
                response = await axios.get(`/api/v1/countries`)
            }
            catch (error) {
                console.log(error)
            }
            this.$store.dispatch('storeCountries', response.data)
        },
        async getChannels() {
            var response = ''
            try {
                response = await axios.get(`/api/v1/channels`)
            }
            catch (error) {
                console.log(error)
            }
            this.$store.dispatch('storeChannels', response.data)
        },
        createTableHeaders() {
            // Header 1: Create Channel Header
            var header = {
                text: 'Channel',
                align: 'start',
                sortable: false,
                value: 'channelCode'
            }
            this.tableHeaders.push(header)

            // Headers 2 to nnn (2 header per country: 
            var index = 0
            this.storedCountries.forEach((country) => {
                // Create a header for each country - where we'll place a checkbox 
                var countryHeader = {
                    text: country.code,
                    align: 'start',
                    sortable: false,
                    value: 'countryCode' + index
                }
                this.tableHeaders.push(countryHeader)

                // Create a header for each country budget - where we'll place a budget field
                var budgetHeader = {
                    text: 'Budget',
                    align: 'start',
                    sortable: false,
                    value: 'budgetAmount' + index
                }
                this.tableHeaders.push(budgetHeader)

                // Increment the count used to make the value field name unique
                // This must match the field name in the actual table row
                index += 1
            })
            console.log('tableHeaders: ', this.tableHeaders)
        },
        createDataItemLabels() {
            // Create a label for each country and each country budget
            // County Labels
            // Used to unqiuely identify a country per channel - and the set the value of the checkbox when
            // We create the data items
            var index = 0
            this.storedCountries.forEach((country) => {
                this.checkboxValues.push('checked' + country.code + index)
                this.budgetValues.push('budget' + country.code + index)
                index += 1
            })
            console.log('checkboxValues: ', this.checkboxValues)
            console.log('budgetValues: ', this.budgetValues)
        },
        createTableItems() {
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
                    // Add checkbox value
                    item = Object.assign({
                        [this.checkboxValues[index]]: false,
                    }, item)
                    // Add budget value
                    item = Object.assign({
                        [this.budgetValues[index]]: 0,
                    }, item)
                    index += 1
                })
                this.tableItems.push(item)
            })
            console.log('tableItems: ', this.tableItems)
            // console.log('checkboxValues: ', this.checkboxValues)
        },
        checkClick(item, checked, index) {
            // console.log('checkBox clicked:', item[checked])
            var checkObj = {
                channel: item.channelCode,
                country: this.storedCountries[index].code
            }
            // this.checked.push(checkObj)
            // console.log('Channel: ', item.channelCode)
            // console.log('Country: ', this.storedCountries[index].code)
        },
        checkChange(item, checked, index, newValue) {
            if (item[checked] != newValue) {
                console.log('new value: ', item[checked], newValue)
            } else {
                console.log('NOT new value: ', item[checked], newValue)
            }
            item[checked] = newValue
            if (item[checked]) {
                var checkObj = {
                    channel: item.channelCode,
                    country: this.storedCountries[index].code
                }
                this.checked.push(checkObj)
            } else {
                let x = this.storedCountries[index].code
                this.checked = this.checked.filter(function (o) {
                    return !(o.channel === item.channelCode && o.country === x)
                })
                console.log('this.checked AFTER REMOVE: ', this.checked)
            }
        },
        save() {
            Object.keys(this.$refs.form.inputs).forEach((item) => {
                console.log('form item: ', item)
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

/* @media screen and (max-width: 1200px) {

    .v-data-table.theme--light tbody>thead>tr {
        border-bottom: medium solid rgba(212, 7, 7, 0.957) !important;
    }
} */

/* bob {
    .theme--light.v-data-table border-spacing: 0.5rem !important;
} */

.theme--light.v-data-table>.v-data-table__wrapper>table>thead>tr:last-child>th {
    /* border-bottom: medium solid rgba(212, 7, 7, 0.957) !important; */
    background-color: var(--v-primary-base);
    font-weight: bold;
    font-size: medium;
    color: white;
}

tbody tr:nth-of-type(odd) {
    background-color: rgba(0, 0, 0, .05);
}


.theme--light.v-data-table>.v-data-table__wrapper>table>tbody>tr:not(:last-child)>th:not(.v-data-table__mobile-row) {
    border-right: thin solid rgba(0, 0, 0, 0.12);
    border: thin solid rgba(0, 0, 0, 0.12);
}

/* var(--v-primary-base) */
/* .theme--light.v-data-table {
    border-bottom: medium solid rgba(212, 7, 7, 0.957) !important;
} */

.mytable>tr {
    border-bottom: medium solid rgba(212, 7, 7, 0.957) !important;
}

::v-deep .v-data-table-header {
    background-color: #FF0000;
}
</style>