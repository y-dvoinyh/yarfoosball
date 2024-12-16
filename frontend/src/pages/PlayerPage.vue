<template>
  <q-page>
    <div class="q-pa-md">
      <q-breadcrumbs>
        <q-breadcrumbs-el to="/" label="Главная" icon="home" />
        <q-breadcrumbs-el :label="player_info.first_name ? player_info.first_name + ' ' + player_info.last_name : ''" />
      </q-breadcrumbs>
      <div id="chart"/>
      <q-table
        :title="player_info.first_name ? player_info.first_name + ' ' + player_info.last_name + ' ' + player_info.rating : ''"
        row-key="id"
        :columns="columns"
        :rows="rows"

        :loading="loading"
        v-model:pagination="pagination"
        @request="onRequest">
<!--          <template v-slot:top-right="props">-->
<!--            <q-input borderless dense debounce="300" v-model="filter" placeholder="Поиск">-->
<!--              <template v-slot:append>-->
<!--                <q-icon name="search" />-->
<!--              </template>-->
<!--            </q-input>-->
<!--            <q-btn-->
<!--              flat round dense-->
<!--              :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"-->
<!--              @click="props.toggleFullscreen"-->
<!--              class="q-ml-md"-->
<!--            />-->
<!--          </template>-->
      </q-table>
    </div>
  </q-page>
</template>

<script>
import {defineComponent, onMounted, ref} from 'vue'
import ApexCharts from 'apexcharts'
import api from 'src/api'

export default defineComponent({
  props: {
    id: String
  },
  name: 'PlayerPage',
  setup (props) {
    const player_id = props.id;
    const columns = [
      { name: 'name', label: 'Соревнование', align: 'left', field: 'name', sortable: false},
      { name: 'date', label: 'Дата', align: 'left', field: 'date', sortable: false},
      { name: 'rating', label: 'Рейтинг', align: 'left', field: 'rating', sortable: false },
      { name: 'diff', label: ' ', align: 'left', field: 'diff', sortable: false,
        format: (val, row) => `${val && val > 0 ? '+' : ''}${val || val === 0 ? val : ''}`,
        style: row => (row.diff > 0 ? 'color: green' : 'color: red')
      },
      { name: 'matches_diff', label: 'Матчей', align: 'left', field: 'matches_diff', sortable: false },
      { name: 'wins_diff', label: 'Побед', align: 'left', field: 'wins_diff', sortable: false },
      { name: 'losses_diff', label: 'Поражений', align: 'left', field: 'losses_diff', sortable: false },

      { name: 'percent_win', label: 'Процент побед', align: 'left', field: 'wins_diff', sortable: false,
        format: (val, row) => `${Math.round((val/row.matches_diff) * 100)}%`},
    ]
    const loading = ref(true);
    const rows = ref([]);
    const filter = ref('')

    const pagination = ref({
      sortBy: null,
      descending: null,
      page: 1,
      rowsPerPage: 10,
      rowsNumber: null
    });

    const player_info = ref({
      rating: null,
      matches: null,
      wins: null,
      losses: null,
      first_name: null,
      last_name: null,
    })

    const fetchCompetitions = (page, rowsPerPage, searchString) => {

      api.players.get_competitions(page, rowsPerPage, player_id, searchString)
      .then((response) => {
        const responce_data = response.data
        pagination.value.rowsNumber = responce_data.count

        rows.value.splice(0, rows.value.length, ...responce_data.competitions)
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

    const fetchChart = () => {

      api.players.get_competitions(0, 0, player_id, null)
      .then((response) => {
        const responce_data = response.data
        const chart_data = responce_data.competitions.reverse()

        const chart_options = {
          chart: {
            type: 'line',
            height: '300px'
          },
          series: [{
            name: 'rating',
            data: [...[1100], ...chart_data.map(function(item) {
                return item.rating;
            })]
          }],
          xaxis: {
            categories: [...['Старт'], ...chart_data.map(function(item) {
                return item.date;
            })]
          },

        }
        const chart = new ApexCharts(document.querySelector("#chart"), chart_options);
        chart.render();
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

    const fetchPlayerInfo = () => {

      api.players.get_player_info(player_id)
      .then((response) => {
        const responce_data = response.data

        player_info.value = {
          rating: responce_data.rating,
          matches: responce_data.matches,
          wins: responce_data.wins,
          losses: responce_data.losses,
          first_name: responce_data.first_name,
          last_name: responce_data.last_name,
        }
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
      fetchCompetitions(page, rowsPerPage, player_id, filter);
    }





    // Загрузка данных при инициализации таблицы
    onMounted(() => {
      console.log('onMounted')
      fetchPlayerInfo(player_id)
      fetchCompetitions(pagination.value.page, pagination.value.rowsPerPage, player_id, filter.value);
      fetchChart()
    });

    return {
      columns,
      rows,
      loading,
      pagination,
      filter,
      player_info,
      onRequest
    }
  }
})
</script>
