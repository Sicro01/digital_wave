<template>
    <v-form
        ref="form"
        v-model="valid">
        <v-dialog v-model="show" persistent>
            <v-card flat outlined class=" mt-2 rounded-0">
                <v-card-title>Enter New Phase Details</v-card-title>
                <v-card-title>
                    <v-row>
                        <v-col md="4" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="newPhase.name"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="Name"
                                clearable
                                dense
                                outlined>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="newPhase.start_date"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="Start Date"
                                dense
                                outlined>
                                <template v-slot:append>
                                    <DatePicker v-model="newPhase.start_date" />
                                </template>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="newPhase.end_date"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="End Date"
                                dense
                                outlined>
                                <template v-slot:append>
                                    <DatePicker v-model="newPhase.end_date" />
                                </template>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="newPhase.budget"
                                :rules="[rules.notEmpty, rules.inRange]"
                                label="Budget"
                                dense
                                class="rounded-0"
                                outlined>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-checkbox
                                v-model="newPhase.auto_allocate"
                                :disabled="newPhase.budget <= 0"
                                label="Autoallocate?"
                                dense
                                color="secondary">
                            </v-checkbox>
                        </v-col>
                    </v-row>
                </v-card-title>
                <v-card-text class="px-5">
                    <v-textarea
                        v-model="newPhase.description"
                        :rules="[rules.required]"
                        class="rounded-0"
                        label="Description"
                        clearable
                        dense
                        outlined>
                    </v-textarea>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        class="grey lighten-1 mr-3 rounded-0 text-capitalize"
                        light
                        depressed
                        @click="show = false">
                        Cancel
                    </v-btn>
                    <v-btn
                        class="mr-3 success rounded-0 text-capitalize"
                        depressed
                        :disabled="!valid"
                        @click="save">
                        Save
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-form>
</template>

<script>
import DatePicker from '@/components/shared/DatePicker'

export default {
    name: 'PhaseEditDialog',
    components: {
        DatePicker,
    },
    props: {
        value: Boolean,
        phase: Object,
    },
    data() {
        return {
            valid: false,
            rules: {
                required: (v => !!v || "Required"),
                notEmpty: (v => (v.toString().length > 0) || "Budget should be between 0 and 10,000,000"),
                inRange: (v => (Number.isInteger(Number(v)) && v >= 0 && v <= 10000000) || "Budget should be between 0 and 10,000,000"),
            },
            newPhase: Object,
        }
    },
    watch: {
        value(val) {
            if (val) {
                console.log('phase: ', this.phase)
                this.newPhase = Object.assign({}, this.phase)
                this.$refs.form.resetValidation()
            }
        },
    },
    computed: {
        show: {
            get() {
                return this.value
            },
            set(value) {
                this.$emit('input', value)
            },
        },
    },
    methods: {
        save() {
            this.$emit("create-phase", this.newPhase)
            this.show = false
        },
    }
}
</script>