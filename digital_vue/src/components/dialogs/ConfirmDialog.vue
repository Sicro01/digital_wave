<template>
    <v-dialog
        v-model="dialog"
        @click:outside="cancel"
        :max-width="options.width"
        :style="{ zIndex: options.zIndex }">
        <v-card>
            <v-toolbar
                dark
                :color="options.color"
                dense
                flat>
                <v-toolbar-title
                    class="body-2 font-weight-bold grey--text">
                    {{ title }}
                </v-toolbar-title>
            </v-toolbar>
            <v-card-text
                v-show="!!message"
                v-html="message"
                class="pa-4 black--text">
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    class="grey lighten-1 body-2 font-weight-bold rounded-0 text-capitalize"
                    outlined
                    @click="cancel">
                    Cancel
                </v-btn>
                <v-btn
                    class="error body-2 font-weight-bold rounded-0 text-capitalize"
                    dark
                    @click="agree">
                    Confirm Delete
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>
export default {
    data() {
        return {
            dialog: false,
            resolve: null,
            reject: null,
            message: null,
            title: null,
            options: {
                color: "grey lighten-3",
                width: 400,
                zIndex: 200,
                noconfirm: false,
            },
        }
    },
    methods: {
        open(title, message, options) {
            this.dialog = true;
            this.title = title;
            this.message = message;
            this.options = Object.assign(this.options, options)
            return new Promise((resolve, reject) => {
                this.resolve = resolve
                this.reject = reject
            });
        },
        agree() {
            this.resolve(true)
            this.dialog = false
        },
        cancel() {
            console.log('resolve false')
            this.resolve(false)
            this.dialog = false
        }
    }
}
</script>