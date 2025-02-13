<template>
    <div class="container">
        <p class="category-name">
            - {{ categoryName }} -
        </p>
        <div class="card mb-3" style="max-width: 700px;">
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
  .normalize('NFD') // Normaliza la cadena
  .replace(/[\u0300-\u036f]/g, '') // Elimina los caracteres diacríticos
  .replace(/ /g, '-') // Reemplaza los espacios por guiones
  .toLowerCase(); // Convierte a minúsculas
</script>

<style scoped>
    .category-name {
    color: red;
    margin-top: 10px;
  }

  .img-circle {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Hace que la imagen cubra todo sin deformarse */
  border-radius: 50%;
}

.circle {
  width: 60px;  /* Reduce el tamaño */
  height: 60px;
  border-radius: 50%; /* Mantiene la forma circular */
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>