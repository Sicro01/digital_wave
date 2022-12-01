<template>
    <!-- gradient="to top right, rgba(19, 84, 122, .5), rgba(19, 84, 122, .8)" -->
    <!-- src="@/assets/entrepreneur.jpg" -->
    <v-card outlined tile>
        <v-img
            :src="selectedImage"
            min-height="290"
            class="d-flex fill-height justify-center text-center align-center text-h4 font-weight-bold white--text">
            {{ plan.name }}
        </v-img>
        <v-card-text>
            <v-textarea
                label="Description"
                class="rounded-0"
                outlined
                hide-details
                readonly
                :value=plan.description>
            </v-textarea>

        </v-card-text>
        <v-card-actions class="pb-2 justify-center">
            <v-btn
                class="px-10 primary rounded-0 text-capitalize"
                dark
                @click="openDialog()"
                depressed>
                <v-icon small class="mr-2">mdi-pencil</v-icon>
                Edit Plan
            </v-btn>
        </v-card-actions>

        <v-divider class="mx-8"></v-divider>
        <!-- :to="this.plan.phases[0].get_absolute_url" -->
        <v-card-actions class="pt-2 justify-center">
            <v-btn
                @click="$emit('view-details')"
                class="px-2 secondary darken-3 rounded-0 text-capitalize"
                depressed>
                <v-icon small class="mr-2">mdi-magnify-plus</v-icon>
                View Plan Details
            </v-btn>
        </v-card-actions>
    </v-card>
</template>
<script>
import PlanEditDialog from '@/components/dialogs/PlanEditDialog'

export default {
    name: 'PlanCard',
    props: {
        plan: Object,
        editId: Number,
    },
    components: {
        PlanEditDialog,
    },
    data() {
        return {
            toggleEditPlan: false,
            displayMenu: false,
            images: [
                'entrepreneur.jpg',
                'businessman.jpg',
                'social_media_1.jpg',
                'social_media_2.jpg',
                'social_media_3.jpg',
                'doors.jpg',
                'chess_2.jpg',
                'startup.jpg',
                'student.jpg',
            ],
            selectedImage: '',
        }
    },
    computed: {
        firstPhaseURL: {
            get() {
                console.log('url: ', this.plan.phases[0].get_absolute_url)
                return this.plan.phases[0].get_absolute_url
            }
        }
    },
    methods: {
        openDialog() {
            this.$emit("open-dialog");
        },
    },
    created() {
        const idx = Math.floor(Math.random() * this.images.length)
        this.selectedImage = this.images[idx]
    }
}
</script>
<style scoped>
.v-text-field--outlined>>>fieldset {
    border: 1px solid lightgray !important;
}
</style>