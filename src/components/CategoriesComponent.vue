<template>
    <div class="btn-group-vertical" role="group" aria-label="Basic example">
        <button type="button" class="btn btn-secondary">
            <img src="@/assets/tiendas.png" alt="icon" class="btn-icon">
            Tiendas
        </button>
        <button type="button" class="btn btn-secondary">
            <img src="@/assets/ferreterias.png" alt="icon" class="btn-icon">
            Ferreterias
        </button>
        <button type="button" class="btn btn-secondary">
            <img src="@/assets/panaderias.jpg" alt="icon" class="btn-icon">
            Panaderias
        </button>
    </div>
</template>

<script setup>

/*import { useRouter } from 'vue-router';

const router = useRouter();

const goToColdDrinks = () => {
    router.push({ path: '/bebidas'} )
}

const goToHotDrinks = () => {
    router.push({ path: '/hotDrinks'} )
}

const goToFoods = () => {
    router.push({ path: '/food'});
}*/

</script>

<style scoped>
.btn-group-vertical {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.btn {
  margin-bottom: 20px;
  background-color: #e50e0e;
  font-size: 40px;
  font-weight: bold;
  text-align: center;
  width: 100%;
  color: white;
  display: flex;
  align-items: center;
  padding: 10px;
}

.btn img {
  width: 150px; /* Ajusta el tamaño de la imagen según sea necesario */
  margin-right: 10px; /* Espacio entre la imagen y el texto */
}

.btn span {
  flex-grow: 1;
  text-align: center; /* Centra el texto */
}
</style>