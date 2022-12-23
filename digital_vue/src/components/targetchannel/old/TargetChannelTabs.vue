<template>
    <div>
        <v-tabs
            ref="tabs"
            v-model="tab"
            class="mt-1 rounded-0 "
            background-color="grey lighten-4"
            center-active
            show-arrows
            slider-size=6>
            <v-tabs-slider color="grey"></v-tabs-slider>
            <v-tab
                v-for="(target_country, index) in storedTargetCountries"
                :key="target_country.id"
                class="text-capitalize font-weight-regular">
                {{ target_country.name }}
            </v-tab>
            <v-spacer></v-spacer>
        </v-tabs>
        <v-tabs-items
            v-model="tab">
            <v-tab-item
                v-for="(target_country, index) in storedTargetCountries"
                :key="target_country.id">
                <TargetChannelTabCard />
            </v-tab-item>
        </v-tabs-items>

    </div>
</template>
<script>
import TargetChannelTabCard from '@/components/targetchannel/TargetChannelTabCard'
export default {
    name: 'TargetChannelTabs',
    components: {
        TargetChannelTabCard,
    },
    data() {
        return {
            tab: '',
        }
    },
    computed: {
        storedTargetCountries: {
            get() {
                return this.$store.state.storedTargetCountries
            }
        },
        storedTargetChannels: {
            get() {
                return this.$store.state.storedTargetChannels
            }
        },
        storedCountries: {
            get() {
                return this.$store.state.storedCountries
            }
        },
        storedChannels: {
            get() {
                return this.$store.state.storedChannels
            }
        },
    }
}
</script>
<style scoped lang='scss'>

.v-tab--active {
    color: white !important;
    font-weight: bolder;
}

.v-tab {
    text-transform: none !important;
}