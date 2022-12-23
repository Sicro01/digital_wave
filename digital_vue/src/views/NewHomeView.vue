<template >
    <div>
        <!-- <v-container fluid class=" fill"> -->
        <v-row class="fill  d-flex justify-start">
            <v-col cols="auto" class="">
                <v-treeview
                    dense
                    v-model="selection"
                    color="secondary"
                    selected-color="green"
                    activatable
                    :item-text="name"
                    hoverable
                    :items="items">
                    <template v-slot:label="{ item }">
                        <a @click="onUpdate(item)">{{ item.node_type + ':' + item.name }}</a>
                    </template>
                </v-treeview>
            </v-col>
            <v-col cols="auto"><v-divider vertical class="grey"></v-divider></v-col>
            <v-col cols="auto" class="">
                <v-tabs
                    ref="tabs"
                    v-model="tab"
                    background-color="grey lighten-4"
                    center-active
                    show-arrows
                    slider-size=6>
                    <v-tabs-slider color="grey"></v-tabs-slider>
                    <v-tab
                        v-for="(node, index) in selectedNodes"
                        :key="node.id">
                        {{ node.name }}
                    </v-tab>
                </v-tabs>
                <v-tabs-items
                    v-model="tab">
                    <v-tab-item
                        v-for="(node, index) in selectedNodes"
                        :key="node.id">
                        {{ node.node_type }}
                        <PhaseCard
                            v-if="node.node_type == 'phase'"
                            @hide="(showPhase = false)"
                            @copy="copyPhase"
                            @update="updatePhase"
                            @delete="deletePhase" />
                    </v-tab-item>
                </v-tabs-items>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import PhaseCard from '@/components/phase/PhaseCard'
import axios from 'axios'

export default {
    name: 'NewHomeView',
    data() {
        return {
            tab: '',
            items: [],
            selectedNodes: [],
            selection: [],
        }
    },
    components: {
        PhaseCard,
    },
    computed: {
        plans: {
            get() {
                return this.$store.state.plans
            }
        },
        phases: {
            get() {
                return this.$store.state.phases
            }
        },
        strategies: {
            get() {
                return this.$store.state.strategies
            }
        },
    },
    // watch: {
    //     selection(to, from) {
    //         console.log('to:', to)
    //         console.log('from: ', from)
    //         console.log(this.selection)
    //     },
    // },
    async mounted() {
        await this.getPlans()
        await this.buildTreeData()
    },
    methods: {
        onUpdate(selection) {
            console.log('onUpdate: selection: ', selection)
            this.selectedNodes.push(selection)
        },
        buildTreeData() {
            var items = []
            var index = 1
            var item = {}
            this.plans.forEach((plan) => {
                item = { id: index, name: plan.name, database_id: plan.id, node_type: 'Plan', children: [] }
                plan.phases.forEach((phase) => {
                    index += 1
                    let this_phase = { id: index, name: phase.name, database_id: phase.id, node_type: 'Phase' }
                    item.children.push(this_phase)
                }); // Phases
            }); // Plans
            this.items.push(item)
            console.log('buildTreeData: ', this.items)
            return items
        }, // BuildTree
        async getPlans() {
            var response = ''
            try {
                response = await axios.get('api/v1/plans/')
            }
            catch (error) {
                console.log(error)
            }
            if (response.data.length > 0) {
                this.$store.dispatch('acquirePlans', response.data)
            }
        },
    }
}
</script>
<style scoped>
.fill {
    min-height: 87vh;
}
</style>
<!-- this.$store.dispatch('getStrategies', phase)
                    this.$store.strategies.forEach((strategy) => {
                        this.$store.dispatch('getTargetCountries', strategy)
                        this.$store.targetCountries.forEach((targetCountry) => {
                            this.$store.dispatch('getTargetChannels', targetCountry)
                            this.$store.targetChannels.forEach((targetChannel) => {
                                this.$store.dispatch('getTargetDevices', targetChannel)

                            }) // TargetChannels

                        }) // TargetCountries

                    }) // Strategies -->