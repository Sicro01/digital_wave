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
                        :headers="headerRow"
                        :items="items"
                        hide-default-footer
                        class="pb-3">

                        <template v-slot:body="{ items }">
                            <tbody>
                                <tr v-for="(item, itemIndex) in items">
                                    <td>{{ item.code }}</td>
                                    <template v-for="(country, countryIndex) in item.countries">
                                        <td>
                                            <v-checkbox
                                                v-model="country.auto_allocate"
                                                color="secondary"
                                                :readonly="locked"
                                                dense
                                                hide-details
                                                @change="includeChange(item, itemIndex, country, countryIndex)"></v-checkbox>
                                            </v-checkbox>
                                        </td>
                                        <td>
                                            <v-text-field
                                                v-model="country.budget"
                                                :readonly="locked"
                                                :disabled="!country.auto_allocate"
                                                :rules="country.auto_allocate ? [rules.notEmpty, rules.inRange] : []"
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

export default {
    name: 'TargetChannelCard',
    components: {
        CardIcons,
    },
    data() {
        return {
            headerRow: [],
            headers: [],
            items: [],
            itemLabels: [],
            budgetValues: [],
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
        async selectedStrategy(newValue) {
            await this.getTargetCountries()
            await this.getTargetChannels()
            await this.createHeaders()
            await this.createItems()
        },
    },
    mounted() {
        this.createItems()
        this.createHeaders()
    },
    methods: {
        async getTargetCountries() {
            var response = ''
            try {
                response = await axios.get(`api/v1/targetcountries`, {
                    params: {
                        strategy: this.selectedStrategy.id,
                    }
                })
            }
            catch (error) {
                console.log(error)
            }
            // Refresh Strategy's Stored  Target Country data 
            this.$store.dispatch('storeTargetCountries', response.data)
        },
        async getTargetChannels() {
            var storedTargetChannels = []
            for (const target_country of this.storedTargetCountries) {
                var response = ''
                try {
                    response = await axios.get(`api/v1/targetchannels`, {
                        params: {
                            target_country_id: target_country.id,
                        }
                    })
                }
                catch (error) {
                    console.log(error)
                }
                if (typeof (response.data) !== 'undefined') {
                    let target_channels = response.data
                    target_channels.forEach(tch => storedTargetChannels.push(tch))
                }
            }
            this.$store.dispatch('storeTargetChannels', storedTargetChannels)
            // console.log('PlanDetailView: getTargetChannels:storedTargetChannels:', this.storedTargetChannels)
        },
        createItems() {
            this.items = []
            this.storedChannels.forEach(ch => {
                let item = { ...ch }
                item.countries = []
                this.storedTargetCountries.forEach(tco => {
                    let found_target_channel = this.storedTargetChannels.find(tch => tch.channel === ch.id && tch.target_country === tco.id)
                    if (found_target_channel) {
                        item.countries.push({
                            target_country_id: tco.id,
                            auto_allocate: found_target_channel.auto_allocate,
                            budget: found_target_channel.budget
                        })
                    } else {
                        item.countries.push({
                            target_country_id: tco.id,
                            auto_allocate: false,
                            budget: ''
                        })
                    }
                })
                this.items.push(item)
            })
        },
        createHeaders() {
            this.headerRow = []
            let channel = {
                text: 'Channel',
                align: 'start',
                sortable: false,
                value: 'code',
                class: "black--text text-subtitle-1",
                width: "50px",
            }
            this.headerRow.push(channel)
            if (this.storedTargetCountries.length > 0) {
                this.storedTargetCountries.map(tco => {
                    // Create a header for each country - where we'll place a checkbox 
                    var country = {
                        text: tco.code,
                        align: 'start',
                        sortable: false,
                        value: "auto_allocate",
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
            } else {
                // Create a header indicating no countries have been selected
                var no_countries_selected = {
                    text: 'No Target Countries Selected',
                    align: 'start',
                    sortable: false,
                    value: "auto_allocate",
                    class: "black--text text-subtitle-1",
                    width: "50px",
                }
                this.headerRow.push(no_countries_selected)
            }
        },
        save() {
            let newTargetChannelObjects = []
            this.items.map(i => {
                i.countries.map(c => {
                    if (c.auto_allocate) {
                        let obj = {
                            channel: i.id,
                            target_country: c.target_country_id,
                            code: i.code,
                            name: i.name,
                            auto_allocate: c.auto_allocate,
                            budget: c.budget,
                            budget_allocated: 0,
                        }
                        newTargetChannelObjects.push(obj)
                    }
                })
            })

            // Which countries has the user deleted?
            var deleteTargetChannelIds = this.diffArray(newTargetChannelObjects)
            this.$emit('update-target-channels', newTargetChannelObjects, deleteTargetChannelIds)
            this.locked = true
        },
        diffArray(newTargetChannelObjects) {
            function diff(newTargetChannelObjects, current_tch) {
                for (let newItem of newTargetChannelObjects) {
                    if (newItem.target_country_id === current_tch.target_country_id && newItem.channel === current_tch.channel) {
                        return true
                    }
                }
                return false
            }
            let deleteTargetChannelIds = []
            this.storedTargetChannels.forEach(current_tch => {
                if (!diff(newTargetChannelObjects, current_tch)) {
                    deleteTargetChannelIds.push(current_tch)
                }
            })
            return deleteTargetChannelIds
        },
        cancel() {
            this.locked = true
            this.createItems()
        },
        includeChange(item, itemIndex, country, countryIndex) {
            !country.auto_allocate ? country.budget = '' : null
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