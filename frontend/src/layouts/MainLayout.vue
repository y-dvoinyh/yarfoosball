<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          Рейтинг неофициальных соревнований
        </q-toolbar-title>
        <div>Версия 1.6</div>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>

defineOptions({
  name: 'MainLayout'
})

</script>
