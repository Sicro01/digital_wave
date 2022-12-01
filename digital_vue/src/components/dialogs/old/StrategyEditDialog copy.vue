<template>
    <v-form
        ref="form"
        v-model="valid">
        <v-dialog v-model="show" persistent>
            <v-card flat outlined class=" mt-2 rounded-0">
                <v-card-title>
                    {{ isEdit ? "Edit Strategy Details" : "Enter New Strategy Details" }}
                </v-card-title>
                <v-card-title>
                    <v-row>
                        <v-col md="4" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="editStrategy.name"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="Name"
                                dense
                                outlined>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="editStrategy.start_date"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="Start Date"
                                dense
                                outlined>
                                <template v-slot:append>
                                    <DatePicker v-model="editStrategy.start_date" />
                                </template>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="editStrategy.end_date"
                                :rules="[rules.required]"
                                class="rounded-0"
                                label="End Date"
                                dense
                                outlined>
                                <template v-slot:append>
                                    <DatePicker v-model="editStrategy.end_date" />
                                </template>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-text-field
                                v-model="editStrategy.budget"
                                :rules="[rules.required]"
                                label="Budget"
                                dense
                                class="rounded-0"
                                outlined>
                            </v-text-field>
                        </v-col>
                        <v-col md="2" sm="12" class="mt-3 px-2">
                            <v-checkbox
                                v-model="editStrategy.auto_allocate"
                                label="Autoallocate?"
                                dense
                                color="secondary">
                            </v-checkbox>
                        </v-col>
                    </v-row>
                </v-card-title>
                <v-card-text class="px-5">
                    <v-textarea
                        v-model="editStrategy.description"
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
                        v-if="isEdit"
                        :disabled="!isEdit"
                        @click="confirmDeleteStrategy">
                        Delete
                    </v-btn>
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
                    <v-btn
                        class="mr-3 success rounded-0 text-capitalize"
                        depressed
                        v-if="isEdit"
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
                required: value => !!value || "Required.",
            },
            editStrategy: Object,
        }
    },
    watch: {
        value(val) {
            if (val) {
                // Assign local strategy object with value of that passed in via prop
                this.editStrategy = Object.assign({}, this.strategy)
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
        isEdit: {
            get() {
                if (this.strategy.id > -1)
                    return true
                else
                    return false
            }
        },
    },
    methods: {
        save() {
            this.strategy.name != this.editStrategy.name ? this.changeRoute = true : this.changeRoute = false
            var payload = { strategy: this.editStrategy, changeRoute: this.changeRoute }
            this.isEdit ? this.$emit("update-strategy", payload) : this.$emit("create-strategy", this.editStrategy)
            this.show = false
        },
        async confirmDeleteStrategy() {
            if (await this.$refs.confirm.open("Confirm", "Are you sure you want to delete this record?")) {
                this.deleteStrategy()
            }
        },
        deleteStrategy() {
            this.$emit("delete-strategy", this.editStrategy)
            this.show = false
        },
    }
}
</script>