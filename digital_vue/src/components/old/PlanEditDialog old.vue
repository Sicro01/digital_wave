<template>
    <v-form
        ref="form"
        v-model="valid">
        <v-dialog
            v-model="dialog">
            <v-card flat outlined class=" mt-2 rounded-0">
                <v-card-title>
                    {{ isEdit ? "Edit Plan Details" : "Enter New Plan Details" }}
                </v-card-title>
                <v-card-text>
                    <v-text-field
                        :value="dialogPlan.name"
                        @input="$emit('input', $event)"
                        label="Name"
                        :rules="[rules.required]"
                        dense
                        class="rounded-0"
                        outlined>
                    </v-text-field>
                </v-card-text>
                <v-card-text>
                    <v-textarea
                        v-model="dialogPlan.description"
                        label="Description"
                        :rules="[rules.required]"
                        dense
                        class="rounded-0"
                        outlined>
                    </v-textarea>
                </v-card-text>
                <v-card-actions>
                    <v-btn
                        class="ml-2 error rounded-0 text-capitalize"
                        depressed
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
import ConfirmDialog from '@/components/dialogs/ConfirmDialog';

export default {
    name: "PlanEditDialog",
    components: {
        ConfirmDialog,
    },
    props: {
        dialogPlan: Object,
        dialog: Boolean,
        isEdit: Boolean,
    },
    watch: {
        dialog() {
            // if (this.dialog) this.$refs.form.resetValidation()
            console.log('dialog:', this.dialog)
            // console.log('event:', this.$event.target.value)
        }
    },
    data() {
        return {
            valid: false,
            rules: {
                required: value => !!value || "Required.",
            }
        }
    },
    methods: {
        save(value) {
            this.isEdit ? this.$emit("update-plan", this.dialogPlan) : this.$emit("create-plan", this.dialogPlan)
            this.$refs.form.reset();
        },
        async delPlan() {
            if (await this.$refs.confirm.open("Confirm", "Are you sure you want to delete this record?")) {
                console.log('delete it')
                this.deletePlan();
            }
        },
        deletePlan() {
            console.log("Record deleted.")
            this.$emit("delete-plan", this.dialogPlan)
            this.$refs.form.reset();
        },
        closeDialog() {
            if (!this.isEdit) this.$refs.form.reset()

            console.log('closeDialog PlanEditDialog:', this.dialogPlan)
            // this.$refs.form.reset();
        },
    }
}
</script>