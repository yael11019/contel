<template>
    <div class="container">
        <p class="category-name">
            - {{ categoryName }} -
        </p>
        <div class="card mb-3">
            <div class="row g-0 align-items-center">
                <div class="col-4 col-md-4">
                    <img src="../assets/contelLogo.png" class="img-fluid rounded-start" alt="Logo">
                </div>
                <div class="col-8 col-md-8">
                    <div class="card-body">
                        <h5 class="card-title">{{ merchantName }}</h5>
                        <p class="card-text">
                            Cel. (453) 999 999, Tel. (453) 999 999
                            Calle, número, colonia, C.P 
                            Municipio
                        </p>
                        <router-link
                            :to="{ name: 'merchant', params: { merchantName: merchantRouterName, categoryName: categoryName } }"
                        >
                            <p>Ver más ...</p>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  categoryName: String,
})

const merchantName = 'Nombre o razón social';

const merchantRouterName = merchantName
  .normalize('NFD')
  .replace(/[\u0300-\u036f]/g, '')
  .replace(/ /g, '-')
  .toLowerCase();
</script>

<style scoped>
/* Contenedor principal: Centra la card */
.container {
    display: flex;
    flex-direction: column;
    align-items: center; /* Centra verticalmente */
    min-height: 100vh; /* Ocupa toda la altura de la pantalla */
    text-align: center;
}

/* Centra el nombre de la categoría */
.category-name {
    color: red;
    margin-top: 10px;
    text-align: center;
}

/* Centra la tarjeta */
.card {
    max-width: 700px;
    width: 100%; /* Que ocupe el 100% del ancho permitido */
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Agrega una sombra ligera */
    padding: 20px;
}

/* Imagen redonda */
.img-circle {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}

.circle {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
