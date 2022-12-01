<template>
    <div>
        <v-card
            flat
            tile
            outlined
            class="mt-5 mx-3">
            <v-card-title class="pa-0">
                <v-toolbar
                    flat
                    dense
                    outlined
                    class="secondary darken-3 rounded-0 text-h3 white--text">
                    <v-spacer></v-spacer>
                    <v-toolbar-title class="ml-0">
                        <v-btn icon @click="prev">
                            <v-icon class="white--text">mdi-chevron-left</v-icon>
                        </v-btn>
                        <v-btn icon @click="next">
                            <v-icon class="white--text">mdi-chevron-right</v-icon>
                        </v-btn>
                    </v-toolbar-title>
                    <v-menu
                        left
                        offset-y>
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                dark
                                icon
                                v-bind="attrs"
                                v-on="on">
                                <v-icon>mdi-dots-vertical</v-icon>
                            </v-btn>
                        </template>
                        <v-list>
                            <v-list-item
                                v-for="(menuItem, i) in menuItems"
                                :key="i"
                                @click="menuActionClick(i)">
                                <v-btn text class="text-capitalize">{{ menuItem.text }}</v-btn>
                            </v-list-item>
                        </v-list>
                    </v-menu>
                </v-toolbar>
            </v-card-title>
            <v-card-text class="px-0">
                <v-row class="ma-0">
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h3 class="text-center">
                                {{ getMonthName(0) }}
                            </h3>
                            <v-calendar
                                :events="phaseEvents"
                                ref="calendar1"
                                type="month"
                                @click:event="showEvent"
                                :start="calendarStartDates[0]"
                                @change="calendar1Change">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h3 class="text-center">
                                {{ getMonthName(1) }}
                            </h3>
                            <v-calendar
                                :events="phaseEvents"
                                ref="calendar2"
                                type="month"
                                @click:event="showEvent"
                                :start="calendarStartDates[1]">
                            </v-calendar>
                        </div>
                    </v-col>
                </v-row>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn icon @click="prev">
                    <v-icon>mdi-chevron-left</v-icon>
                </v-btn>
                <v-btn icon @click="next">
                    <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
            </v-card-actions>
        </v-card>

        <PhaseEditDialog
            v-model="show"
            :phase="selectedPhase"
            @create="createPhase"
            @delete="deletePhase"
            @update="updatePhase" />
    </div>
</template>
<script>
import PhaseEditDialog from '@/components/dialogs/PhaseEditDialog'
import axios from 'axios'

