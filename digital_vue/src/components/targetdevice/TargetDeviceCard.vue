<template>
    <v-form
        ref="form"
        v-model="valid">
        <v-card class="mt-3 mx-3">
            <v-card-title class="py-0">
                Select Devices and Set Budgets for Target Country/Channels
                <v-spacer></v-spacer>
                <CardIcons
                    :showEditIcon="true"
                    :showHideIcon="true"
                    @edit="(locked = !locked)"
                    @hide="$emit('hide')"
                    cardType="Linked Devices" />
            </v-card-title>
            <v-divider></v-divider>
            <!-- <v-card-text>
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
            </v-card-text> -->

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
                                    <td>{{ item.name }}</td>
                                    <template v-for="(target_channel, targetChannelIndex) in item.target_channels">
                                        <td>
                                            <v-checkbox
                                                v-model="target_channel.auto_allocate"
                                                color="secondary"
                                                :readonly="locked"
                                                dense
                                                hide-details
                                                @change="includeChange(item, itemIndex, target_channel, targetChannelIndex)"></v-checkbox>
                                            </v-checkbox>
                                        </td>
                                        <td>
                                            <v-text-field
                                                v-model="target_channel.budget"
                                                :readonly="locked"
                                                :disabled="!target_channel.auto_allocate"
                                                :rules="target_channel.auto_allocate ? [rules.notEmpty, rules.inRange] : []"
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
    name: 'TargetDeviceCard',
    components: {
        CardIcons,
    },
    data() {
        return {
            target_country: '',
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
        storedTargetDevices: {
            get() {
                return this.$store.state.storedTargetDevices
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
        storedDevices: {
            get() {
                return this.$store.state.storedDevices
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
            await this.getTargetDevices()
            await this.createHeaders()
            await this.createItems()
        },
    },
    mounted() {
        this.createItems()
        this.createHeaders()
    },
    methods: {
        async getTargetCountry(id) {
            var response = ''
            try {
                response = await axios.get(`api/v1/targetcountries/${id}`)
            }
            catch (error) {
                console.log(error)
            }
            this.target_country = response.data
        },
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
        async getTargetDevices() {
            var storedTargetDevices = []
            // console.log('PlanDetailView: getTargetDevices: storedTargetChannels: ', this.storedTargetChannels)
            for (const target_channel of this.storedTargetChannels) {
                var response = ''
                try {
                    response = await axios.get(`api/v1/targetdevices`, {
                        params: {
                            target_channel_id: target_channel.id,
                        }
                    })
                }
                catch (error) {
                    console.log(error)
                }
                if (typeof (response.data) !== 'undefined') {
                    let target_devices = response.data
                    // console.log('PlanDetailView: getTargetDevices: target_devices: ', target_devices)
                    target_devices.forEach(tdev => storedTargetDevices.push(tdev))
                }
            }
            // console.log('PlanDetailView: getTargetDevices: storedTargetDevices: ', storedTargetDevices)
            this.$store.dispatch('storeTargetDevices', storedTargetDevices)
        },
        createItems() {
            this.items = []
            this.storedDevices.forEach(dev => {
                let item = { ...dev }
                item.target_channels = []
                // console.log('TargetDeviceCard: createItems: storedTargetDevices:', this.storedTargetDevices)
                this.storedTargetChannels.forEach(tch => {
                    // console.log('TargetDeviceCard: createItems: tch:', tch)
                    let found_target_device = this.storedTargetDevices.find(tdev => tdev.device === dev.id && tdev.target_channel === tch.id)
                    if (found_target_device) {
                        // console.log('TargetDeviceCard: createItems: found tdev:', found_target_device)
                        item.target_channels.push({
                            target_channel_id: tch.id,
                            auto_allocate: found_target_device.auto_allocate,
                            budget: found_target_device.budget
                        })
                    } else {
                        // console.log('TargetDeviceCard: createItems: did not find dev/tch:', dev, tch)
                        item.target_channels.push({
                            target_channel_id: tch.id,
                            auto_allocate: false,
                            budget: ''
                        })
                    }
                })
                this.items.push(item)
            })
            // console.log('TargetDeviceCard: createItems: items:', this.items)
        },
        async createHeaders() {
            this.headerRow = []
            let device = {
                text: 'Device',
                align: 'start',
                sortable: false,
                value: 'code',
                class: "black--text text-subtitle-1",
                width: "50px",
            }
            this.headerRow.push(device)
            if (this.storedTargetChannels.length > 0) {
                for (const target_channel of this.storedTargetChannels) {
                    // Get the country details to display
                    await this.getTargetCountry(target_channel.target_country)

                    // Create a header for each country - where we'll place a checkbox 
                    var channel = {
                        text: this.target_country.code + '/' + target_channel.code,
                        align: 'start',
                        sortable: false,
                        value: "auto_allocate",
                        class: "black--text text-subtitle-1",
                        width: "50px",
                    }
                    this.headerRow.push(channel)

                    // Create a header for each channel budget - where we'll place a budget field
                    var budget = {
                        text: 'Budget',
                        align: 'center',
                        sortable: false,
                        value: "budget",
                        class: "black--text text-subtitle-1",
                        width: "150px",
                    }
                    this.headerRow.push(budget)
                }
            } else {
                // Create a header indicating no channels have been selected
                var no_countries_channels_selected = {
                    text: 'No Target Countries/Channels Selected',
                    align: 'start',
                    sortable: false,
                    value: "auto_allocate",
                    class: "black--text text-subtitle-1",
                    width: "50px",
                }
                this.headerRow.push(no_countries_channels_selected)
            }
        },
        save() {
            let newTargetDeviceObjects = []
            this.items.map(i => {
                // console.log(i)
                i.target_channels.map(tch => {
                    if (tch.auto_allocate) {
                        let obj = {
                            device: i.id,
                            target_channel: tch.target_channel_id,
                            code: i.code,
                            name: i.name,
                            auto_allocate: tch.auto_allocate,
                            budget: tch.budget,
                            budget_allocated: 0,
                        }
                        newTargetDeviceObjects.push(obj)
                    }
                })
            })
            // console.log('newTargetDeviceObjects:', newTargetDeviceObjects)

            // Which countries has the user deleted?
            var deleteTargetDeviceIds = this.diffArray(newTargetDeviceObjects)
            // console.log('deleteTargetDeviceIds:', deleteTargetDeviceIds)
            this.$emit('update-target-devices', newTargetDeviceObjects, deleteTargetDeviceIds)
            this.locked = true
        },
        diffArray(newTargetDeviceObjects) {
            function diff(newTargetDeviceObjects, current_tdev) {
                for (let newItem of newTargetDeviceObjects) {
                    if (newItem.target_channel_id === current_tdev.target_channel_id && newItem.device === current_tdev.device) {
                        return true
                    }
                }
                return false
            }
            let deleteTargetDeviceIds = []
            this.storedTargetDevices.forEach(current_tdev => {
                if (!diff(newTargetDeviceObjects, current_tdev)) {
                    deleteTargetDeviceIds.push(current_tdev)
                }
            })
            return deleteTargetDeviceIds
        },
        cancel() {
            this.locked = true
            this.createItems()
        },
        includeChange(item, itemIndex, country, countryIndex) {
            !country.auto_allocate ? country.budget = '' : null
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