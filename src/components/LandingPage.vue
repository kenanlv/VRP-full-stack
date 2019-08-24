<template>
    <div id="landing">
        <img src="../assets/logo.svg">
        <div class="sign-in-group">
            <p class="sign-in-title">Sign In</p>
            <p class="sign-in-subtitle">Vehicle Routing System</p>
            <div class="sign-in-button-wrapper">
                <button @click="login" class="sign-in-button-google">
                    <p>Sign in with <i class="fab fa-google"></i></p>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "LandingPage",
        methods: {
            login: function () {
                window.location.replace('/login/')
            }
        }
    }
</script>

<style scoped>
    @import url('https://fonts.googleapis.com/css?family=Roboto&display=swap');

    #landing {
        display: block;
        font-family: 'Roboto', sans-serif;
        position: relative;
    }

    #landing img {
        margin: 54px;
    }

    .sign-in-group {
        position: absolute;
        bottom: 100px;
        height: auto !important;
        left: 54px;
    }

    .sign-in-group p {
        font-family: Roboto, sans-serif;
        margin-bottom: 2px;
        font-style: normal;
        font-weight: bold;
    }

    .sign-in-title {
        font-size: 50px;
        line-height: 59px;
        color: #FFFFFF;
    }

    .sign-in-subtitle {
        font-size: 18px;
        line-height: 21px;
        color: #444444;
    }

    .sign-in-button-google {
        bottom: 285px;
        background-color: #2C2C2C;
        width: 100%;
        height: 100%;
        border: 0;
    }

    .sign-in-button-google p, i {
        color: #FFFFFF;
        font-size: 24px;
    }

    .sign-in-button-wrapper {
        margin-top: 100px;
        background: linear-gradient(238deg, #678ADA, #173960 100%);
        width: 244px;
        height: 60px;
        padding: 6px;
    }
</style>