export default {
    name: "PlanDetailCalendarView",
    components: {
        PhaseEditDialog
    },
    data() {
        return {
            show: false,
            editPhase: {},
            selectedEvent: {},
            selectedElement: null,
            selectedOpen: false,
            phaseEvents: [],
            focus: "",
            startDate: "2022-11-01",
            calendarStartDates: [],
            menuItems: [
                { text: "Add Phase", click() { this.$emit("open-dialog"); } },
                { text: "Hide/Show Phases", click() { this.$emit("show"); } },
            ],
        };
    },
    computed: {
        selectedPlan: {
            get() {
                return this.$store.state.selectedPlan;
            }
        },
        selectedPhase: {
            get() {
                return this.$store.state.selectedPhaseData.phase;
            }
        },
        selectedPhaseIndex: {
            get() {
                return this.$store.state.selectedPhaseData.index
            }
        },
    },
    mounted() {
        this.calcStartDates();
        this.loadEvents();
        let phaseDataPayload = { phase: this.selectedPlan.phases[0], index: 0 }
        this.$store.dispatch('selectPhaseData', phaseDataPayload)
    },
    methods: {
        loadEvents() {
            const events = [];
            let index = 0;
            this.selectedPlan.phases.forEach((phase) => {
                const eventObj = {
                    name: phase.name,
                    start: phase.start_date,
                    end: phase.end_date,
                    color: "green",
                    phase: phase,
                    index: index,
                };
                events.push(eventObj);
                index += 1;
            });
            this.phaseEvents = events;
            console.log("phaseEvents: ", this.phaseEvents);
        },
        calcStartDates() {
            var startDate = new Date(this.startDate);
            this.calendarStartDates = [];
            var n = 0;
            for (let i = 0; i < 6; i++) {
                this.calendarStartDates.push(new Date((startDate.setMonth(startDate.getMonth() + n))));
                n = 1;
            }
        },
        prev() {
            var startDate = new Date(this.startDate);
            this.startDate = new Date((startDate.setMonth(startDate.getMonth() - 1)));
            this.calcStartDates();
        },
        next() {
            var startDate = new Date(this.startDate);
            this.startDate = new Date((startDate.setMonth(startDate.getMonth() + 1)));
            this.calcStartDates();
        },
        showEvent({ nativeEvent, event }) {
            console.log(event.phase);
            console.log(event.index);
            const open = () => {
                let phaseDataPayload = { phase: event.phase, index: event.index }
                this.$store.dispatch('selectPhaseData', phaseDataPayload)
                this.selectedEvent = event;
                this.selectedElement = nativeEvent.target;
                requestAnimationFrame(() => requestAnimationFrame(() => this.show = true));
            };
            if (this.show) {
                this.show = false;
                requestAnimationFrame(() => requestAnimationFrame(() => open()));
            }
            else {
                open();
            }
            nativeEvent.stopPropagation();
        },
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
            this.endDBProcessing(this.selectedPhaseIndex, `Successfully updated Phase "${response.data.name}"`, 'success', updatePayload.changeRoute)
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
            this.endDBProcessing(0, `Successfully created Phase "${response.data.name}"`)
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
                this.endDBProcessing(0, `Succesfully deleted Phase "${this.selectedPhase.name}"`)
            }
        },
        async endDBProcessing(phaseIndex, message, alertType = 'success', changeRoute = true) {
            // Refresh updated Plan and save phase to store
            await this.getPlan()
            const phaseDataPayload = { phase: this.selectedPlan.phases[phaseIndex], index: phaseIndex }
            this.$store.dispatch('selectPhaseData', phaseDataPayload)

            // Display Snackbar message
            this.showSnackBar(message, alertType)

            // Change route to selected phase
            // changeRoute ? this.$router.push(this.selectedPhase.get_absolute_url) : ''
            this.loadEvents()
        },
        showSnackBar(message, alertType, text_color = 'white--text') {
            const payload = { text: `${message}`, alerttype: alertType, contentclass: text_color }
            this.$store.dispatch('showSnackBar', payload)
        },
        viewMore(event) {

        },
        getEventColor(event) {
            return event.color;
        },
        calendar1Change() {
            // console.log('firing cal1 change')
        },
        clickDate(event, x) {
        },
        getMonthName(index) {
            const date = new Date(this.calendarStartDates[index]);
            if (date.toString() !== "Invalid Date")
                return date.toLocaleString("en-us", { month: "long" });
            else
                return "December";
        },
        menuActionClick(index) {
            this.menuItems[index].click.call(this);
        }
    },
}
</script>
<!-- events: [
                {
                    name: 'Phase 1',
                    start: '2022-01-02',
                    end: '2022-05-04',
                    timed: false,
                    color: 'blue',
                },
                {
                    name: 'Event 2',
                    start: '2022-04-05',
                    end: '2022-04-07',
                },
                {
                    name: 'Event 3',
                    start: '2022-04-09T08:00:00',
                    end: '2022-04-09T10:00:00',
                    timed: true,
                },
            ], -->
  <!-- <v-menu
            v-model="selectedOpen"
            :close-on-content-click="false"
            :activator="selectedElement"
            offset-x>
            <v-card
                color="grey lighten-4"
                min-width="350px"
                flat>
                <v-toolbar
                    :color="selectedEvent.color"
                    dark>
                    <v-btn icon>
                        <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                    <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn icon>
                        <v-icon>mdi-heart</v-icon>
                    </v-btn>
                    <v-btn icon>
                        <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                </v-toolbar>
                <v-card-text>
                    <span v-html="selectedEvent.details"></span>
                </v-card-text>
                <v-card-actions>
                    <v-btn
                        text
                        color="secondary"
                        @click="selectedOpen = false">
                        Cancel
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-menu> -->