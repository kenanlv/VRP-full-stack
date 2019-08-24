<template>
    <div class="edit-info">
        <v-app class="info-wrapper" dark>
            <h1 class="info-header">Your Information </h1>
            <v-form class="info-form">
                <v-container class="info-container">
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                    dark
                                    label="Full name"
                                    outlined
                                    placeholder="Your preferred name"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                    dark
                                    disabled
                                    label="Email address"
                                    outlined
                                    v-model="emailAddress"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                    dark
                                    label="Contact number"
                                    outlined
                                    placeholder="888-888-8888"
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12">
                            <v-autocomplete
                                    :items="predictions"
                                    :onchange="getPredictions"
                                    :search-input.sync="address"
                                    hide-no-data
                                    item-text="description"
                                    item-value="place_id"
                                    label="Address"
                                    outlined
                                    placeholder="Your current address"
                                    v-model="address_id"
                            ></v-autocomplete>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="6">
                            <v-select
                                    :items="yesNo"
                                    label="Are you a driver"
                                    outlined
                                    v-model="isDriver"
                            ></v-select>
                        </v-col>
                        <v-col cols="6">
                            <v-select
                                    :disabled="isDriver === 'No'"
                                    :items="capacities"
                                    label="Capacity of your car"
                                    outlined
                                    v-model="capacity"
                            ></v-select>
                        </v-col>
                    </v-row>
                </v-container>
            </v-form>
            <v-btn class="ma-2 info-btn" color="indigo"
                   to="/success"
            >Save and register
            </v-btn>
            <v-btn @click="logoff"
                   class="ma-2 info-btn"
            >Logoff
            </v-btn>
        </v-app>
    </div>
</template>

<script>
    import axios from 'axios'


    export default {
        name: "EditInfo",
        data: function () {
            return {
                capacities: [1, 2, 3, 4, 5],
                yesNo: ['Yes', 'No'],
                isDriver: 'No',
                capacity: 1,
                address: "",
                address_id: "",
                emailAddress: "haha@uw.edu",
                sessionToken: "",
                service: "",
                predictions: [],
                axiosConfig: {
                    headers: {Authorization: "bearer " + window.localStorage.getItem("AccessToken")}
                }
            }
        },
        methods: {
            logoff: function () {
                window.location.replace('/');
                window.localStorage.clear()
            }
        },
        watch: {
            address(val) {
                if (this.sessionToken === "") {
                    this.sessionToken = new google.maps.places.AutocompleteSessionToken();
                    this.service = new google.maps.places.AutocompleteService();
                }
                this.service.getPlacePredictions({
                    input: this.address,
                    sessionToken: this.sessionToken
                }, (prediction, status) => {
                    console.log(prediction);
                    this.predictions = prediction;
                })
            }
        },
        mounted() {
            axios.get('/api/info', this.axiosConfig)
                .then(response => {
                    console.log(response)
                })
        }
    }
</script>

<style>
    .edit-info {
        margin: 0 35px;
        font-family: Roboto, sans-serif;
    }

    h1.info-header {
        font-weight: bold;
        color: white;
        font-size: 50px;
        margin-bottom: 50px;
        margin-top: 50px;
    }

    .info-container {
        padding: 0;
    }

    .info-wrapper {
        background-color: #2C2C2C !important;
    }

    .col {
        padding: 0 12px;
    }

    .info-form {
        margin-bottom: 50px;
    }

    .v-text-field--outlined.v-input--is-disabled div div fieldset {
        border-style: dashed !important;
    }
</style>