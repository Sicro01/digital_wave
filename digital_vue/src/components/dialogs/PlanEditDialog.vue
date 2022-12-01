<template>
    <v-form
        ref="form"
        v-model="valid">
        <v-dialog v-model="show" max-width="600" persistent>
            <v-card flat outlined class=" mt-2 rounded-0">
                <v-card-title>
                    {{ isEdit ? "Edit Plan Details" : "Enter New Plan Details" }}
                </v-card-title>
                <v-card-text>
                    <v-text-field
                        v-model="editPlan.name"
                        :rules="[rules.required]"
                        label="Name"
                        dense
                        class="rounded-0"
                        outlined>
                    </v-text-field>
                </v-card-text>
                <v-card-text>
                    <v-textarea
                        v-model="editPlan.description"
                        :rules="[rules.required]"
                        label="Description"
                        dense
                        class="rounded-0"
                        outlined>
                    </v-textarea>
                </v-card-text>
                <v-card-text>
                    <v-row>
                        <v-col md="4" sm="12">
                            <v-text-field
                                v-model.number="editPlan.budget"
                                :rules="[rules.notEmpty, rules.inRange]"
                                label="Budget"
                                type="number"
                                dense
                                class="rounded-0"
                                @input="checkAutoAllocate"
                                outlined>
                            </v-text-field>
                        </v-col>
                        <v-col md="4" sm="12"></v-col>
                        <v-col md="4" sm="12">
                            <v-checkbox
                                :disabled="editPlan.budget <= 0"
                                v-model="editPlan.auto_allocate"
                                label="Autoallocate Budget?"
                                dense
                                color="secondary">
                            </v-checkbox>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions>
                    <v-btn
                        class="ml-2 error rounded-0 text-capitalize"
                        depressed
                        v-if="isEdit"
                        :disabled="!isEdit"
                        @click="delPlan">
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

export default {
    name: 'PlanNewDialog',
    components: {
        ConfirmDialog,
    },
    props: {
        value: Boolean,
        plan: Object,
    },
    data() {
        return {
            valid: false,
            editPlan: {},
            // 
            rules: {
                required: (v => !!v || "Required"),
                notEmpty: (v => (v.toString().length > 0) || "Budget should be between 0 and 10,000,000"),
                inRange: (v => (Number.isInteger(Number(v)) && v >= 0 && v <= 10000000) || "Budget should be between 0 and 10,000,000"),
            },
        }
    },
    watch: {
        value(val) {
            if (val) {
                this.editPlan = Object.assign({}, this.plan)
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
                if (this.editPlan.id != -1)
                    return true
                else
                    return false
            }
        },
    },
    methods: {
        checkAutoAllocate() {
            // If user has entered budget, checked on auto-allocate then reset budget to 0 then we uncheck auto-allocate
            this.editPlan.budget === 0 ? this.editPlan.auto_allocate = false : null
        },
        save() {
            this.isEdit ? this.$emit("update-plan", this.editPlan) : this.$emit("create-plan", this.editPlan)
            this.show = false
        },
        async delPlan() {
            if (await this.$refs.confirm.open("Confirm", "Are you sure you want to delete this record?")) {
                console.log('delete it')
                this.deletePlan()
            }
        },
        deletePlan() {
            this.$emit("delete-plan", this.editPlan)
            this.show = false
        },
    }
}
</script>