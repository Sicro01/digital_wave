<template>
    <v-form
        ref="form"
        v-model="valid">
        <v-card class="mt-3 mx-3">
            <v-card-title class="py-0">
                Select Countries and Set Budgets
                <v-spacer></v-spacer>
                <CardIcons
                    :showEditIcon="true"
                    :showHideIcon="true"
                    @edit="(locked = !locked)"
                    @hide="$emit('hide')"
                    cardType="Linked Countries" />
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
                                    <td>{{ item.country_name }}</td>

                                    <td class="d-flex justify-center align-center">
                                        <v-checkbox
                                            v-model="item.include"
                                            color="secondary"
                                            dense
                                            @change="includeChange(item)"
                                            :readonly="locked"></v-checkbox>
                                    </td>
                                    <td>
                                        <v-text-field
                                            :disabled="!item.include"
                                            :readonly="locked"
                                            v-model.number="item.budget"
                                            label="Strategy / Country Budget"
                                            :rules="item.include ? [rules.notEmpty, rules.inRange] : []"
                                            type="number"
                                            dense
                                            hide-details
                                            class="shrink rounded-0"
                                            outlined>
                                        </v-text-field>
                                    </td>
                                    <td class="d-flex justify-center align-center">
                                        <v-checkbox
                                            v-model="item.auto_allocate"
                                            :disabled="item.budget <= 0"
                                            :readonly="locked"
                                            dense
                                            color="secondary"></v-checkbox>
                                    </td>
                                </tr>
                            </tbody>
                        </template>
                    </v-data-table>
                </v-sheet>
                <div class="caption text--disabled">
                    <span>Last edit: {{ targetCountriesLastEdited }}</span>
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
    name: 'TargetCountryCard',
    components: {
        CardIcons,
    },
    data() {
        return {
            headers: [
                {
                    text: 'Country',
                    align: 'center',
                    sortable: false,
                    value: 'country_name',
                    class: "text-subtitle-1 black--text",
                },
                { text: 'Include?', align: 'center', value: 'include', class: "text-subtitle-1 black--text" },
                { text: 'Budget', align: 'center', value: 'budget', class: "text-subtitle-1 black--text", },
                { text: 'Auto-allocate?', align: 'center', value: 'autoallocate', class: "text-subtitle-1 black--text", },
            ],
            items: [],
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
        storedCountries: {
            get() {
                return this.$store.state.storedCountries
            }
        },
        targetCountriesLastEdited: {
            get() {
                if (this.storedTargetCountries.length > 0) {
                    let lastEditDate = new Date(Math.max(...this.storedTargetCountries.map(e => new Date(e.date_modified)))).toLocaleDateString('en-GB');
                    let lastEditTime = new Date(Math.max(...this.storedTargetCountries.map(e => new Date(e.date_modified)))).toLocaleTimeString('en-GB');
                    return `${lastEditDate} ${lastEditTime}`
                } else {
                    return 'N/A'
                }
            }
        },
    },
    watch: {
        async selectedStrategy(newValue) {
            await this.getTargetCountries()
            this.createItems()
        },
    },
    mounted() {
        this.createItems()
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
        createItems() {
            this.items = []
            // Table Data - check box AND budget field for each country
            var index = 0
            this.storedCountries.forEach((country) => {
                var item = {
                    'country_id': country.id,
                    'country_name': country.name,
                    'country_code': country.code,
                    'include': false,
                    'budget': '',
                    'auto_allocate': false,
                }
                // See if this country is already a target country
                let foundTargetCountry = this.storedTargetCountries.find(targetCountry =>
                    targetCountry.country == item.country_id
                )
                // Update table data item with target country settings
                if (foundTargetCountry) {
                    item.include = true
                    item.budget = foundTargetCountry.budget
                    item.budget_allocated = foundTargetCountry.budget_allocated
                    item.auto_allocate = foundTargetCountry.auto_allocate
                }
                this.items.push(item)
            })
        },
        save() {
            // Capture the country objects the user has picked
            var newTargetCountryObjects = this.items.filter(item => item.include).map(item => ({
                strategy: this.selectedStrategy.id,
                country: item.country_id,
                code: item.country_code,
                name: item.country_name,
                budget: item.budget,
                auto_allocate: item.auto_allocate,
                budget_allocated: 0,
            }))
            // Which countries has the user deleted?
            var deleteTargetCountryIds = this.diffArray()

            // Emit update
            this.$emit('update-target-countries', newTargetCountryObjects, deleteTargetCountryIds)

            /// Turn off edit mode
            this.locked = true
        },
        diffArray() {
            // Identify which target countries the user has deleted
            function diffArray(oldTargetCountryIds, newTargetCountryIds) {
                return [...diff(oldTargetCountryIds, newTargetCountryIds)];

                function diff(a, b) {
                    return a.filter(item => b.indexOf(item) === -1)
                }
            }
            // What user originally picked - just the country id's
            var oldTargetCountryIds = this.storedTargetCountries.map(c => c.country)

            // What user has now picked - just the country id's
            var newTargetCountryIds = this.items.filter(i => i.include).map(i => i.country_id)
            return diffArray(oldTargetCountryIds, newTargetCountryIds)
        },
        cancel() {
            this.locked = true
            this.createItems()
        },
        includeChange(item) {
            !item.include ? item.budget = '' : null
        },
    }
}
</script>