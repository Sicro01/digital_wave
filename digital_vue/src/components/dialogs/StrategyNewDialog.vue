<template>
    <v-form
        ref="form"
        v-model="valid">
        <v-dialog v-model="show" persistent>
            <v-card flat outlined class=" mt-2 rounded-0">
                <v-card-title>Enter New Strategy Details</v-card-title>
                <v-card-title>
                    <v-row>
                        <v-col md="4" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="newStrategy.name"
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
                                v-model="newStrategy.start_date"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="Start Date"
                                dense
                                outlined>
                                <template v-slot:append>
                                    <DatePicker v-model="newStrategy.start_date" />
                                </template>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="newStrategy.end_date"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="End Date"
                                dense
                                outlined>
                                <template v-slot:append>
                                    <DatePicker v-model="newStrategy.end_date" />
                                </template>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model.number="newStrategy.budget"
                                :rules="[rules.notEmpty, rules.inRange]"
                                label="Budget"
                                type="number"
                                dense
                                class="rounded-0"
                                outlined>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-checkbox
                                v-model="newStrategy.auto_allocate"
                                :disabled="newStrategy.budget <= 0"
                                label="Autoallocate?"
                                dense
                                color="secondary">
                            </v-checkbox>
                        </v-col>
                    </v-row>
                </v-card-title>
                <v-card-text class="px-5">
                    <v-textarea
                        v-model="newStrategy.description"
                        :rules="[rules.required]"
                        class="rounded-0"
                        label="Description"
                        clearable
                        dense
                        outlined>
                    </v-textarea>
                </v-card-text>

                <v-card-actions>

                    <ConfirmDialog ref="confirm" />
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
import ConfirmDialog from '@/components/dialogs/ConfirmDialog'
import DatePicker from '@/components/shared/DatePicker'

export default {
    name: 'StrategyEditDialog',
    components: {
        ConfirmDialog,
        DatePicker,
    },
    props: {
        value: Boolean,
        strategy: Object,
    },
    data() {
        return {
            changeRoute: false,
            valid: false,
            rules: {
                required: (v => !!v || "Required"),
                notEmpty: (v => (v.toString().length > 0) || "Budget should be between 0 and 10,000,000"),
                inRange: (v => (Number.isInteger(Number(v)) && v >= 0 && v <= 10000000) || "Budget should be between 0 and 10,000,000"),
            },
            newStrategy: Object,
        }
    },
    watch: {
        value(val) {
            if (val) {
                // Assign local strategy object with value of that passed in via prop
                this.newStrategy = Object.assign({}, this.strategy)
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
            this.$emit("create-strategy", this.newStrategy)
            this.show = false
        },
        async confirmDeleteStrategy() {
            if (await this.$refs.confirm.open("Confirm", "Are you sure you want to delete this record?")) {
                this.deleteStrategy()
            }
        },
        deleteStrategy() {
            this.$emit("delete-strategy", this.newStrategy)
            this.show = false
        },
    }
}
</script>