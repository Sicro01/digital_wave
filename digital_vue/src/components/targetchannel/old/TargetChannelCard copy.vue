<template>
    <v-form
        ref="form"
        v-model="valid">
        <v-card class="mt-3 mx-3">
            <v-card-title class="py-0">
                Select Channels and Set Budgets for Target Countries
                <v-spacer></v-spacer>
                <CardIcons
                    :showEditIcon="true"
                    :showHideIcon="true"
                    @edit="(locked = !locked)"
                    @hide="$emit('hide')"
                    cardType="Linked Channels" />
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <v-row class="text--disabled">
                    <v-col cols="auto" class="py-0 d-flex align-center">Phase Budget:</v-col>
                    <v-col cols="auto" class="d-flex align-center">
                        <v-text-field
                            :value="selectedPhase.budget"
                            label="Budget"
                            outlined
                            dense
                            disabled
                            hide-details>
                        </v-text-field>
                        <v-col cols="auto" class="py-0 d-flex align-center">
                            <v-text-field
                                :value="selectedPhase.auto_allocate ? 'Yes' : 'No'"
                                label="Budget Autoallocated?"
                                outlined
                                dense
                                disabled
                                hide-details>
                            </v-text-field>
                        </v-col>
                    </v-col>
                    <v-col cols="auto" class="py-0 d-flex align-center">Strategy Budget:</v-col>
                    <v-col cols="auto" class="d-flex align-center">
                        <v-text-field
                            :value="selectedStrategy.budget"
                            label="Budget"
                            outlined
                            dense
                            disabled
                            hide-details>
                        </v-text-field>
                        <v-col cols="auto" class="py-0 d-flex align-center">
                            <v-text-field
                                :value="selectedStrategy.auto_allocate ? 'Yes' : 'No'"
                                label="Budget Autoallocated?"
                                outlined
                                dense
                                disabled
                                hide-details>
                            </v-text-field>
                        </v-col>
                    </v-col>
                </v-row>
            </v-card-text>

            <v-card-text>
                <v-sheet
                    class="mb-3 grey"
                    tile
                    outlined>
                    <v-data-table
                        :headers="headers"
                        :items="items"
                        hide-default-footer
                        class="pb-3">

                        <template v-slot:body="{ items }">
                            <tbody>
                                <tr v-for="(item, itemIndex) in items" :key="itemIndex">
                                    <td>
                                        {{ item.channel_code }}
                                    </td>
                                    <template v-for="(labels, labelIndex) in itemLabels">
                                        <td>
                                            <v-checkbox
                                                v-model="item[labels.checked]"
                                                color="secondary"
                                                :readonly="locked"
                                                dense
                                                hide-details
                                                @change="includeChange(item, labels, labelIndex, itemIndex)"></v-checkbox>
                                        </td>
                                        <td>
                                            <v-text-field
                                                :readonly="locked"
                                                :disabled="!item[labels.checked]"
                                                v-model="item[labels.budget]"
                                                :rules="item[labels.checked] ? [rules.notEmpty, rules.inRange] : []"
                                                label="Budget"
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

                        <!-- <template v-slot:body="{ items }">
                            <tbody>
                                <tr v-for="(item, itemIndex) in items" :key="itemIndex">
                                    <td>
                                        {{ item.channel_code }}
                                    </td>
                                    <template v-for="(labels, labelIndex) in itemLabels">
                                        <td>
                                            <v-checkbox
                                                v-model="item[labels.checked]"
                                                color="secondary"
                                                :readonly="locked"
                                                dense
                                                hide-details
                                                @change="includeChange(item, labels, labelIndex, itemIndex)"></v-checkbox>
                                        </td>
                                        <td>
                                            <v-text-field
                                                :readonly="locked"
                                                :disabled="!item[labels.checked]"
                                                v-model="item[labels.budget]"
                                                :rules="item[labels.checked] ? [rules.notEmpty, rules.inRange] : []"
                                                label="Budget"
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
                        </template> -->
                    </v-data-table>
                </v-sheet>
                <div class="caption text--disabled">
                    <span>Last edit: {{ targetChannelsLastEdited }}</span>
                    <!-- <span>Last edit:{{ targetCountriesLastEdited.toLocaleDateString(("en-GB")) }}</span>
                    <span> {{ targetCountriesLastEdited.toLocaleTimeString(("en-GB")) }}</span> -->
                </div>
            </v-card-text>
            <v-card-actions v-if="!locked">
                <v-spacer></v-spacer>
                <v-btn
                    class="grey lighten-1 mr-3 rounded-0 text-capitalize"
                    light
                    depressed
                    @click="cancel">
                    Cancel
                </v-btn>
                <v-btn
                    class="mr-3 success rounded-0 text-capitalize"
                    depressed
                    :disabled="(!valid)"
                    @click="save">
                    Save
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-form>
</template>
<script>
import CardIcons from '@/components/shared/CardIcons'
import axios from 'axios'
import ConfirmDialog from '../../dialogs/ConfirmDialog.vue'

