<template>
    <div class="success-wrapper">
        <div class="success-container">
            <h1>Registration Completed</h1>
            <p class="success-subtitle">An e-mail regarding your pickup detail will be sent within 24 hours before the
                trip.</p>
            <img src="../assets/mirage-message-sent.png">
        </div>
    </div>
</template>

<script>
    export default {
        name: "Success"
    }
</script>

<style scoped>
    .success-wrapper {
        font-family: Roboto, sans-serif;
        display: flex;
    }

    .success-container {
        margin: 0 35px;
    }

    h1 {
        font-weight: bold;
        color: white;
        font-size: 50px;
        margin-bottom: 4px;
        margin-top: 54px;
        line-height: 72px;
    }

    p.success-subtitle {
        color: #8A8A8A;
        font-weight: bold;
        font-size: 16px;
        line-height: 24px;
        letter-spacing: 0.4px;
    }

    img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
    }
</style>