<template>
    <v-form
        ref="form"
        v-model="valid">
        <v-card
            class="mt-3 mx-3"
            flat
            tile
            outlined>
            <v-card-title class="py-0 pl-4 pr-2">Phase
                <v-spacer></v-spacer>

                <CardIcons cardType="Phase"
                    @edit="(locked = !locked)"
                    @delete="confirmDeletePhase"
                    @copy="$emit('copy')"
                    @hide="$emit('hide')" />

            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <v-row>
                    <v-col md="4" sm="12" class="mt-3 px-2">
                        <v-text-field
                            v-model="selectedPhase.name"
                            class="rounded-0"
                            :rules="[rules.required]"
                            label="Name"
                            :hide-details="locked"
                            :readonly="locked"
                            :clearable="!locked"
                            dense
                            outlined>
                        </v-text-field>
                    </v-col>
                    <v-col md="2" sm="12" class="mt-3 px-2">
                        <v-text-field
                            v-model="selectedPhase.start_date"
                            class="rounded-0"
                            :rules="[rules.required]"
                            label="Start Date"
                            :hide-details="locked"
                            :readonly="locked"
                            dense
                            outlined>
                            <template v-slot:append>
                                <DatePicker v-model="selectedPhase.start_date" :locked="locked" />
                            </template>
                        </v-text-field>
                    </v-col>
                    <v-col md="2" sm="12" class="mt-3 px-2">
                        <v-text-field
                            v-model="selectedPhase.end_date"
                            class="rounded-0"
                            :rules="[rules.required]"
                            label="End Date"
                            :hide-details="locked"
                            :readonly="locked"
                            dense
                            outlined>
                            <template v-slot:append>
                                <DatePicker v-model="selectedPhase.end_date" :locked="locked" />
                            </template>
                        </v-text-field>
                    </v-col>
                    <v-col md="2" sm="12" class="mt-3 px-2">
                        <v-text-field
                            v-model.number="selectedPhase.budget"
                            class="rounded-0"
                            label="Budget"
                            type="number"
                            :rules="[rules.notEmpty, rules.inRange]"
                            :hide-details="locked"
                            :readonly="locked"
                            dense
                            outlined>
                        </v-text-field>
                    </v-col>
                    <v-col md="2" sm="12" class="mt-3 px-2">
                        <v-checkbox
                            v-model="selectedPhase.auto_allocate"
                            label="Autoallocate?"
                            :disabled="selectedPhase.budget <= 0"
                            :hide-details="locked"
                            :readonly="locked"
                            dense
                            color="secondary">
                        </v-checkbox>
                    </v-col>
                </v-row>
            </v-card-text>
            <v-card-text class="py-1">
                <v-row>
                    <v-col md="12" sm="12" class="pb-6 px-2">
                        <v-textarea
                            v-model="selectedPhase.description"
                            class="rounded-0"
                            label="Description"
                            :rules="[rules.required]"
                            :hide-details="locked"
                            :readonly="locked"
                            :clearable="!locked"
                            dense
                            outlined>
                        </v-textarea>
                    </v-col>
                </v-row>
                <div class="caption">
                    <span>Last edit:{{ new Date(selectedPhase.date_modified).toLocaleDateString(("en-GB")) }}</span>
                    <span> {{ new Date(selectedPhase.date_modified).toLocaleTimeString(("en-GB")) }}</span>
                </div>
            </v-card-text>
            <v-card-actions v-if="!locked">
                <v-spacer></v-spacer>
                <v-btn
                    class="grey lighten-1 mr-3 rounded-0 text-capitalize"
                    light
                    depressed
                    @click="locked = true">
                    Cancel
                </v-btn>
                <v-btn
                    class="mr-1 success rounded-0 text-capitalize"
                    depressed
                    :disabled="!valid"
                    @click="savePhase">
                    Save
                </v-btn>
            </v-card-actions>
        </v-card>

        <ConfirmDialog ref="confirm" />

    </v-form>
</template>
<script>
import CardIcons from '@/components/shared/CardIcons'
import ConfirmDialog from '@/components/dialogs/ConfirmDialog'
import DatePicker from '@/components/shared/DatePicker'

export default {
    name: 'PhaseCard',
    components: {
        CardIcons,
        ConfirmDialog,
        DatePicker,
    },
    data() {
        return {
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
                console.log('selectedPhase:', this.$store.state.selectedPhaseData.phase)
                return this.$store.state.selectedPhaseData.phase
            }
        },
        selectedPhaseIndex: {
            get() {
                return this.$store.state.selectedPhaseData.index
            }
        },
    },
    methods: {
        savePhase() {
            this.locked = true
            this.$emit('update', this.selectedPhase)
        },
        async confirmDeletePhase() {
            if (await this.$refs.confirm.open("Confirm", "Are you sure you want to delete this record?")) {
                this.$emit("delete", this.selectedPhase)
            }
        },
    },
}
</script>