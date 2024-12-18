<template>
  <q-page>
    <div class="q-pa-md">
      <q-breadcrumbs>
        <q-breadcrumbs-el to="/" label="Главная" icon="home" />
        <q-breadcrumbs-el :label="player_info.first_name ? player_info.first_name + ' ' + player_info.last_name : ''" />
      </q-breadcrumbs>
      <div id="chart"/>

      <div class="q-pa-md">
        <div class="row">
        <div class="q-layout-padding" style="width: 450px">
          <q-table
            title="Больше всего выиграл матчей"
            row-key="id"
            :columns="parners_opponents_columns_win"
            :rows="opponents_rows_win"
            :rows-per-page-options="[0]"
          >
            <template v-slot:pagination=""></template>
          </q-table>
        </div>
        <div class="q-layout-padding" style="width: 450px">
          <q-table
            title="Больше всего проиграл матчей"
            row-key="id"
            :columns="parners_opponents_columns_loss"
            :rows="opponents_rows_loss"
            :rows-per-page-options="[0]"
          >
            <template v-slot:pagination=""></template>
          </q-table>
        </div>
        <div class="q-layout-padding" style="width: 450px">
          <q-table
            title="Лучший напарник"
            row-key="id"
            :columns="parners_opponents_columns_win"
            :rows="partners_rows_win"
            :rows-per-page-options="[0]"
          >
            <template v-slot:pagination=""></template>
          </q-table>
        </div>
        <div class="q-layout-padding" style="width: 450px">
          <q-table
            title="Худший напарник"
            row-key="id"
            :columns="parners_opponents_columns_loss"
            :rows="partners_rows_loss"
            :rows-per-page-options="[0]"
          >
            <template v-slot:pagination=""></template>
          </q-table>
        </div>
      </div>
      </div>
      <q-table
        :title="player_info.first_name ? player_info.first_name + ' ' + player_info.last_name + ' ' + player_info.rating : ''"
        row-key="id"
        :columns="columns"
        :rows="rows"
        ref="tableRef"
        :loading="loading"
        v-model:pagination="pagination"
        @request="onRequest"
      >
        <template v-slot:body-cell="props">
          <q-td :props="props" v-if="props.col.name === 'name'">
            <q-btn
              flat color="primary"
              :label="props.value"
              :to="{ name: 'competition_page_route', params: {id: props.row.player_id, competition_id: props.row.id}}"
            />
          </q-td>
          <q-td :props="props" v-else> {{props.value}} </q-td>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import {defineComponent, onMounted, ref} from 'vue'
import ApexCharts from 'apexcharts'
import api from 'src/api'
import {useQuasar} from "quasar";

export default defineComponent({
  props: {
    id: String
  },
  name: 'PlayerPage',
  setup (props) {
    const $q = useQuasar()
    const player_id = props.id;
    const tableRef = ref()
    const columns = [
      { name: 'name', label: 'Соревнование', align: 'left', field: 'name', sortable: false},
      { name: 'date', label: 'Дата', align: 'left', field: 'date', sortable: false},
      { name: 'rating', label: 'Рейтинг', align: 'left', field: 'rating', sortable: false },
      { name: 'diff', label: '+/-', align: 'left', field: 'diff', sortable: false,
        format: (val, row) => `${val && val > 0 ? '+' : ''}${val || val === 0 ? val : ''}`,
        style: row => (row.diff > 0 ? 'color: green' : 'color: red')
      },
      { name: 'matches_diff', label: 'Матчей', align: 'left', field: 'matches_diff', sortable: false },
      { name: 'wins_diff', label: 'Побед', align: 'left', field: 'wins_diff', sortable: false },
      { name: 'losses_diff', label: 'Поражений', align: 'left', field: 'losses_diff', sortable: false },

      { name: 'percent_win', label: 'Процент побед', align: 'left', field: 'wins_diff', sortable: false,
        format: (val, row) => `${Math.round((val/row.matches_diff) * 100)}%`},
    ]
    const parners_opponents_columns_win = [
      { name: 'name', label: 'Игрок', align: 'left', field: 'name', sortable: false},
      { name: 'count', label: 'Матчей выиграно', align: 'left', field: 'count', sortable: false}
    ];
    const parners_opponents_columns_loss = [
      { name: 'name', label: 'Игрок', align: 'left', field: 'name', sortable: false},
      { name: 'count', label: 'Матчей проиграно', align: 'left', field: 'count', sortable: false}
    ];
    const loading = ref(true);
    const rows = ref([]);
    const partners_rows_win = ref([]);
    const partners_rows_loss = ref([]);
    const opponents_rows_win = ref([]);
    const opponents_rows_loss = ref([]);
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

    const fetchPartners = () => {
      api.players.get_partners(player_id)
      .then((response) => {
        const responce_data = response.data
        const partners_win = responce_data.filter(function (item){return item.is_win});
        partners_rows_win.value.splice(0, partners_rows_win.value.length, ...partners_win)
        const partners_loss = responce_data.filter(function (item){return item.is_losse});
        partners_rows_loss.value.splice(0, partners_rows_loss.value.length, ...partners_loss)
      })
      .catch(() => {
        $q.notify({
          color: 'negative',
          position: 'top',
          message: 'Ошибка загрузки',
          icon: 'report_problem'
        });
      });
    }

    const fetchOpponents = () => {
      api.players.get_opponents(player_id)
      .then((response) => {
        const responce_data = response.data
        const opponents_win = responce_data.filter(function (item){return item.is_win});
        opponents_rows_win.value.splice(0, opponents_rows_win.value.length, ...opponents_win)
        const opponents_loss = responce_data.filter(function (item){return item.is_losse});
        opponents_rows_loss.value.splice(0, opponents_rows_loss.value.length, ...opponents_loss)
      })
      .catch(() => {
        $q.notify({
          color: 'negative',
          position: 'top',
          message: 'Ошибка загрузки',
          icon: 'report_problem'
        });
      });
    }

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
            height: '250px'
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
      console.log('onMounted');
      fetchPlayerInfo(player_id);
      fetchPartners();
      fetchOpponents();
      fetchCompetitions(pagination.value.page, pagination.value.rowsPerPage, player_id, filter.value);
      fetchChart();
    });

    return {
      columns,
      rows,
      loading,
      pagination,
      filter,
      player_info,
      onRequest,
      tableRef,
      parners_opponents_columns_win,
      parners_opponents_columns_loss,
      partners_rows_win,
      partners_rows_loss,
      opponents_rows_win,
      opponents_rows_loss
    }
  }
})
</script>
