<template>
    <v-form
        ref="form"
        v-model="valid">
        <v-dialog
            v-model="dialog"
            @click:outside="closeDialog()"
            @input="$emit('input', $event)">
            <v-card flat outlined class="mt-2 rounded-0">
                <v-card-title>
                    {{ isEdit ? "Edit Phase Details" : "Enter New Phase Details" }}
                </v-card-title>
                <v-card-title>
                    <v-row>
                        <v-col md="4" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="phase.name"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="Name"
                                dense
                                outlined>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="start_date"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="Start Date"
                                dense
                                outlined>
                                <template v-slot:append>
                                    <date-picker v-model="start_date" />
                                </template>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="end_date"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="End Date"
                                dense
                                outlined>
                                <template v-slot:append>
                                    <date-picker v-model="end_date" />
                                </template>
                            </v-text-field>
                        </v-col>
                    </v-row>
                </v-card-title>
                <v-card-text class="px-5">
                    <v-textarea
                        v-model="phase.description"
                        :rules="[rules.required]"
                        class="rounded-0"
                        label="Description"
                        dense
                        outlined>
                    </v-textarea>
                </v-card-text>
                <v-card-actions>
                    <v-btn
                        class="ml-2 error rounded-0 text-capitalize"
                        depressed
                        :disabled="!isEdit"
                        @click="delPhase">
                        Delete
                    </v-btn>

                    <ConfirmDialog ref="confirm" />

                    <v-spacer></v-spacer>
                    <v-btn
                        class="grey lighten-1 mr-3 rounded-0 text-capitalize"
                        light
                        depressed
                        @click="closeDialog">
                        Cancel
                    </v-btn>
                    <v-btn
                        class="mr-3 success rounded-0 text-capitalize"
                        depressed
                        :disabled="!valid"
                        @click="save">
                        Save
                    </v-btn>
                    <v-btn
                        class="mr-3 success rounded-0 text-capitalize"
                        depressed
                        :disabled="!valid">
                        Copy
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
    name: "PhaseEditDialog",
    props: {
        phase: Object,
        dialog: Boolean,
        isEdit: Boolean,
    },
    components: {
        ConfirmDialog,
        DatePicker,
    },
    computed: {
        start_date: {
            get() {
                return this.phase.start_date
            },
            set(val) {
                this.phase.start_date = val
            }
        },
        end_date: {
            get() {
                return this.phase.end_date
            },
            set(val) {
                this.phase.end_date = val
            }
        },
    },
    data() {
        return {
            // value: null,
            startDate: '',
            valid: false,
            rules: {
                required: value => !!value || "Required.",
            }
        }
    },
    methods: {
        save() {
            console.log('isEdit: ', this.isEdit)
            console.log('phase: ', this.phase)
            this.isEdit ? this.$emit("update-phase", this.phase) : this.$emit("create-phase", this.phase)
        },
        async delPhase() {
            if (await this.$refs.confirm.open("Confirm", "Are you sure you want to delete this record?")) {
                console.log('delete it')
                this.deletePhase();
            }
        },
        deletePhase() {
            console.log("Record deleted.")
            this.$emit("delete-phase", this.phase)
        },
        closeDialog() {
            if (!this.isEdit) this.$refs.form.reset()
            this.$emit("close-dialog");
        },
    },
    updated() {
        this.$refs.form.resetValidation();
    },
}
</script>