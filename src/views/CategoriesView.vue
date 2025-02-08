<template>
    <HeaderComponent />
    <CategoriesComponent />
    <FooterComponent />
</template>

<script setup>
    import FooterComponent from '@/components/FooterComponent.vue';
    import HeaderComponent from '../components/HeaderComponent.vue';
    import CategoriesComponent from '@/components/CategoriesComponent.vue';
</script>

<style scoped>
footer {
  margin-top: auto; /* Empuja el footer al final */
}

.categories-componet {
    flex-grow: 1;
}
</style>