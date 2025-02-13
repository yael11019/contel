<template>
  <div class="container">
    <!-- Modal -->
    <ModalComponent 
      v-if="showModal && subCategories.length > 0" 
      @update:showModal="showModal = $event" 
      :isVisible="showModal"  
      :name="categoryName"
      :subCategories="subCategories"
    />

    <!-- Carrusel -->
    <div class="d-flex align-items-center">
      <div id="carouselExampleAutoplaying" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          <div
            v-for="(comercio, index) in comercios"
            :key="index"
            class="carousel-item"
            :class="{ active: index === 0 }"
            @click.prevent="irAPagina(comercio.url)"
            style="cursor: pointer;"
          >
            <img
              :src="comercio.img"
              class="d-block w-100 img-fluid carousel-img"
              :alt="comercio.nombre"
            />
          </div>
        </div>
        <button class="carousel-control-prev custom-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next custom-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </div>

    <!-- Categorías -->
    <div class="categories mt-4">
      <ul class="row list-unstyled text-center">
        <li 
          v-for="category in categoriesItems" 
          :key="category.id" 
          class="col-3 category-item" 
          @click="showModalAction(category)"
          style="cursor: pointer;"
        >
          <div class="circle">
            <span v-html="category.icon"></span>
          </div>
          <p class="category-name">{{ category.name }}</p>
        </li> 
      </ul>
    </div>

    <!-- Barra de búsqueda -->
    <div>
      <div class="input-group mb-3">
        <span class="input-group-text" id="inputGroup-sizing-default">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
          </svg>
        </span>
        <input
          type="text"
          class="form-control text-center"
          aria-label="Buscar"
          aria-describedby="inputGroup-sizing-default"
          placeholder="¿Qué buscas?"
        />
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { categories } from '../store/categoriesInfo.js';
import comercio1 from '@/assets/comercio1.png';
import comercio2 from '@/assets/comercio2.png';
import comercio3 from '@/assets/comercio3.jpg';
import ModalComponent from './ModalComponent.vue';
import { useRouter } from "vue-router";

const router = useRouter();

const showModal = ref(false);

const categoryName = ref('');

const subCategories = ref([]);

/*const filteredCategories = computed(() => {
  return categories.value.filter(category => category.subcategories.length > 0);
});*/


const showModalAction = (category) => {
  if (category.subCategories && category.subCategories.length > 0) {
    // Si tiene subcategorías, mostrar el modal
    subCategories.value = category.subCategories;
    categoryName.value = category.name;
    showModal.value = true;
  } else {
    // Si NO tiene subcategorías, ir a la ruta directamente
    router.push(`/categorias/${category.name}`);
  }
};

const comercios = [
  { img: comercio1, nombre: "Comercio 1", url: "https://www.gandhi.com.mx/?srsltid=AfmBOop9N995D44CkGyUrJHzbf-UijPBbu7cs5g5uDYCnLAgiGDKSdd5" },
  { img: comercio2, nombre: "Comercio 2", url: "https://www.veganlabel.mx/?srsltid=AfmBOopBvEyj6Q0ArbYUizjbfJ_oXLYf345TqHyBzi1k2yi3U1xVjhNv"  },
  { img: comercio3, nombre: "Comercio 3", url: "https://www.burgerking.com.mx/en/" }
];

const irAPagina = (url) => {
  window.open(url, '_blank');
};

const categoriesItems = ref(categories);

onMounted(() => {
  import('bootstrap/dist/js/bootstrap.bundle.min.js').then((bootstrap) => {
    new bootstrap.Carousel(document.getElementById('carouselExampleAutoplaying'), {
      interval: 3000, 
      ride: 'carousel'
    });
  });
});
</script>



<style scoped>
.container {
  justify-content: center;
  height: 100vh;
  background-color: white;
  margin-top: 10px;
  z-index: 1;
  position: relative; /* IMPORTANTE para que no bloquee el menú */
  overflow: visible; /* Evita que recorte el menú */
}

.categories {
  align-items: center;
}

.category-name {
  color: black;
}

.category-item {
  display: flex;
  flex-direction: column; /* Apila el círculo y el texto */
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-bottom: 20px;
}

.circle {
  width: 60px;
  height: 60px;
  background-color: rgb(78, 189, 78);
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-bottom: 8px; /* Espacio entre el círculo y el texto */
}

.carousel-inner {
  display: flex; /* Mantiene las imágenes alineadas */
  align-items: center; /* Centra verticalmente */
}

.carousel-item {
  text-align: center; /* Centra las imágenes horizontalmente */
}

.carousel-img {
  max-height: 500px; /* Ajusta la altura para mantener el tamaño uniforme */
  width: auto; /* Mantiene la proporción original */
  margin: auto; /* Centra la imagen dentro del carrusel */
}

/* Cambiar el color de los iconos dentro de los botones */
.custom-prev .carousel-control-prev-icon,
.custom-next .carousel-control-next-icon {
  background-color: black; /* Cambia el color del icono a negro */
}

/* Redondear los botones */
.custom-prev,
.custom-next {
  border: none; /* Elimina el borde predeterminado */
  border-radius: 50%; /* Botones redondeados */
  padding: 10px; /* Ajusta el tamaño del botón */
  background: none; /* Elimina el color de fondo */
}

/* Agregar efectos al pasar el cursor sobre los botones */
.custom-prev:hover,
.custom-next:hover {
  cursor: pointer; /* Cambia el cursor a puntero */
}
</style>
