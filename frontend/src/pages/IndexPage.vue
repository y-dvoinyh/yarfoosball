<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md">
      <p class="text-h5">Список игроков</p>
      <q-list bordered separator>
        <div v-for="row in players" :key="row.id">
          <q-item>
            <q-item-section>
              <q-item-label  >{{row.first_name + ' ' + row.last_name}}</q-item-label>
            </q-item-section>
          </q-item>
        </div>
      </q-list>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import api from 'src/api'

export default defineComponent({
  name: 'IndexPage',
  setup () {
    const players = ref([]);

    // Загрузка данных при инициализации таблицы
    onMounted(() => {
      api.players.list().then((response) => {
        players.value.splice(0, players.value.length, ...response.data)
      });
    });

    return {
      players
    }
  }
})
</script>
