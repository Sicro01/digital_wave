<template>
    <div>
        <v-app-bar
            class=""
            app
            dark
            flat
            tile
            src="phone.jpg">
            <template v-slot:img="{ props }">
                <v-img
                    v-bind="props"
                    gradient="to top right, rgba(100,115,201,.7), rgba(25,32,72,.7)"></v-img>
            </template>
            <v-app-bar-nav-icon
                @click="openDrawer"
                v-click-outside="closeDrawer">
            </v-app-bar-nav-icon>
            <router-link to="/">
                <v-toolbar-title class="white--text text-uppercase">
                    <span class="font-weight-light">Digital</span>
                    <span>Wave</span>
                </v-toolbar-title>
            </router-link>
            <v-spacer></v-spacer>
            <v-btn
                v-if="$store.state.isAuthenticated"
                class="px-7 secondary darken-3 white--text text-capitalize"
                to="/my-account"
                depressed
                tile>My account
            </v-btn>
            <v-btn
                v-else
                class="mr-3 white--text text-capitalize"
                to="/log-in"
                depressed
                outlined
                tile>
                <v-icon small class="mr-3">mdi-login</v-icon>
                Log in
            </v-btn>
        </v-app-bar>
    </div>
</template>
<script>
export default {
    name: 'AppBar',
    props: ['drawer'],
    data() {
        return {
            searchClosed: true,
            drawerCopy: Boolean,
        }
    },
    methods: {
        openDrawer() {
            this.$emit('toggleDrawer', true)
        },
        closeDrawer() {
            this.$emit('toggleDrawer', false)
        }
    }
}
</script>