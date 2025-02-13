<template>
    <div class="container">
        <nav class="navbar">
            <div class="menu" @click="emit('toggleMenu')">
                <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/>
                </svg>
                <img src="../assets/contelLogo.png" alt="Contel Logo" width="100" height="50" class="logo option" @click="goToHome">
            </div>
            <div class="selector option">
                 <select class="form-select" aria-label="Default select example">
                    <option selected>Apatzingán</option>
                    <option value="2">Morelia</option>
                    <option value="3">Patzcuaro</option>
                </select>
            </div>
        </nav>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { defineEmits } from 'vue';

const router = useRouter();
const emit = defineEmits(['toggleMenu']);

const goToHome = () => {
    router.push('/');
};
</script>



<style scoped>
.container {
    background-color: rgb(27, 134, 27);;
    justify-content: space-between;
    padding: 0%;
    width : 100%;
    opacity: 1;
}

.option {
    align-items: center;
    display: flex;
    flex-direction: column;
    margin-left: 10px;
    margin-right: 10px;
    cursor: pointer;
}

.menu {
    display: flex;
    justify-content: space-between;
    
}

img.logo {
    cursor: pointer;
}

.selector {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.menu {
    cursor: pointer;
}

button {
    margin-left: 10px;
    background-color: white;
}
</style>