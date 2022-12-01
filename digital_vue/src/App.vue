<template>
  <v-app id="app" v-bind:style="{ backgroundColor: color }">
    <AppBar :drawer='drawer' @toggleDrawer="toggleDrawer" />
    <AppNavDrawer :drawer='drawer' />
    <v-main>
      <v-container fluid class="pa-0">
        <router-view />
        <SnackBar />
      </v-container>
    </v-main>
    <v-footer app padless absolute>
      <AppFooter />
    </v-footer>
  </v-app>
</template>

<script>
import AppBar from '@/components/layout/AppBar'
import AppNavDrawer from '@/components/layout/AppNavDrawer'
import AppFooter from '@/components/layout/AppFooter'
import SnackBar from '@/components/shared/SnackBar'

export default {
  name: 'App',
  components: {
    AppBar,
    AppNavDrawer,
    AppFooter,
    SnackBar,
  },
  data: () => ({
    drawer: false,
    color: '#eeeeee'
  }),
  methods: {
    toggleDrawer(drawerValue) {
      this.drawer = drawerValue
    }
  }
}
</script>
