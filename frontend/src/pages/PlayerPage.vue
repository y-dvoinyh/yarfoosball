<template>
  <q-page>
    <div class="q-pa-md">
      <q-breadcrumbs>
        <q-breadcrumbs-el to="/" label="Главная" icon="home" />
        <q-breadcrumbs-el :label="player_info.name" />
      </q-breadcrumbs>
      <div class="q-pa-md ">
        <q-card class="my-card" flat bordered>
          <q-card-section>
            <div class="text-h6">{{ player_info.name }}</div>
            <div class="text-subtitle2">Текущий рейтинг: {{player_info.rating}}</div>
          </q-card-section>
        </q-card>
      </div>

      <div class="q-pa-md row items-start q-gutter-md">
        <q-card class="my-card col-grow"  style="height: 375px">
          <q-card-section>
            <div class="text-subtitle2">Статистика</div>
          </q-card-section>
          <q-card-section>
            <q-markup-table>
              <tbody>
                <tr v-for="row in statistic_rows" :key="row.id">
                   <td class="text-left">{{ row.name  }}</td>
                   <td class="text-left">{{ row.value  }}</td>
                </tr>
              </tbody>
            </q-markup-table>
          </q-card-section>
        </q-card>

        <q-card class="my-card col-grow" style="height: 375px">
          <q-card-section>
            <div class="text-subtitle2">Медали</div>
          </q-card-section>
          <q-card-section>
            <q-markup-table>
              <tbody>
                <tr v-for="row in medal_rows" :key="row.id">
                   <td class="text-left">{{ row.name  }}</td>
                   <td class="text-left">{{ row.value  }}</td>
                </tr>
              </tbody>
            </q-markup-table>
          </q-card-section>
        </q-card>

        <q-card class="my-card col-grow" style="height: 375px">
          <q-card-section>
            <div class="text-subtitle2">Серии</div>
          </q-card-section>
          <q-card-section>
            <q-markup-table>
              <tbody>
                <tr v-for="row in series_rows" :key="row.id">
                   <td class="text-left">{{ row.name  }}</td>
                   <td class="text-left">{{ row.value  }}</td>
                </tr>
              </tbody>
            </q-markup-table>
          </q-card-section>
        </q-card>

        <q-card class="my-card col-grow" style="width: 800px; height: 375px">
          <q-card-section>
            <div class="text-subtitle2">График рейтинга</div>
          </q-card-section>
          <q-card-section>
            <div id="chart"/>
          </q-card-section>
        </q-card>

        <q-card class="my-card col-grow" >
          <q-card-section>
            <div class="text-subtitle2">Больше всего выиграл матчей</div>
          </q-card-section>
          <q-card-section>
            <q-markup-table>
              <thead>
                  <tr>
                    <th class="text-left">Противник</th>
                    <th class="text-left">Матчей</th>
                  </tr>
              </thead>
              <tbody>
                <tr v-for="row in opponents_rows_win" :key="row.id">
                    <td class="text-left">
                      <q-btn
                        flat color="primary"
                        :label="row.name"
                        :to="{ name: 'player_page_route', params: {id: row.id}}"
                      />
                    </td>
                   <td class="text-left">{{ row.count  }}</td>
                </tr>
              </tbody>
            </q-markup-table>
          </q-card-section>
        </q-card>

        <q-card class="my-card col-grow">
          <q-card-section>
            <div class="text-subtitle2">Больше всего проиграл матчей</div>
          </q-card-section>
          <q-card-section>
            <q-markup-table>
              <thead>
                  <tr>
                    <th class="text-left">Противник</th>
                    <th class="text-left">Матчей</th>
                  </tr>
              </thead>
              <tbody>
                <tr v-for="row in opponents_rows_loss" :key="row.id">
                   <td class="text-left">
                      <q-btn
                        flat color="primary"
                        :label="row.name"
                        :to="{ name: 'player_page_route', params: {id: row.id}}"
                      />
                    </td>
                   <td class="text-left">{{ row.count  }}</td>
                </tr>
              </tbody>
            </q-markup-table>
          </q-card-section>
        </q-card>

        <q-card class="my-card col-grow">
          <q-card-section>
            <div class="text-subtitle2">Напарник с которым больше всего выиграно матчей</div>
          </q-card-section>
          <q-card-section>
            <q-markup-table>
              <thead>
                  <tr>
                    <th class="text-left">Напарник</th>
                    <th class="text-left">Матчей</th>
                  </tr>
              </thead>
              <tbody>
                <tr v-for="row in partners_rows_win" :key="row.id">
                   <td class="text-left">
                      <q-btn
                        flat color="primary"
                        :label="row.name"
                        :to="{ name: 'player_page_route', params: {id: row.id}}"
                      />
                    </td>
                   <td class="text-left">{{ row.count  }}</td>
                </tr>
              </tbody>
            </q-markup-table>
          </q-card-section>
        </q-card>

        <q-card class="my-card col-grow">
          <q-card-section>
            <div class="text-subtitle2">Напарник с которым больше всего проиграно матчей</div>
          </q-card-section>
          <q-card-section>
            <q-markup-table>
              <thead>
                  <tr>
                    <th class="text-left">Напарник</th>
                    <th class="text-left">Матчей</th>
                  </tr>
              </thead>
              <tbody>
                <tr v-for="row in partners_rows_loss" :key="row.id">
                   <td class="text-left">
                      <q-btn
                        flat color="primary"
                        :label="row.name"
                        :to="{ name: 'player_page_route', params: {id: row.id}}"
                      />
                    </td>
                   <td class="text-left">{{ row.count  }}</td>
                </tr>
              </tbody>
            </q-markup-table>
          </q-card-section>
        </q-card>
      </div>
      <div class="q-pa-md">
        <q-table
        title="Список соревнований"
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
    </div>
  </q-page>
