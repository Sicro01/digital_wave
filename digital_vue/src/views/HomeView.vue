<template>
    <div>
        <v-row
            class="mt-2 primary--text font-weight-black text-h3">
            <v-col
                class="text-center"
                md="6"
                offset="3">
                <span>Plans</span>
            </v-col>
            <v-spacer></v-spacer>
            <v-col
                class="text-right"
                cols="2">
                <v-btn
                    class="mr-4 primary rounded-0 text-capitalize text-body-1"
                    dark
                    @click="openNewPlanDialog"
                    depressed>
                    <v-icon small class="mr-2">mdi-plus</v-icon>
                    New Plan
                </v-btn>
            </v-col>
        </v-row>
        <br />
        <br />
        <br />
        <v-row class="mb-0 mx-4">
            <v-col
                v-for="(plan, index) in plans" :key="plan.id"
                lg="3"
                md="4"
                sm=12
                class="px-3 py-0">
    
                <PlanCard
                    :plan="plan"
                    @open-dialog="openEditPlanDialog(plan)"
                    @view-details="viewPlanDetails(plan)" />
    
            </v-col>
        </v-row>
    
        <PlanEditDialog
            v-model="open_dialog"
            :plan="editPlan"
            @create-plan="createPlan"
            @update-plan="updatePlan"
            @delete-plan="deletePlan" />
    
    </div>
</template>
<script>
import PlanCard from '@/components/plan/PlanCard'
import PlanEditDialog from '@/components/dialogs/PlanEditDialog'
import axios from 'axios'

export default {
    name: 'HomeView',
    components: {
        PlanCard,
        PlanEditDialog,
    },
    data() {
        return {
            plans: [],
            editPlan: {},
            open_dialog: false,
            initialStrategy: {
                name: 'Strategy name',
                description: 'Strategy description',
                start_date: new Date().toISOString().substring(0, 10),
                end_date: new Date().toISOString().substring(0, 10),
                budget: 0,
                budget_allocated: 0,
                auto_allocated: false,
            },
            initialPhase: {
                name: 'Phase name',
                description: 'Phase description',
                start_date: new Date().toISOString().substring(0, 10),
                end_date: new Date().toISOString().substring(0, 10),
                budget: 0,
                budget_allocated: 0,
                auto_allocated: false,
            },
            initialPlan: {
                id: -1,
                name: '',
                description: '',
                budget: 0,
                auto_allocate: false,
            },
        }
    },
    computed: {
        newPlan: {
            get() {
                this.initialPhase.strategies = [this.initialStrategy]
                this.initialPlan.phases = [this.initialPhase]
                return this.initialPlan
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
    },
    mounted() {
        this.getPlans()
        document.title = 'Home | Digital Wave'
    },
    methods: {
        async getPlans() {
            var response = ''
            try {
                response = await axios.get('api/v1/plans/')
            }
            catch (error) {
                console.log(error)
            }
            if (response.data.length > 0) {
                this.plans = response.data
                console.log('plans: ', this.plans)
                this.$store.dispatch('selectPlan', this.plans[0])
            }
        },
        async getPlan(id) {
            var response = ''
            try {
                response = await axios.get(`/api/v1/plan/${id}`)
            }
            catch (error) {
                console.log(error)
            }
            this.$store.dispatch('selectPlan', response.data)
        },
        async updatePlan(updatePlan) {
            var response = ''
            // var planPayload = { name: updatePlan.name, description: updatePlan.description }
            try {
                response = await axios.patch(`api/v1/plan/${updatePlan.id}/`, updatePlan)
            }
            catch (error) {
                console.log(error)
            }
            this.getPlans()
            const payload = { text: `Successfully updated ${updatePlan.name}`, alerttype: "success", contentclass: 'white--text' }
            this.$store.dispatch('showSnackBar', payload)
        },
        async createPlan(createPlan) {
            console.log('createPlan', createPlan)
            // Auto allocate budget 
            var createPlan = this.autoAllocateBudget(createPlan)

            // Save plan to DB
            var response = ''
            console.log('createPlan: ', createPlan)
            try {
                response = await axios.post(`api/v1/plans/`, createPlan)
            }
            catch (error) {
                console.log(error)
            }
            this.getPlans()
            const payload = { text: `Successfully created ${createPlan.name} - Initial Phase Added`, alerttype: "success", contentclass: 'white--text' }
            this.$store.dispatch('showSnackBar', payload)
        },
        async deletePlan(deletePlan) {
            var response = ''
            try {
                response = await axios.delete(`api/v1/plan/${deletePlan.id}/`)
            }
            catch (error) {
                console.log(error)
            }
            this.getPlans()
            const payload = { text: `Successfully deleted ${deletePlan.name}`, alerttype: "success", contentclass: 'white--text' }
            this.$store.dispatch('showSnackBar', payload)
        },
        autoAllocateBudget(plan) {
            if (plan.auto_allocate)
                console.log('auto allocate budget into phase and strategy')
            return plan
        },
        openEditPlanDialog(editPlan) {
            this.editPlan = editPlan
            this.open_dialog = true
        },
        openNewPlanDialog() {
            console.log('newPlan:', this.newPlan)
            this.editPlan = this.newPlan
            this.open_dialog = true
        },
        viewPlanDetails(plan) {
            // Save the plan to the Store
            this.$store.dispatch('selectPlan', plan)

            // Save phase selection (the first one) to the Store
            var phasePayload = { phase: this.selectedPlan.phases[0], index: 0 }
            this.$store.dispatch('selectPhaseData', phasePayload)

            // Save strategy selection (the first one) to the Store
            var strategyPayload = { strategy: this.selectedPhase.strategies[0], index: 0 }
            this.$store.dispatch('selectStrategyData', strategyPayload)

            // Display the PlanDetailView
            document.title = this.selectedPlan.name + ' | Digital Wave'
            // this.$router.push(this.selectedPhase.get_absolute_url)
            this.$router.push('/plan')
        },
    }
}
</script>