export default {
    name: 'CountryCard',
    components: {
        CardIcons,
    },
    data() {
        return {
            rows: [],
            headerRow: [],
            headers: [],
            items: [],
            itemLabels: [],
            budgetValues: [],
            countryChannelData: [],
            locked: true,
            valid: false,
            rules: {
                required: (v => !!v || "Required"),
                notEmpty: (v => (v.toString().length > 0) || "Budget should be between 0 and 10,000,000"),
                inRange: (v => (Number.isInteger(Number(v)) && v >= 0 && v <= 10000000) || "Budget should be between 0 and 10,000,000"),
            },
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
        storedTargetCountries: {
            get() {
                return this.$store.state.storedTargetCountries
            }
        },
        storedTargetChannels: {
            get() {
                return this.$store.state.storedTargetChannels
            }
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
        targetChannelsLastEdited: {
            get() {
                if (this.storedTargetChannels.length > 0) {
                    let lastEditDate = new Date(Math.max(...this.storedTargetChannels.map(e => new Date(e.date_modified)))).toLocaleDateString('en-GB');
                    let lastEditTime = new Date(Math.max(...this.storedTargetChannels.map(e => new Date(e.date_modified)))).toLocaleTimeString('en-GB');
                    return `${lastEditDate} ${lastEditTime}`
                } else {
                    return 'N/A'
                }
            }
        }
    },
    watch: {
        async storedTargetCountries(newValue) {
            console.log('TargetChannelCard: watch: storedTargetCountries', this.storedTargetCountries)
            await this.createHeaders()
            await this.createItemLabels()
            await this.createDataItems()
        },
    },
    mounted() {
        this.createHeaders()
        this.createItemLabels()
        this.createDataItems()
        this.newItems1()
        this.newHeader()
    },
    methods: {
        createHeaders() {
            this.headers = []
            // Header 1: Create Channel Header
            var channelCodeHeader = {
                text: 'Channel',
                align: 'center',
                sortable: false,
                value: 'channel_code',
                class: "black--text text-subtitle-1",
                width: "50px",
            }
            this.headers.push(channelCodeHeader)

            // Headers 2 to nnn (2 header per country: 
            var index = 0
            this.storedTargetCountries.forEach((country) => {
                // Create a header for each country - where we'll place a checkbox 
                var countryHeader = {
                    text: country.code,
                    align: 'start',
                    sortable: false,
                    value: 'checked' + country.code + index,
                    class: "black--text text-subtitle-1",
                    width: "50px",
                }
                this.headers.push(countryHeader)

                // Create a header for each country budget - where we'll place a budget field
                var budgetHeader = {
                    text: 'Budget',
                    align: 'center',
                    sortable: false,
                    value: "budget" + country.code + index,
                    class: "black--text text-subtitle-1",
                    width: "150px",
                }
                this.headers.push(budgetHeader)

                // Increment the count used to make the value field name unique
                // This must match the field name in the actual table row
                index += 1
            })
            console.log('TargetChannelCard:createHeaders:headers: ', this.headers)
        },
        createItemLabels() {
            this.itemLabels = []
            // Create a label for each country and each country budget
            // Used to unqiuely identify a country per channel - and the set the value of the checkbox when
            // we create the data items
            var index = 0
            // console.log(this.storedTargetCountries)
            this.storedTargetCountries.forEach((country) => {
                var checkBoxBudgetLabel = {
                    checked: 'checked' + country.code + index,
                    budget: 'budget' + country.code + index,
                    country_id: 'country_id' + country.code,
                    country_code: 'country_code' + country.code,
                    country_name: 'country_name' + country.code,
                }
                this.itemLabels.push(checkBoxBudgetLabel)

                // Increment the count used to make the value field name unique
                // This must match the field name in the header row
                index += 1
            })
            console.log('TargetChannelCard:createItemLabels:itemLabels: ', this.itemLabels)
        },
        createDataItems() {
            // Table Data
            // Cycle through each country for each channel - creating:
            // Value 1 - channel
            // Value 2 & 3 per country (checkbox - with the checkboxValue label e.g. checkedDE01, checkedGB01) amd budget
            // console.log('TargetChannelCard:createDataItems:this.storedChannels: ', this.storedChannels)
            this.items = []
            this.storedChannels.forEach((channel) => {
                // console.log(this.storedChannels)
                // Value 1: Channel
                var item = {
                    'channel_id': channel.id,
                    'channel_code': channel.code,
                    'channel_name': channel.name,
                }
                // Values 2 to nnn: Country check box AND budget field for each channel / country combination
                var index = 0
                this.storedTargetCountries.forEach((country) => {
                    // Set Country Id
                    item = Object.assign({
                        [this.itemLabels[index].country_id]: country.country,
                    }, item)

                    // Set Country Code
                    item = Object.assign({
                        [this.itemLabels[index].country_code]: country.code,
                    }, item)

                    // Set Country Name
                    item = Object.assign({
                        [this.itemLabels[index].country_name]: country.name,
                    }, item)

                    // Set country / channel checkbox value
                    item = Object.assign({
                        [this.itemLabels[index].checked]: false,
                    }, item)

                    // Set country / channel budget value
                    item = Object.assign({
                        [this.itemLabels[index].budget]: '',
                    }, item)

                    index += 1
                })
                this.items.push(item)
                // console.log('TargetChannelCard:createDataItems:item: ', item)
            })
            console.log('TargetChannelCard:createDataItems:items: ', this.items)
            // console.log('items: ', this.items)
        },
        save() {
            // Build array of countries
            // var targetCountries = []
            // this.items.forEach((item) => {
            //     if (item.include) {
            //         let itemObj = {
            //             strategy: this.selectedStrategy.id,
            //             country: item.country_id,
            //             code: item.country_code,
            //             name: item.country_name,
            //             budget: item.budget,
            //             auto_allocate: item.auto_allocate,
            //             budget_allocated: 0,
            //         }
            //         targetCountries.push(itemObj)
            // console.log('TargetCountryCard: save: itemObj', itemObj)
            // }
            // })

            var targetChannels = []
            this.items.forEach((item) => {
                this.itemLabels.forEach((country) => {
                    if (item[country.checked]) {
                        // console.log('item: ', item)
                        // console.log('item channel_id: ', item['channel_id'])
                        // console.log('item channel_code: ', item['channel_code'])
                        // console.log('item channel_name: ', item['channel_name'])
                        // console.log('item country_id: ', item['country_id'])
                        // console.log('item country_code: ', item['country_code'])
                        // console.log('item country_name: ', item['country_name'])
                        // console.log('item budget: ', item[country.budget])
                        // console.log('item checked: ', item[country.checked])

                        let itemObj = {
                            target_country: item['country_code'],
                            channel: item['channel_id'],
                            code: item['channel_code'],
                            name: item['channel_name'],
                            budget: item[country.budget],
                            budget_allocated: 0,
                            auto_allocate: true,
                        }
                        targetChannels.push(itemObj)
                    }
                })
            })
            this.$emit('update-target-channels', targetChannels)
            this.locked = true
        },
        cancel() {
            this.locked = true
            // this.createItems()
        },
        includeChange(item, labels, labelIndex, itemIndex) {
            !item[labels.checked] ? item[labels.budget] = '' : null
        },
        newItems() {
            let i = []
            this.storedChannels.forEach(channel => {
                let ch = { ...channel }
                ch.target_countries = []
                console.log('ch:', ch)
                console.log('ch array langth:', ch.target_countries.length)
                this.storedTargetCountries.forEach((target_country, index) => {
                    console.log('target_country:', target_country)
                    // If target channel exists then  populate displayed info with correct values
                    if (this.storedTargetChannels.length > 0) {
                        console.log('searching stored_channels:', this.storedTargetChannels)
                        let found_target_channel = this.storedTargetChannels.find(target_channel =>
                            target_channel.code === ch.code && target_country.code === target_channel.country)
                        if (found_target_channel) {
                            console.log('existing target_channel found')
                            let country = {
                                auto_allocate: found_target_channel.auto_allocate,
                                budget: found_target_channel.budget,
                            }
                            ch.target_countries.push(country)
                        }
                        else {
                            console.log('existing target_channel NOT found')
                            let country = {
                                auto_allocate: false,
                                budget: 'a',
                            }
                            ch.target_countries.push(country)
                        }
                    }
                    else {
                        console.log('no stored_channels exist')
                        let country = {
                            auto_allocate: false,
                            budget: '',
                        }
                        ch.target_countries.push(country)
                    }

                })
                i.push(ch)
                console.log('i:', i)
            })
            // console.log(i)
            i.forEach(i => {
                console.log(i.code)
                i.target_countries.forEach(c => {
                    console.log(c.auto_allocate, c.budget)
                })
            })
            // console.log(output)
        },
        newItems1() {
            this.rows = []
            this.storedChannels.forEach(ch => {
                console.log(ch.code)
                let row = { ...ch }
                row.countries = []
                this.storedTargetCountries.forEach(tco => {
                    console.log('tco:', tco)
                    if (this.storedTargetChannels.find(tch => tch.code === ch.code && tch.target_country === tco.code)) {
                        row.countries.push({ target_country: tco.country, auto_allocate: tch.auto_allocate, budget: tch.budget })
                    } else {

                        row.countries.push({ target_country: tco.country, auto_allocate: false, budget: '' })
                    }
                })
                this.rows.push(row)
            })
            console.log('rows:', this.rows)
        },
        newHeader() {
            this.headerRow = []
            let channel = {
                text: 'Channel',
                align: 'center',
                sortable: false,
                value: 'channel_code',
                class: "black--text text-subtitle-1",
                width: "50px",
            }
            this.headerRow.push(channel)
            this.storedTargetCountries.map(tco => {
                // Create a header for each country - where we'll place a checkbox 
                var country = {
                    text: tco.code,
                    align: 'start',
                    sortable: false,
                    value: 'checked',
                    class: "black--text text-subtitle-1",
                    width: "50px",
                }
                this.headerRow.push(country)

                // Create a header for each country budget - where we'll place a budget field
                var budget = {
                    text: 'Budget',
                    align: 'center',
                    sortable: false,
                    value: "budget",
                    class: "black--text text-subtitle-1",
                    width: "150px",
                }
                this.headerRow.push(budget)
            })
            console.log('newHeader:', this.headerRow)
        }
    }
}
</script>
<style scoped>
table>tbody>tr>td:nth-child(1),
table>thead>tr>th:nth-child(1) {
    position: sticky !important;
    position: -webkit-sticky !important;
    left: 0;
    z-index: 9998;
    background: white;
}

table>thead>tr>th:nth-child(1) {
    z-index: 9999;
}
</style>
<!-- // async getTargetCountries() {
    //     var response = ''
    //     try {
    //         response = await axios.get(`api/v1/targetcountries`, {
    //             params: {
    //                 strategy: this.selectedStrategy.id,
    //             }
    //         })
    //     }
    //     catch (error) {
    //         console.log(error)
    //     }
    //     // Refresh Strategy's Stored  Target Country data 
    //     this.$store.dispatch('storeTargetCountries', response.data)
    // },
    // createItems() {
    //     this.items = []
    //     // Table Data - check box AND budget field for each country
    //     var index = 0
    //     this.storedCountries.forEach((country) => {
    //         var item = {
    //             'id': country.id,
    //             'country': country.name,
    //             'include': false,
    //             'budget': '',
    //             'auto_allocate': false,
    //         }
    //         // See if this country is already a target country
    //         let foundTargetCountry = this.storedTargetCountries.find(targetCountry =>
    //             targetCountry.country == item.id
    //         )
    //         // Update table data item with target country settings
    //         if (foundTargetCountry) {
    //             item.include = true
    //             item.budget = foundTargetCountry.budget
    //             item.budget_allocated = foundTargetCountry.budget_allocated
    //             item.auto_allocate = foundTargetCountry.auto_allocate
    //         }
    //         this.items.push(item)
    //     })
    // },
    // save() {
    //     // Build array of countries
    //     this.locked = true
    //     var targetCountries = []
    //     console.log('save: ', this.items)
    //     this.items.forEach((item) => {
    //         if (item.include) {
    //             let itemObj = {
    //                 strategy: this.selectedStrategy.id,
    //                 country: item.id,
    //                 budget: item.budget,
    //                 auto_allocate: item.auto_allocate,
    //                 budget_allocated: 0,
    //             }
    //             targetCountries.push(itemObj)
    //         }
    //     })
    //     this.$emit('update-target-countries', targetCountries)
    // },
    // cancel() {
    //     this.locked = true
    //     this.createItems()
    // } -->