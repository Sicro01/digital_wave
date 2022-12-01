<template>
    <div>
        <v-row
            class="mt-2 primary--text font-weight-black text-h3">
            <v-col md="6" offset="3" class="text-center">
                <span>Plans</span>
            </v-col>
            <v-spacer></v-spacer>
            <v-col cols="2" class="text-right">
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
                    @view-details="checkPlanPhases(plan)" />
    
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
import store from '@/store'

export default {
    name: 'HomeView',
    components: {
        PlanCard,
        PlanEditDialog,
    },
    data() {
        return {
            plans: [],
            open_dialog: false,
            newPlan: {
                id: -1,
                name: '',
                description: '',
            },
            editPlan: {
                id: 0,
                name: '',
                description: '',
            },
            initialPhase: {
                name: 'Phase name',
                description: 'Phase description',
                start_date: new Date().toISOString().substring(0, 10),
                end_date: new Date().toISOString().substring(0, 10),
            }
        }
    },
    mounted() {
        this.getPlans()
        document.title = 'Home | Digital Wave'
    },
    methods: {
        async getPlans() {
            await axios
                .get('api/v1/plans/')
                .then(response => {
                    this.plans = response.data
                    console.log('plan data:', this.plans)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        async updatePlan(updatePlan, newPhaseMessage) {
            var response = ''
            try {
                response = await axios.put(`api/v1/plans/${updatePlan.id}/`, updatePlan)
            }
            catch (error) {
                console.log(error)
            }

            const payload = { text: `Successfully updated ${updatePlan.name} ${newPhaseMessage}`, alerttype: "success", contentclass: 'white--text' }
            this.$store.dispatch('showSnackBar', payload)
            return response.data
        },
        async createPlan(createPlan) {
            var newPlan = {}
            newPlan = {
                name: createPlan.name,
                description: createPlan.description,
                phases: [this.initialPhase]
            }
            await axios
                .post(`api/v1/plans/`, newPlan)
                .catch(error => {
                    console.log(error)
                })
            this.getPlans()
            const payload = { text: `Successfully created ${newPlan.name} - Initial Phase Added`, alerttype: "success", contentclass: 'white--text' }
            this.$store.dispatch('showSnackBar', payload)
        },
        async deletePlan(deletePlan) {
            await axios
                .delete(`api/v1/plans/${deletePlan.id}/`)
                .catch(error => {
                    console.log(error)
                })
            this.getPlans()
            const payload = { text: `Successfully deleted ${deletePlan.name}`, alerttype: "success", contentclass: 'white--text' }
            this.$store.dispatch('showSnackBar', payload)
        },
        openEditPlanDialog(editPlan) {
            this.editPlan = editPlan
            this.open_dialog = true
        },
        openNewPlanDialog() {
            this.editPlan = this.newPlan
            this.open_dialog = true
        },
        checkPlanPhases(plan) {
            // If it's new plan OR user has deleted all phases then create a dummy phase and update the plan
            if (plan.phases.length === 0) {
                plan.phases.push(this.initialPhase)
                plan = this.updatePlan(plan, '- initial Phase added to Plan')
            }
            this.viewPlanDetails(plan)
        },
        viewPlanDetails(plan) {
            // Save the selected plan in the Store
            this.$store.dispatch('selectPlan', plan)
            const phaseDataPayload = { phase: plan.phases[0], index: 0 }
            this.$store.dispatch('selectPhaseData', phaseDataPayload)
            document.title = this.$store.state.selectedPlan.name + ' | Digital Wave'
            this.$router.push(this.$store.state.selectedPlan.phases[0].get_absolute_url)
        },
    }
}
</script>