</template>

<script>
import {defineComponent, onMounted, reactive, ref, watch} from 'vue'
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
    const tableRef = ref()
    const columns = [
      { name: 'name', label: 'Соревнование', align: 'left', field: 'name', sortable: false},
      { name: 'date', label: 'Дата', align: 'left', field: 'date_str', sortable: false},
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
    const loading = ref(true);
    const rows = ref([]);
    const statistic_rows = ref([]);
    const medal_rows = ref([]);
    const series_rows = ref([]);
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
      id: null,
      name: null,
      rating: null,
      competitions_count: null,
      matches: null,
      wins: null,
      losses: null,
      draws: null,
      percent_wins: null,
      gold: null,
      silver: null,
      bronze: null
    })

    const fetchPartners = () => {
      api.players.get_partners(props.id)
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
      api.players.get_opponents(props.id)
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

      api.players.get_competitions(page, rowsPerPage, props.id, searchString)
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

      api.players.get_competitions(0, 0, props.id, null)
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
                return item.date_str;
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

    const fetchSeries = () => {
      api.players.get_series(props.id)
      .then((response) => {
        const responce_data = response.data

        series_rows.value.splice(
          0,
          series_rows.value.length, ...[
            {name: 'Побед подряд', value: responce_data.s_wins},
            {name: 'Поражений подряд', value: responce_data.s_loss},
            {name: 'Ничья подряд', value: responce_data.s_draws}
          ]);
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

    const fetchPlayerInfo = () => {

      api.players.get_player_statistic(props.id)
      .then((response) => {
        const responce_data = response.data
        player_info.value = {...response.data}
        statistic_rows.value.splice(
          0,
          statistic_rows.value.length, ...[
            {name: 'Турниров сыграно', value: player_info.value.competitions_count},
            {name: 'Матчей сыграно', value: player_info.value.matches},
            {name: 'Матчей выиграно', value: player_info.value.wins},
            {name: 'Матчей проиграно', value: player_info.value.losses},
            {name: 'Ничья', value: player_info.value.draws},
            {name: 'Процент побед', value: player_info.value.percent_wins ? `${player_info.value.percent_wins}%`: null},
          ]);
          medal_rows.value.splice(
          0,
            medal_rows.value.length, ...[
              {name: 'Золотых медалей', value: player_info.value.gold},
              {name: 'Серебряных медалей', value: player_info.value.silver},
              {name: 'Бронзовых медалей', value: player_info.value.bronze},
            ]);
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
      fetchCompetitions(page, rowsPerPage, props.id, filter);
    }

    function load_data() {
      fetchPlayerInfo(props.id);
      fetchPartners();
      fetchOpponents();
      fetchCompetitions(pagination.value.page, pagination.value.rowsPerPage, props.id, filter.value);
      fetchChart();
      fetchSeries();
    }
    watch(() => props.id, (new_id, prev_id) => {
      load_data();
    });

    // Загрузка данных при инициализации таблицы
    onMounted(() => {
      load_data();
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
      partners_rows_win,
      partners_rows_loss,
      opponents_rows_win,
      opponents_rows_loss,
      statistic_rows,
      medal_rows,
      series_rows,
      fetchPartners
    }
  }
})
</script>
