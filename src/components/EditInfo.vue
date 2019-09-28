<template>
    <div class="edit-info">
        <v-app class="info-wrapper" dark>
            <h1 class="info-header">Your Information </h1>
            <v-form class="info-form" ref="form" v-model="valid">
                <v-container class="info-container">
                    <v-row>
                        <v-col cols="12">
                            <v-text-field
                                    dark
                                    :rules="[v => !!v || 'Name is required']"
                                    label="Full name"
                                    outlined
                                    placeholder="Your preferred name"
                                    required
                                    v-model="name"
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
                                    :rules="contactRule"
                                    label="Contact number"
                                    outlined
                                    placeholder="888-888-8888"
                                    required
                                    v-model="contactNumber"
                                    validate-on-blur
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12">
                            <v-autocomplete
                                    :items="predictions"
                                    :search-input.sync="address"
                                    hide-no-data
                                    item-text="description"
                                    item-value="place_id"
                                    label="Address"
                                    outlined
                                    placeholder="Your current address"
                                    v-model="address_id"
                                    :rules="[v => !!v || 'Name is required']"
                                    required
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
                                    required
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
                   :disabled="!valid"
                   @click="updateInfo"
            >Save and register
            </v-btn>
            <v-btn @click="logoff"
                   class="ma-2 info-btn"
            >Logoff
            </v-btn>
            <v-snackbar
                    v-model="snackbar"
            >
                {{ error_msg }}
                <v-btn
                        color="pink"
                        text
                        @click="snackbar = false"
                >
                    Close
                </v-btn>
            </v-snackbar>
        </v-app>
    </div>
</template>

<script>
    import axios from 'axios'


    export default {
        name: "EditInfo",
        data: function () {
            return {
                valid: true,
                error_msg: "",
                snackbar: false,
                contactNumber: "",
                name: "",
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
                    headers: {Authorization: "Bearer " + window.localStorage.getItem("AccessToken")}
                },
                contactRule: [
                    v => /^\d+$/.test(v) || 'Number must contain only digits',
                    v => v.length === 10 || 'Number must be valid',
                ]
            }
        },
        methods: {
            logoff: function () {
                window.location.replace('/');
                window.localStorage.clear()
            },
            updateInfo: function () {
                axios.post('/api/info', {
                    name: this.name,
                    email: this.emailAddress,
                    is_driver: this.isDriver === "Yes" ? "True" : "False",
                    will_present: 'True',
                    phone_number: this.contactNumber,
                    address_id: this.address_id,
                    address_show_txt: this.address,
                    capacity: "" + this.capacity
                }, this.axiosConfig)
                    .then(() => {
                        this.$router.push('/success')
                    })
                    .catch((msg) => {
                        console.log(msg);
                        this.error_msg = msg.response.data;
                        this.snackbar = true;
                    })
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
            },
            contactNumber(val) {
                this.contactNumber = val.replace(/\D/g, '')
            }
        },
        mounted() {
            axios.get('/api/info', this.axiosConfig)
                .then(response => {
                    const data = response.data;
                    this.address_id = data.address_id === "None" ? "" : data.address_id;
                    this.contactNumber = parseInt(data.phone_number) === "None" ? "" : data.phone_number;
                    this.address = data.address_show_txt === "None" ? "" : data.address_show_txt;
                    this.capacity = parseInt(data.capacity);
                    this.emailAddress = data.email === "None" ? "" : data.email;
                    this.isDriver = data.is_driver === "False" ? "No" : "Yes";
                    this.name = data.name === "None" ? "" : data.name;
                    this.$refs.form.resetValidation();
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