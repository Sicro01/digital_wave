<template>
    <div>
        <v-menu
            offset-y>
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                    @click="$emit('open-targetcountry-card')"
                    class="ml-3 pa-0 grey--text text-capitalize"
                    text
                    v-bind="attrs"
                    v-on="on">
                    <span>Linked Countries</span>
                </v-btn>
            </template>
        </v-menu>
    </div>
</template>
<script>
export default {
    name: 'TargetCountryMenu',
}
</script>