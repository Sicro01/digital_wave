<template>
    <v-row>
        <v-col
            v-for="plan in plans"
            :key="plan.id"
            sm="6"
            md="3">
            <PlanCard :plan="plan" :active="isActive(plan)" @clicked="planClicked"></PlanCard>
        </v-col>
    </v-row>
</template>
<script>
import PlanCard from '@/components/PlanCard'
import axios from 'axios'

export default {
    name: 'PlanList',
    components: {
        PlanCard,
    },
    props: {
        plans: Array,
    },
    data() {
        return {
            selectedPlanId: null,
        }
    },
    methods: {
        planClicked(value) {
            this.selectedPlanId = value
        },
        isActive(plan) {
            if (plan.id === this.selectedPlanId) {
                return true
            }
            return false
        }
    }
}
</script>
<style lang="">
    
</style>