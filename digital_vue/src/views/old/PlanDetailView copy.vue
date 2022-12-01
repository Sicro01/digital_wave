<template>
    <div>
        <v-row class="mt-3 mx-4">
            <v-col
                md="12"
                sm="12"
                class="align-center">

                <PhaseToolbar
                    :activeName="activeName"
                    :plan="plan"
                    @open-dialog="openNewDialog()"
                    @show="show = !show" />

                <v-card v-if="show">
                    <v-tabs
                        v-model="tab"
                        class="mt-3 elevation-0 rounded-0"
                        background-color="grey lighten-3"
                        center-active
                        show-arrows
                        slider-size=6>
                        <v-tabs-slider color="white"></v-tabs-slider>
                        <v-tab
                            v-for="phase in plan.phases"
                            :key="phase.id"
                            :href="'#' + phase.slug"
                            :to="`${phase.get_absolute_url}`"
                            @click="activeName = phase.name"
                            class="secondary darken-3 text-capitalize black--text font-weight-regular">
                            {{ phase.name }}
                        </v-tab>
                        <v-spacer></v-spacer>
                    </v-tabs>
                </v-card>

                <v-tabs-items
                    v-if="show"
                    v-model="tab">
                    <v-tab-item
                        v-for="(phase, index) in plan.phases"
                        :key="index"
                        :id="phase.get_absolute_url">
                        <router-view v-if="tab === phase.slug" />
                        <PhaseCard
                            :phase="phase"
                            @open-editphase-dialog="openEditDialog(phase)" />

                    </v-tab-item>
                </v-tabs-items>
            </v-col>
        </v-row>

        <PhaseEditDialog
            v-model="open_dialog"
            :phase="editPhase"
            @create="create"
            @update="update"
            @delete="del" />

    </div>
</template>
<script>
import PhaseCard from '@/components/phase/PhaseCard'
import PhaseToolbar from '@/components/phase/PhaseToolbar'
import PhaseEditDialog from '@/components/dialogs/PhaseEditDialog'
import axios from 'axios'

export default {
    name: 'PhaseDetailView',
    components: {
        PhaseCard,
        PhaseToolbar,
        PhaseEditDialog,
    },
    data() {
        return {
            menuItems: [
                { text: "Add Phase", click() { this.openNewDialog() } },
                { text: "Hide/Show Phases", click() { this.show = !this.show } },
            ],
            show: true,
            plan: '',
            isCreate: false,
            tab: '',
            activeName: '',
            isEdit: false,
            open_dialog: false,
            newPhase: {
                id: -1,
                name: '',
                description: '',
                start_date: new Date().toISOString().substring(0, 10),
                end_date: new Date().toISOString().substring(0, 10),
            },
            editPhase: {
                id: 0,
                name: '',
                description: '',
                start_date: '',
                end_date: '',
            },
        }
    },
    watch: {
        tab(newTabURL, oldTabURL) {
            // Set the name of the tab name variable to the first tab in the tablist when the tabs are first shown.
            // oldTabURL will be empty as there will be no previous tab
            if (!oldTabURL) { this.activeName = this.plan.phases[0].name }
        }
    },
    mounted() {
        this.getPlan()
    },
    methods: {
        async onTabClick(phase) {
            this.activeName = phase.name
        },
        async getPlan() {
            const plan_slug = this.$route.params.plan_slug
            await axios
                .get(`/api/v1/plan/${plan_slug}`)
                .then(response => {
                    this.plan = response.data
                    document.title = this.plan.name + ' | Digital Wave'
                })
                .catch(error => {
                    console.log(error)
                })

            if (this.isCreate) {
                this.$router.push(this.plan.phases[0].get_absolute_url)
                this.activeName = this.plan.phases[0].name
                this.isCreate = false
            }
        },
        async update(phase) {
            // Find phase by matching id and replace it with updated one
            this.plan.phases.forEach((item, index) => {
                if (item.id === phase.id) {
                    this.$set(this.plan.phases, index, phase)
                }
            })
            await axios
                .put(`api/v1/plans/${this.plan.id}/`, this.plan)
                .catch(error => {
                    console.log(error)
                })
            this.refreshData('Successfully updated', phase.name)
        },
        async create(phase) {
            // Using the plan update serializer which either updates a phase or create a new one if no phase id

            this.$delete(phase, 'id') // get rid of the plan's id field as we want to update the plan
            this.plan.phases.push(phase) // add the phase to the plan then update the plan

            await axios
                .put(`api/v1/plans/${this.plan.id}/`, this.plan)
                .catch(error => {
                    console.log(error)
                })
            this.isCreate = true
            this.refreshData('Successfully created', phase.name)
        },
        async del(phase) {
            await axios
                .delete(`api/v1/phases/${phase.id}/`)
                .catch(error => {
                    console.log(error)
                })
            this.refreshData('Successfully delete', phase.name)
        },
        refreshData(message, name) {
            this.getPlan()
            const payload = { text: `${message} ${name}`, alerttype: "success", contentclass: 'white--text' }
            this.$store.dispatch('showSnackBar', payload)
        },
        openEditDialog(editPhase) {
            this.editPhase = editPhase
            this.open_dialog = true
        },
        openNewDialog() {
            this.editPhase = this.newPhase
            this.open_dialog = true
        },
        menuActionClick(index) {
            this.menuItems[index].click.call(this)
        }
    }
}
</script>
<style scoped lang='scss'>
.v-tab--active {
    color: white !important;
}

.v-tab {
    text-transform: none !important;
}
</style>