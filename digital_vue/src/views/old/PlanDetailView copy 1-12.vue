<template>
    <div>
        <v-row
            class="ma-0 white d-flex align-center">
            <v-col
                class="ma-0 pa-0 black--text"
                cols="auto">
                <v-tooltip
                    bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            class="ml-2"
                            icon
                            v-bind="attrs"
                            v-on="on">
                            <v-icon
                                @click="$router.push('/')"
                                color="primary"
                                size="50">mdi-clipboard-list-outline</v-icon>
                        </v-btn>
                    </template>
                    <span>Plans home</span>
                </v-tooltip>
            </v-col>

            <v-col cols="11" class="pa-0 black--text">

                <v-row class="ml-2 my-1 d-flex align-center">
                    {{ selectedPlan.name }}
                    <v-spacer></v-spacer>
                    <v-chip small outlined class="primary black mr-2">
                        <v-icon small class="black--text">mdi-alpha-p-circle-outline</v-icon>
                        {{ selectedPlan.phases.length }}
                    </v-chip>
                    <v-chip small outlined class=" primary ml-1 black mr-2">
                        <v-icon small class="black--text">mdi-alpha-s-circle-outline</v-icon>
                        {{ planNumberStrategies }}
                    </v-chip>
                    <div class="text-caption">
                        <span>Last edit:{{ new Date(selectedPlan.date_modified).toLocaleDateString(("en-GB")) }}</span>
                        <span> {{ new Date(selectedPlan.date_modified).toLocaleTimeString(("en-GB")) }}</span>
                    </div>
                </v-row>

                <v-row class="ml-2 my-1">{{ selectedPhase.name }} : {{ selectedStrategy.name }}</v-row>

                <v-row class="ma-0">
                    <v-col cols="auto" class="pa-0">
                        <v-toolbar dense flat>
                            <PhaseMenu
                                @open-phase-card='openPhaseCard'
                                @open-createphase-dialog="showNewPhaseDialog = true" />
                        </v-toolbar>
                    </v-col>
                    <v-col cols="auto" class="pa-0">
                        <v-toolbar dense flat>
                            <StrategyMenu
                                @open-strategy-card='openStrategyCard'
                                @open-createstrategy-dialog="showNewStrategyDialog = true" />
                        </v-toolbar>
                    </v-col>
                </v-row>

            </v-col>
        </v-row>

        <v-divider></v-divider>

        <PhaseCard
            v-if="showPhase"
            @hide="showPhase = false"
            @copy="copyPhase"
            @update="updatePhase"
            @delete="deletePhase" />
        <PhaseNewDialog
            v-model="showNewPhaseDialog"
            :phase="newPhaseStrategyData"
            @create-phase="createPhase" />

        <StrategyCard
            v-if="showStrategy"
            @hide="showStrategy = false"
            @copy="copyStrategy"
            @update="updateStrategy"
            @delete="deleteStrategy" />
        <StrategyNewDialog
            v-model="showNewStrategyDialog"
            :strategy="initialStrategy"
            @create-strategy="createStrategy" />

    </div>
</template>
<script>
import PhaseMenu from '@/components/phase/PhaseMenu'
import PhaseCard from '@/components/phase/PhaseCard'
import PhaseNewDialog from '@/components/dialogs/PhaseNewDialog'
import StrategyMenu from '@/components/strategy/StrategyMenu'
import StrategyCard from '@/components/strategy/StrategyCard'
import StrategyNewDialog from '@/components/dialogs/StrategyNewDialog'
import axios from 'axios'

