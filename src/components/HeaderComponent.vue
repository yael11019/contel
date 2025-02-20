<template>
    <div class="container">
        <nav class="navbar">
            <!-- Ícono del menú -->
             <div class="menu_logo">
                <div class="menu option" @click="emit('toggleMenu')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/>
                    </svg>
                </div>

                <!-- Logo en el centro -->
                <div class="logo-container">
                    <img src="../assets/contelLogo.png" alt="Contel Logo" width="100" height="50" class="logo option" @click="goToHome">
                </div>
            </div>

            <!-- Selector de ubicación -->
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
    background-color: rgb(27, 134, 27);
    display: flex;
    justify-content: center; /* Centra el contenido del navbar */
    align-items: center;
    padding: 0 20px;
    width: 100%;
    max-width: 100%;
}

.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    max-width: 1200px; /* Para evitar que los elementos se peguen demasiado en pantallas grandes */
}

/* Ajustes a los elementos internos */
.option {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 10px;
    cursor: pointer;
    color: white;
}

/* Distribuir los elementos correctamente */
.menu {
    display: flex;
    align-items: center;
}

.logo-container {
    flex-grow: 1; /* Hace que el logo se mantenga centrado */
    display: flex;
    justify-content: center;
}

.selector {
    display: flex;
    align-items: center;
}

img.logo {
    cursor: pointer;
}

button {
    margin-left: 10px;
    background-color: white;
}

.menu_logo {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
</style>
