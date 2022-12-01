<template>
    <v-snackbar
        v-model="$store.state.snackbar.show"
        :color="$store.state.snackbar.alerttype"
        :content-class="$store.state.snackbar.contentclass"
        tile>
        {{ $store.state.snackbar.text }}
        <template v-slot:action="{ attrs }">
            <v-btn
                @click="$store.dispatch('hideSnackBar')"
                text
                :class="$store.state.snackbar.contentclass"
                v-bind="attrs">
                Close
            </v-btn>
        </template>
    </v-snackbar>
</template>

<script>
export default {
    name: 'SnackBar',
}
</script>
