<template>
    <div>
        <v-row class="mx-2">
            <v-col cols="12">
                <PlanCalendar
                    :showPlanCalendar="showPlanCalendar" />
            </v-col>
        </v-row>
        <v-row class="mx-2">
            <v-col cols="12">
                <PhaseTabs
                    ref="parentPhaseTabs"
                    :showPhaseTabs="showPhaseTabs"
                    @open-newphase-dialog="openNewPhaseDialog"
                    @open-editphase-dialog="openEditPhaseDialog" />
            </v-col>
        </v-row>
        <v-row class="mx-2">
            <v-col cols="12">
                <StrategyTabs
                    :showStrategyTabs="showStrategyTabs"
                    @open-newstrategy-dialog="openNewStrategyDialog"
                    @open-editstrategy-dialog="openEditStrategyDialog"
                    @open-editcountry-dialog="openEditCountryDialog"
                    @open-editcountrychannel-dialog="openEditCountryChannelDialog" />
            </v-col>
        </v-row>

        <PhaseEditDialog
            v-model="showEditPhaseDialog"
            :phase="editPhase"
            @create-phase="createPhase"
            @update-phase="updatePhase"
            @delete-phase="deletePhase" />

        <StrategyEditDialog
            v-model="showEditStrategyDialog"
            :strategy="editStrategy"
            @create-strategy="createStrategy"
            @update-strategy="updateStrategy"
            @delete-strategy="deleteStrategy" />

        <CountryEditDialog
            v-model="showEditCountryDialog"
            :strategy="editStrategy"
            @update-strategy-country="prepCountryDataForUpdate" />

        <CountryChannelEditDialog
            v-model="showEditCountryChannelDialog"
            :strategy="editStrategy"
            @update-strategy-country-channel="prepCountryChannelDataForUpdate" />

    </div>
</template>
<script>
import PlanCalendar from '@/components/plan/PlanCalendar'
import PhaseTabs from '@/components/phase/PhaseTabs'
import PhaseEditDialog from '@/components/dialogs/PhaseEditDialog'
import StrategyTabs from '@/components/strategy/StrategyTabs'
import StrategyEditDialog from '@/components/dialogs/StrategyEditDialog'
import CountryEditDialog from '@/components/dialogs/CountryEditDialog'
import CountryChannelEditDialog from '@/components/dialogs/CountryChannelEditDialog'
import axios from 'axios'

