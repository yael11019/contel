<template>
  <div class="container">
    <p class="category-name">
      - {{ categoryName }} -
    </p>
    <div class="image-container">
      <img src="@/assets/comercio3.jpg" class="rectangular-image" alt="Rectángulo" />
      <img src="@/assets/contel.png" class="circular-image" alt="Círculo" />
    </div>
    <div class="merchant-information">
      <div class="principal-information"> 
        <h5>{{ merchantName }}</h5>
        <p>
          Cel. (453) 999 999, Tel. (453) 999 999
          <br>Calle, número, colonia, C.P 
          <br>Municipio
          <br>yael110@live.com.mx
        </p>
        <div class="categories mt-4">
          <ul class="row list-unstyled text-center">
            <li 
              v-for="webSite in webSites" 
              :key="webSite.id" 
              class="col-3 category-item" 
              @click="goToUrl(webSite.url)"
              style="cursor: pointer;"
            >
              <div class="circle">
                <span v-html="webSite.icon"></span>
              </div>
            </li> 
          </ul>
        </div>
      </div>
      <div class="secondary-information">
        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-book" viewBox="0 0 16 16">
          <path d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783"/>
        </svg>
        <h5>Catálogo</h5>
      </div>
    </div>
    <div class="services">
      <h4>Servicios/productos:</h4>
      <div class="rectangle">
        Lic. en Derecho egresada de la U.M.S.N.H.
        <br>Atención jurídica en materia civil, penal y familiar.
        <br>Asesoría para constitución de sociedades.
        <br>Horario:
        <br>Lunes a viernes de 10 a 2 pm y de 4 a 7 pm.
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps} from 'vue';
import { webSites } from '@/store/webSites';

defineProps({
  merchantName: String,
  categoryName: String,
})

const goToUrl = (url) => {
  window.open(url, '_blank');
}

</script>

<style scoped>
.image-container {
  position: relative;
  width: 450px; /* Ajusta el tamaño según necesites */
  justify-content: center;
  margin-top: 10px;
}

.rectangular-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
}

.circular-image {
  position: absolute;
  bottom: -40px;
  right: 20px;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 4px solid white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.container {
  justify-content: center;
}

.merchant-information {
  display: flex;
  justify-content: space-between; /* Separa los elementos */
  align-items: center; /* Centra verticalmente */
  width: 100%;
  padding: 20px;
  margin-top: 30px;
}

.secondary-information {
  width: 50%;
  text-align: center; /* Centra el contenido horizontalmente */
  display: flex;
  flex-direction: column;
  justify-content: center; /* Centra verticalmente */
  align-items: center; /* Centra el contenido */
}

.principal-information {
  width: 50%;
  text-align: left; /* Alineación del texto */
}

.rectangle {
  width: 450px;  /* Ancho del rectángulo */
  height: 150px; /* Alto del rectángulo */
  background-color: white; /* Fondo blanco */
  border: 2px solid black; /* Borde negro */
  display: flex;
  justify-content: center; /* Centra horizontalmente */
  align-items: center; /* Centra verticalmente */
  text-align: center;
}

</style>