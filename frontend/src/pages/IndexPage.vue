<template>
  <q-page>
    <div class="q-pa-md">
      <q-table
        title="Рейтинг игроков"
        row-key="id"
        :columns="columns"
        :loading="loading"
        :rows="rows"
        :filter="filter"
        :rows-per-page-options="[10, 15, 20, 25, 50, 0 ]"
        ref="tableRef"
        v-model:pagination="pagination"
        @request="onRequest"
       >
        <template v-slot:top-right="props">
          <q-input borderless dense debounce="300" v-model="filter" placeholder="Поиск">
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
          <q-btn
            flat round dense
            :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
            @click="props.toggleFullscreen"
            class="q-ml-md"
          />
        </template>
        <template v-slot:body-cell="props">
          <q-td :props="props" v-if="props.col.name === 'full_name'">
            <q-btn
              flat color="primary"
              :label="props.value"
              :to="{ name: 'player_page_route', params: {id: props.row.player_id}}"
            />
          </q-td>
          <q-td :props="props" v-else> {{props.value}} </q-td>
        </template>

      </q-table>
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
    const $q = useQuasar()

    const columns = [
      { name: 'number', label: '№', align: 'left', field: 'number', sortable: false },
      { name: 'full_name', label: 'Фамилия Имя', align: 'left', field: 'full_name', sortable: false},
      { name: 'rating', label: 'Рейтинг', align: 'left', field: 'rating', sortable: false },
      { name: 'last_diff', label: ' ', align: 'left', field: 'last_diff', sortable: false,
        format: (val, row) => `${val && val > 0 ? '+' : ''}${val || val === 0 ? val : ''}`,
        style: row => (row.last_diff > 0 ? 'color: green' : 'color: red')
      },

      { name: 'matches', label: 'Матчей', align: 'left', field: 'matches', sortable: false },
      { name: 'wins', label: 'Побед', align: 'left', field: 'wins', sortable: false },
      { name: 'losses', label: 'Поражений', align: 'left', field: 'losses', sortable: false },
      { name: 'percent_win', label: 'Процент побед', align: 'left', field: 'wins', sortable: false, format: (val, row) => `${Math.round((val/row.matches) * 100)}%`},
    ]

    const tableRef = ref()
    const loading = ref(true);
    const rows = ref([]);
    const filter = ref('')

    const pagination = ref({
      sortBy: null,
      descending: null,
      page: 1,
      rowsPerPage: 10,
      rowsNumber: null
    })


    const fetchRating = (page, rowsPerPage, searchString) => {
      api.rating.get_list(page, rowsPerPage, searchString)
      .then((response) => {
        const responce_data = response.data
        pagination.value.rowsNumber = responce_data.count

        rows.value.splice(0, rows.value.length, ...responce_data.players)
        pagination.value.page = page
        pagination.value.rowsPerPage = rowsPerPage

        loading.value = false;
      })
      .catch(() => {
        $q.notify({
          color: 'negative',
          position: 'top',
          message: 'Ошибка загрузки',
          icon: 'report_problem'
        });
      });
    };

    async function onRequest (props) {

      const { page, rowsPerPage } = props.pagination

      const filter = props.filter

      if (filter) {
        pagination.value.page = 0;
      }

      loading.value = true
      // Загрузка данных
      fetchRating(page, rowsPerPage, filter);
    }

    // Загрузка данных при инициализации таблицы
    onMounted(() => {
      console.log('onMounted')
      fetchRating(pagination.value.page, pagination.value.rowsPerPage, filter.value);
    });

    return {
      columns,
      rows,
      loading,
      pagination,
      tableRef,
      filter,
      onRequest
    }
  }
})
</script>
