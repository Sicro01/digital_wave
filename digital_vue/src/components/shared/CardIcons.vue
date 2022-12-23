<template>
    <div>
        <v-tooltip
            v-if="showEditIcon"
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
            v-if="showDeleteIcon"
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
            v-if="showCopyIcon"
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
            v-if="showHideIcon"
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
        cardType: {
            default: '',
            type: String
        },
        showEditIcon: {
            default: false,
            type: Boolean
        },
        showDeleteIcon: {
            default: false,
            type: Boolean
        },
        showCopyIcon: {
            default: false,
            type: Boolean
        },
        showHideIcon: {
            default: false,
            type: Boolean
        },
    },
}
</script>