export default {
    name: 'PlanDetailView',
    components: {
        PhaseMenu,
        PhaseCard,
        PhaseNewDialog,
        StrategyMenu,
        StrategyCard,
        StrategyNewDialog,
    },
    data() {
        return {
            showPhase: false,
            showNewPhaseDialog: false,
            showStrategy: false,
            showNewStrategyDialog: false,
            newPhase: {
                name: '',
                description: '',
                start_date: new Date().toISOString().substring(0, 10),
                end_date: new Date().toISOString().substring(0, 10),
                budget: 0,
                budget_allocated: 0,
                auto_allocate: false,
            },
            initialStrategy: {
                name: 'Strategy name',
                description: 'Strategy description',
                start_date: new Date().toISOString().substring(0, 10),
                end_date: new Date().toISOString().substring(0, 10),
                budget: 0,
                budget_allocated: 0,
                auto_allocate: false,
            },
        }
    },
    computed: {
        newPhaseStrategyData: {
            get() {
                this.newPhase.strategies = [this.initialStrategy]
                return this.newPhase
            }
        },
        selectedPlan: {
            get() {
                return this.$store.state.selectedPlan
            }
        },
        selectedPhase: {
            get() {
                return this.$store.state.selectedPhaseData.phase
            }
        },
        selectedPhaseIndex: {
            get() {
                return this.$store.state.selectedPhaseData.index
            }
        },
        selectedStrategy: {
            get() {
                return this.$store.state.selectedStrategyData.strategy
            }
        },
        selectedStrategyIndex: {
            get() {
                return this.$store.state.selectedStrategyData.index
            }
        },
        planNumberStrategies: {
            get() {
                let count = 0;
                this.selectedPlan.phases.forEach((phase) => {
                    phase.strategies.forEach((strategy) => {
                        count++
                    });
                })
                console.log(count)
                return count;
            }
        },
    },
    methods: {
        openPhaseCard(phase, index) {
            // Show Phase Card
            this.showPhase = true

            // Update selected Phase
            const phaseDataPayload = { phase: phase, index: index }
            this.$store.dispatch('selectPhaseData', phaseDataPayload)

            // Update selected Strategy
            const strategyDataPayload = { strategy: this.selectedPhase.strategies[0], index: 0 }
            this.$store.dispatch('selectStrategyData', strategyDataPayload)
        },
        openStrategyCard(strategy, index) {
            // Show Phase Card
            this.showStrategy = true

            // Update selected Strategy
            const strategyDataPayload = { strategy: strategy, index: index }
            this.$store.dispatch('selectStrategyData', strategyDataPayload)
        },
        async getPlan() {
            console.log('getplan: ', this.selectedPlan)
            var response = ''
            try {
                response = await axios.get(`/api/v1/plan/${this.selectedPlan.id}`)
            }
            catch (error) {
                console.log(error)
            }
            this.$store.dispatch('selectPlan', response.data)
        },
        copyPhase() {
            let newPhase = this.selectedPhase
            newPhase.name = newPhase.name + ' - copy'
            this.createPhase(newPhase)
        },
        async updatePhase() {
            this.selectedPhase.plan = this.selectedPlan.id

            var response = ''
            try {
                response = await axios.put(`api/v1/phase/${this.selectedPhase.id}/`, this.selectedPhase)
            }
            catch (error) {
                console.log(error)
            }
            // Refresh updated Plan and save phase to store, issue message aslert and change route to new tab
            this.endDBPhaseProcessing(this.selectedPhaseIndex, `Successfully updated Phase "${response.data.name}"`, 'success')
        },
        async createPhase(createPhase) {
            // Add current plan to new phase
            createPhase.plan = this.selectedPlan.id
            var response = ''
            try {
                response = await axios.post(`api/v1/phases/`, createPhase)
            }
            catch (error) {
                console.log(error)
            }
            // Refresh updated Plan and save phase to store, issue message aslert and change route to new tab
            this.endDBPhaseProcessing(0, `Successfully created Phase "${response.data.name}"`)
        },
        async deletePhase() {
            // A pLan must have at least one Phase
            if (this.selectedPlan.phases.length === 1) {
                // Display Snackbar message
                this.showSnackBar(`Unable to delete Phase "${this.selectedPhase.name}" - a Plan must have at least 1 Phase`, 'warning', 'black--text')
            } else {
                var response = ''
                try {
                    response = await axios.delete(`api/v1/phase/${this.selectedPhase.id}/`)
                }
                catch (error) {
                    console.log(error)
                }
                // Hide Phase Card after successsful delete
                this.showPhase = false

                // Refresh updated Plan and save phase to store, issue message aslert and change route to new tab
                this.endDBPhaseProcessing(0, `Succesfully deleted Phase "${this.selectedPhase.name}"`)
            }
        },
        async endDBPhaseProcessing(phaseIndex, message, alertType = 'success') {
            // Refresh updated Plan and save phase to store
            await this.getPlan()
            const phaseDataPayload = { phase: this.selectedPlan.phases[phaseIndex], index: phaseIndex }
            this.$store.dispatch('selectPhaseData', phaseDataPayload)

            // Display Snackbar message
            this.showSnackBar(message, alertType)
        },
        copyStrategy() {
            let newStrategy = this.selectedStrategy
            newStrategy.name = newStrategy.name + ' - copy'
            this.createStrategy(newStrategy)
        },
        async updateStrategy() {
            console.log('this.selectedStrategy: ', this.selectedStrategy)
            var response = ''
            try {
                response = await axios.put(`api/v1/strategy/${this.selectedStrategy.id}/`, this.selectedStrategy)
            }
            catch (error) {
                console.log(error)
            }
            // Refresh updated Plan and save strategy to store, issue message aslert and change route to new tab
            this.endDBStrategyProcessing(this.selectedStrategyIndex, `Successfully updated Strategy "${response.data.name}"`, 'success')
        },
        async createStrategy(createStrategy) {
            // Add current plan to new strategy
            createStrategy.phase = this.selectedPhase.id
            var response = ''
            try {
                response = await axios.post(`api/v1/strategies/`, createStrategy)
            }
            catch (error) {
                console.log(error)
            }
            // Refresh updated Plan and save strategy to store, issue message aslert and change route to new tab
            this.endDBStrategyProcessing(0, `Successfully created Strategy "${response.data.name}"`)
        },
        async deleteStrategy() {
            console.log('del strat: this.selectedStrategy')
            // A pLan must have at least one Strategy
            if (this.selectedPhase.strategies.length === 1) {
                // Display Snackbar message
                this.showSnackBar(`Unable to delete Strategy "${this.selectedStrategy.name}" - a Phase must have at least 1 Strategy`, 'warning', 'black--text')
            } else {
                var response = ''
                try {
                    response = await axios.delete(`api/v1/strategy/${this.selectedStrategy.id}/`)
                }
                catch (error) {
                    console.log(error)
                }

                // Hide Strategy Card after successsful delete
                this.showStrategy = false

                // Refresh updated Plan and save strategy to store, issue message aslert and change route to new tab
                this.endDBStrategyProcessing(0, `Succesfully deleted Strategy "${this.selectedStrategy.name}"`)
            }
        },
        async endDBStrategyProcessing(strategyIndex, message, alertType = 'success') {
            // Refresh updated Plan and save strategy to store
            await this.getPlan()

            // Refresh Stored Phase data
            const phaseDataPayload = { phase: this.selectedPlan.phases[this.selectedPhaseIndex], index: this.selectedPhaseIndex }
            this.$store.dispatch('selectPhaseData', phaseDataPayload)

            // Refresh Stored Strategy data
            const strategyDataPayload = { strategy: this.selectedPhase.strategies[strategyIndex], index: strategyIndex }
            console.log('endDBStrategyProcessing - strategyDataPayload:', strategyDataPayload)
            this.$store.dispatch('selectStrategyData', strategyDataPayload)
            console.log('endDBStrategyProcessing - selectedStratgey:', this.selectedStrategy)

            // Display Snackbar message
            this.showSnackBar(message, alertType)
        },
        showSnackBar(message, alertType, text_color = 'white--text') {
            const payload = { text: `${message}`, alerttype: alertType, contentclass: text_color }
            this.$store.dispatch('showSnackBar', payload)
        },
    }
}
</script>
<style>
div.v-toolbar__content {
    padding: 0px;
}
</style>