export default {
    name: 'PlanDetailView',
    components: {
        PlanCalendar,
        PhaseTabs,
        PhaseEditDialog,
        StrategyTabs,
        StrategyEditDialog,
        CountryEditDialog,
        CountryChannelEditDialog,
    },
    data() {
        return {
            plan: '',
            editPhase: {},
            editStrategy: {},
            showEditPhaseDialog: false,
            showEditStrategyDialog: false,
            showEditCountryDialog: false,
            showEditCountryChannelDialog: false,
            newPhase: {
                name: '',
                description: '',
                start_date: new Date().toISOString().substring(0, 10),
                end_date: new Date().toISOString().substring(0, 10),
            },
            initialStrategy: {
                name: 'Strategy name',
                description: 'Strategy description',
                start_date: new Date().toISOString().substring(0, 10),
                end_date: new Date().toISOString().substring(0, 10),
            },
            newStrategy: {
                name: '',
                description: '',
                start_date: new Date().toISOString().substring(0, 10),
                end_date: new Date().toISOString().substring(0, 10),
                phase: '',
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
        showPlanCalendar: {
            get() {
                return this.$store.state.show.planCalendar
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
            },
        },
        showPhaseTabs: {
            get() {
                return this.$store.state.show.phaseTabs
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
        showStrategyTabs: {
            get() {
                return this.$store.state.show.strategyTabs
            }
        },
    },
    methods: {
        async getPlan() {
            var response = ''
            try {
                response = await axios.get(`/api/v1/plan/${this.selectedPlan.id}`)
            }
            catch (error) {
                console.log(error)
            }
            this.$store.dispatch('selectPlan', response.data)
        },
        async updatePhase(updatePayload) {
            updatePayload.phase.plan = this.selectedPlan.id
            var response = ''
            try {
                response = await axios.put(`api/v1/phase/${updatePayload.phase.id}/`, updatePayload.phase)
            }
            catch (error) {
                console.log(error)
            }
            // Refresh updated Plan and save phase to store, issue message aslert and change route to new tab
            this.endDBPhaseProcessing(this.selectedPhaseIndex, `Successfully updated Phase "${response.data.name}"`, 'success', updatePayload.changeRoute)
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
        async deletePhase(deletePhase) {
            // A pLan must have at least one Phase
            if (this.selectedPlan.phases.length === 1) {
                // Display Snackbar message
                this.showSnackBar(`Unable to delete Phase "${this.selectedPhase.name}" - a Plan must have at least 1 Phase`, 'warning', 'black--text')
            } else {
                var response = ''
                try {
                    response = await axios.delete(`api/v1/phase/${deletePhase.id}/`)
                }
                catch (error) {
                    console.log(error)
                }
                // Refresh updated Plan and save phase to store, issue message aslert and change route to new tab
                this.endDBPhaseProcessing(0, `Succesfully deleted Phase "${this.selectedPhase.name}"`)
            }
        },
        async endDBPhaseProcessing(phaseIndex, message, alertType = 'success', changeRoute = true) {
            // Refresh updated Plan and save phase to store
            await this.getPlan()
            const phaseDataPayload = { phase: this.selectedPlan.phases[phaseIndex], index: phaseIndex }
            this.$store.dispatch('selectPhaseData', phaseDataPayload)

            // Display Snackbar message
            this.showSnackBar(message, alertType)
            // this.selectedPhase.slug != this.$refs.phaseTabs.tab ? this.$refs.phaseTabs.callSlider() : null
            // console.log(this.selectedPhase.slug)
            console.log(this.$refs.parentPhaseTabs)
            // console.log(this.$refs.parentPhaseTabs.$refs.phaseTabs)
            // this.$refs.parentPhaseTabs.$refs.phaseTabs.callSlider()

            console.log('route: ', changeRoute)
            // Change route to selected phase
            changeRoute ? this.$router.push(this.selectedPhase.slug) : ''
            // changeRoute ? this.$refs.parentPhaseTabs.$refs.phaseTabs.callSlider() : null
        },
        openEditPhaseDialog(editPhase) {
            this.editPhase = editPhase
            this.showEditPhaseDialog = true
        },
        openNewPhaseDialog() {
            this.editPhase = this.newPhaseStrategyData
            this.showEditPhaseDialog = true
        },
        async updateStrategy(updatePayload) {
            // If no countries added add an empty array to keep the serializer happy
            if (!updatePayload.strategy.countries) {
                updatePayload.strategy.countries = []
            }
            console.log('updatePayload.strategy: ', updatePayload.strategy)
            var response = ''
            try {
                response = await axios.put(`api/v1/strategy/${updatePayload.strategy.id}/`, updatePayload.strategy)
            }
            catch (error) {
                console.log(error)
            }
            // Refresh updated Plan and save strategy to store, issue message aslert and change route to new tab
            this.endDBStrategyProcessing(this.selectedStrategyIndex, `Successfully updated Strategy "${response.data.name}"`, 'success',
                updatePayload.changeRoute)
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
        async deleteStrategy(deleteStrategy) {
            // A pLan must have at least one Strategy
            if (this.selectedPhase.strategies.length === 1) {
                // Display Snackbar message
                this.showSnackBar(`Unable to delete Strategy "${this.selectedStrategy.name}" - a Phase must have at least 1 Strategy`, 'warning', 'black--text')
            } else {
                var response = ''
                try {
                    response = await axios.delete(`api/v1/strategy/${deleteStrategy.id}/`)
                }
                catch (error) {
                    console.log(error)
                }
                // Refresh updated Plan and save strategy to store, issue message aslert and change route to new tab
                this.endDBStrategyProcessing(0, `Succesfully deleted Strategy "${this.selectedStrategy.name}"`)
            }
        },
        async endDBStrategyProcessing(strategyIndex, message, alertType = 'success', changeRoute = true) {
            // Refresh updated Plan and save strategy to store
            await this.getPlan()

            // Refresh Stored Phase data
            const phaseDataPayload = { phase: this.selectedPlan.phases[this.selectedPhaseIndex], index: this.selectedPhaseIndex }
            this.$store.dispatch('selectPhaseData', phaseDataPayload)

            // Refresh Stored Strategy data
            const strategyDataPayload = { strategy: this.selectedPhase.strategies[strategyIndex], index: strategyIndex }
            this.$store.dispatch('selectStrategyData', strategyDataPayload)
            console.log(this.selectedStrategy)
            // Display Snackbar message
            this.showSnackBar(message, alertType)

            // Change route to selected strategy
            changeRoute ? this.$router.push(this.selectedStrategy.get_absolute_url) : ''
        },
        openEditStrategyDialog(editStrategy) {
            this.editStrategy = editStrategy
            this.showEditStrategyDialog = true
        },
        openNewStrategyDialog() {
            this.editStrategy = this.newStrategy
            this.showEditStrategyDialog = true
        },
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
        openEditCountryDialog(editStrategy) {
            this.getCountries()
            this.editStrategy = editStrategy
            this.showEditCountryDialog = true
        },
        openEditCountryChannelDialog(editStrategy) {
            this.getCountries()
            this.getChannels()
            this.editStrategy = editStrategy
            this.showEditCountryChannelDialog = true
        },
        prepCountryDataForUpdate(strategy, countries) {
            console.log('prepCountryData: ', strategy, countries)
            this.selectedStrategy.countries = countries
            var updatePayload = {
                strategy: this.selectedStrategy,
                changeRoute: false
            }
            this.updateStrategy(updatePayload)
            this.showEditCountryChannelDialog = false
        },
        prepCountryChannelDataForUpdate(savePayload) {
            // console.log(savePayload)
            // Build array of countries
            var selectedCountries = []
            savePayload.countryChannelData.forEach((item) => {
                selectedCountries.push(item.countryId)
            })
            this.selectedStrategy.countries = selectedCountries
            var updatePayload = {
                strategy: this.selectedStrategy,
                changeRoute: false
            }
            this.updateStrategy(updatePayload)
            this.showEditCountryChannelDialog = false
            // selectedCountries.forEach((country) => {
            //     this.updateCountry(country)
            // })
            // this.updateCountry(updatePayload)
            // console.log(selectedCountries)
        },
        showSnackBar(message, alertType, text_color = 'white--text') {
            const payload = { text: `${message}`, alerttype: alertType, contentclass: text_color }
            this.$store.dispatch('showSnackBar', payload)
        },
        // async updateCountry(country) {
        //     var response = ''
        //     try {
        //         response = await axios.put(`api/v1/country/${country.id}/`, country)
        //     }
        //     catch (error) {
        //         console.log(error)
        //     }
        //     console.log('updated country: ', response.data)
        // Refresh updated Plan and save strategy to store, issue message aslert and change route to new tab
        // this.endDBStrategyProcessing(this.selectedStrategyIndex, `Successfully updated Strategy "${response.data.name}"`, 'success', updatePayload.changeRoute)
    },
}
</script>