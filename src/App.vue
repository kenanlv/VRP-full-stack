<template>
    <div id="app">
        <div id="left">
            <router-view></router-view>
        </div>
        <div id="background" class="flex-fill">
        </div>
    </div>
</template>

<script>
    export default {
        name: 'app'
    }
</script>

<style scoped>
    #app {
        display: flex;
    }

    #app div {
        height: 100vh;
    }

    #left {
        background: #2C2C2C;
        box-shadow: 20px 0 50px rgba(0, 0, 0, 0.3);
        z-index: 2;
    }
    
    @media only screen and (max-width: 550px) {
        #left {
            width: 100vw;
        }
    }

    @media only screen and (min-width: 550px) {
        #left {
            width: 430px;
        }
    }

    #background {
        background-image: url("./assets/background.svg");
        background-repeat: no-repeat;
        background-size: cover;
    }


</style>
