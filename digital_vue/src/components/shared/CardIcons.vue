<template>
    <div>
        <v-tooltip
            bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on">
                    <v-icon
                        v-blur
                        @click="$emit('edit')"
                        color="primary"
                        small>mdi-pencil</v-icon>
                </v-btn>
            </template>
            <span>Edit {{ cardType }}</span>
        </v-tooltip>

        <v-tooltip
            bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on">
                    <v-icon
                        v-blur
                        @click="$emit('delete')"
                        color="primary"
                        small>mdi-delete</v-icon>
                </v-btn>
            </template>
            <span>Delete {{ cardType }}</span>
        </v-tooltip>

        <v-tooltip
            bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on">
                    <v-icon
                        v-blur
                        @click="$emit('copy')"
                        color="primary"
                        small>mdi-content-copy</v-icon>
                </v-btn>
            </template>
            <span>Copy {{ cardType }}</span>
        </v-tooltip>

        <v-tooltip
            bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    icon
                    v-bind="attrs"
                    v-on="on">
                    <v-icon
                        v-blur
                        @click="$emit('hide')"
                        color="primary"
                        small>mdi-eye-off</v-icon>
                </v-btn>
            </template>
            <span>Hide {{ cardType }}</span>
        </v-tooltip>
    </div>
</template>
<script>
export default {
    name: 'CardIcons',
    props: {
        cardType: String,
    },
}
</script>