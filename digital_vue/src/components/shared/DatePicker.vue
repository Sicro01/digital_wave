<template>
    <v-menu v-model="menu" offset-y :close-on-content-click="false" :disabled="locked">
        <template v-slot:activator="{ on }">
            <v-icon v-on="on" color="primary">mdi-calendar</v-icon>
        </template>
        <v-date-picker v-model="picker" @click="menu = false" />
    </v-menu>
</template>
<script>
export default {
    props: {
        value: {
            type: String,
        },
        locked: Boolean,
    },
    data() {
        return {
            menu: false,
        };
    },
    computed: {
        picker: {
            get() {
                return this.value
            },
            set(val) {
                this.menu = false;
                this.$emit("input", val);
            },
        },
    }
};
</script>