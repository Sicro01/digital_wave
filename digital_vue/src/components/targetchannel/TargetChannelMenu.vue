<template>
    <div>
        <v-menu
            offset-y>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    @click="$emit('open-targetchannel-card')"
                    class="ml-3 pa-0 grey--text text-capitalize"
                    text
                    v-bind="attrs"
                    v-on="on">
                    <span>Linked Channels</span>
                </v-btn>
            </template>
        </v-menu>
    </div>
</template>
<script>
export default {
    name: 'TargetChannelMenu',
}
</script>