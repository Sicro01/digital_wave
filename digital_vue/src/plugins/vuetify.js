import Vue from 'vue';
// import Vuetify from 'vuetify/lib/framework'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify);

const vuetify = new Vuetify({
    theme: {
        themes: {
            light: {
                primary: "#6200ee",
                secondary: "#03dac5",
                accent: "#03dac5",
                error: "#b00020",
                warning: "#ffde03",
                info: "#0336ff",
                success: "#00c853",
                background: "#ffffff",
            },
        },
        options: {
            customProperties: true
        },
    },
})

export default vuetify