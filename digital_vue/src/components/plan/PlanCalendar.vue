<template>
    <v-sheet
        class="mb-2 secondary mt-1 elevation-0"
        outlined>
        <v-card
            flat
            tile>
            <v-card-title class="py-1 grey lighten-1">
                <v-row dense class="mt-1 align-center">
                    <v-col cols="2" class="justify-start">
                        <v-text-field
                            v-if="showPlanCalendar"
                            v-model="startDate"
                            hide-details
                            class="rounded-0"
                            label="Start Date"
                            dense
                            outlined>
                            <template v-slot:append>
                                <DatePicker v-model="startDate" />
                            </template>
                        </v-text-field>
                    </v-col>
                    <v-col cols="1">
                        <v-btn v-if="showPlanCalendar" @click="prev" icon>
                            <v-icon class="black--text">mdi-chevron-left</v-icon>
                        </v-btn>
                        <v-btn v-if="showPlanCalendar" @click="next" icon>
                            <v-icon class="black--text">mdi-chevron-right</v-icon>
                        </v-btn>
                    </v-col>
                    <v-col cols="6" class="d-flex justify-center">
                        <span>{{ selectedPlan.name }} : Phases and Strategies Calendar</span>
                    </v-col>
                    <v-col cols="3" class="d-flex justify-end">
                        <!-- <v-chip @click="openNewPhaseDialog" outlined class="secondary mr-2">
                            <v-icon class="black--text">mdi-plus</v-icon>
                            <v-icon class="black--text">mdi-alpha-p-circle-outline</v-icon>
                        </v-chip>
                        <v-chip @click="openNewPhaseDialog" outlined class="secondary mr-2">
                            <v-icon class="black--text">mdi-plus</v-icon>
                            <v-icon class="black--text">mdi-alpha-s-circle-outline</v-icon>
                        </v-chip> -->
                        <v-btn @click="togglePlanCalendar" icon>
                            <v-icon v-if="showPlanCalendar" class="black--text">mdi-eye-outline</v-icon>
                            <v-icon v-else class="black--text">mdi-eye-off-outline</v-icon>
                        </v-btn>
                    </v-col>
                </v-row>
            </v-card-title>
            <v-divider></v-divider>
            <div v-if="showPlanCalendar">
                <v-row class="mt-1 mx-1">
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(0) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[0]"
                                @click:event="showEvent"
                                @change="calendar1Change"
                                ref="calendar0"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(1) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[1]"
                                @click:event="showEvent"
                                ref="calendar1"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(2) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[2]"
                                @click:event="showEvent"
                                ref="calendar2"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(3) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[3]"
                                @click:event="showEvent"
                                ref="calendar3"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(4) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[4]"
                                @click:event="showEvent"
                                ref="calendar4"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(5) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[5]"
                                @click:event="showEvent"
                                ref="calendar5"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                </v-row>
                <v-row class="mt-1 mx-1">
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(6) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[6]"
                                @click:event="showEvent"
                                @change="calendar1Change"
                                ref="calendar0"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(7) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[7]"
                                @click:event="showEvent"
                                ref="calendar1"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(8) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[8]"
                                @click:event="showEvent"
                                ref="calendar2"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(9) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[9]"
                                @click:event="showEvent"
                                ref="calendar3"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(10) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[10]"
                                @click:event="showEvent"
                                ref="calendar4"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                    <v-col lg="2" md="4" sm="12">
                        <div>
                            <h4 class="text-center">
                                {{ getMonthName(11) }}
                            </h4>
                            <v-calendar
                                :events="phaseEvents"
                                :start="calendarStartDates[11]"
                                @click:event="showEvent"
                                ref="calendar5"
                                type="month">
                            </v-calendar>
                        </div>
                    </v-col>
                </v-row>
                <v-card-actions>
                </v-card-actions>
            </div>
        </v-card>
    </v-sheet>
</template>
<script>
import PhaseEditDialog from '@/components/dialogs/PhaseEditDialog'
import DatePicker from '@/components/shared/DatePicker'

export default {
    name: "PlanDetailCalendarView",
    props: {
        showPlanCalendar: Boolean,
    },
    components: {
        PhaseEditDialog,
        DatePicker,
    },
    data() {
        return {
            selectedEvent: {},
            selectedElement: null,
            selectedOpen: false,
            phaseEvents: [],
            startDate: new Date().toISOString().slice(0, 10),
            calendarStartDates: [],
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
    watch: {
        selectedPlan() {
            this.loadEvents()
        },
        startDate() {
            this.calcStartDates()
            this.loadEvents()
        }
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
        },
        calcStartDates() {
            var _startDate = new Date(this.startDate)
            this.calendarStartDates = [];
            var n = 0;
            for (let i = 0; i < 12; i++) {
                this.calendarStartDates.push(new Date((_startDate.setMonth(_startDate.getMonth() + n))));
                n = 1;
            }
        },
        getMonthName(index) {
            const date = new Date(this.calendarStartDates[index]);
            var options = { year: "numeric", month: "long" };
            if (date.toString() !== "Invalid Date")
                return date.toLocaleString("en-us", options);
            else
                return "December";
        },
        prev() {
            var _startDate = new Date(this.startDate);
            _startDate = new Date((_startDate.setMonth(_startDate.getMonth() - 1)));
            this.startDate = _startDate.toISOString().slice(0, 10)
            this.calcStartDates();
        },
        next() {
            var _startDate = new Date(this.startDate);
            _startDate = new Date((_startDate.setMonth(_startDate.getMonth() + 1)));
            this.startDate = _startDate.toISOString().slice(0, 10)
            this.calcStartDates();
        },
        openNewPhaseDialog() {
            this.$emit("open-newphase-dialog")
        },
        togglePlanCalendar() {
            this.$store.dispatch('togglePlanCalendar')
        },
        showEvent({ nativeEvent, event }) {
            const open = () => {
                let phaseDataPayload = { phase: event.phase, index: event.index }
                this.$store.dispatch('selectPhaseData', phaseDataPayload)
                this.selectedEvent = event;
                this.selectedElement = nativeEvent.target;
                requestAnimationFrame(() => requestAnimationFrame(() => this.$emit("open-editphase-dialog", event.phase)));
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

    },
}
</script>