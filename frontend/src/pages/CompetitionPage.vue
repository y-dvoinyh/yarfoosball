<template>
  <q-page>
    <div class="q-pa-md">
      <q-breadcrumbs>
        <q-breadcrumbs-el to="/" label="Главная" icon="home" />
        <q-breadcrumbs-el
          :label="player_info.first_name ? player_info.first_name + ' ' + player_info.last_name : ''"
          :to="{ name: 'player_page_route', params: {id: player_info.id}}"
        />
        <q-breadcrumbs-el
          :label="`${competition_info.name} (${competition_info.date})`"
        />
      </q-breadcrumbs>
      <div class="q-pa-md row items-start q-gutter-md">

        <q-card class="my-card col-grow" style="height: 350px">
          <q-card-section>
            <div class="text-subtitle2">Матчи</div>
          </q-card-section>
          <q-card-section>
            <apexchart
              height="250"
              type="donut"
              :options="chart_mathes_options"
              :series="chart_mathes_series"
            />
          </q-card-section>
        </q-card>

         <q-card class="my-card col-grow" style="height: 350px">
          <q-card-section>
            <div class="text-subtitle2">График рейтинга</div>
          </q-card-section>
          <q-card-section>
            <apexchart height="250" type="line" :options="chart_options" :series="chart_series"></apexchart>
          </q-card-section>
        </q-card>




      </div>
      <div class="q-pa-md row items-start q-gutter-md">
        <q-card class="my-card col-grow">
          <q-card-section>
            <div class="text-subtitle2">Матчи с участием игрока</div>
          </q-card-section>
          <q-card-section>
            <q-table
              :title="null"
              row-key="id"
              :columns="columns"
              :rows="rows"
              :rows-per-page-options="[0 ]"
              :loading="loading">
              <template v-slot:pagination=""></template>

              <template v-slot:body-cell="props">
                <q-td :props="props" v-if="(props.col.name === 'left_team')">
                  <q-item :to="{ name: 'competition_page_route', params: {id: props.row.left_team_first_id, competition_id: competition_info.id}}" dense>
                    <q-item-section :class="`cursor-pointer ${props.row.left_team_first_id == player_id ? 'text-green': 'text-primary'}`">{{props.row.left_team_first}}</q-item-section>
                  </q-item>
                  <q-item :class="`${!props.row.left_team_second_id ? 'hidden' : ''}`"  :to="{ name: 'competition_page_route', params: {id: props.row.left_team_second_id, competition_id: competition_info.id}}" dense>
                    <q-item-section :class="`cursor-pointer ${props.row.left_team_second_id == player_id ? 'text-green': 'text-primary'}`">{{props.row.left_team_second}}</q-item-section>
                  </q-item>
                </q-td>


                <q-td :props="props" v-else-if="props.col.name === 'right_team'">
                  <q-item :to="{ name: 'competition_page_route', params: {id: props.row.right_team_first_id, competition_id: competition_info.id}}" dense>
                    <q-item-section :class="`cursor-pointer ${props.row.right_team_first_id == player_id ? 'text-green': 'text-primary'}`">{{props.row.right_team_first}}</q-item-section>
                  </q-item>
                  <q-item :class="`${!props.row.right_second_id ? 'hidden' : ''}`" :to="{ name: 'competition_page_route', params: {id: props.row.right_second_id, competition_id: competition_info.id}}" dense>
                    <q-item-section :class="`cursor-pointer ${props.row.right_second_id == player_id ? 'text-green': 'text-primary'}`">{{props.row.right_second}}</q-item-section>
                  </q-item>
                </q-td>
                <q-td :props="props" v-else> {{props.value}} </q-td>
              </template>


            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import {defineComponent, onMounted, ref, watch} from "vue";
import api from 'src/api'
import {useQuasar} from "quasar";

export default defineComponent({
  props: {
    id: String,
    competition_id: String
  },
  name: 'CompetitionPage',
  setup (props) {
    const $q = useQuasar()
    const chart_series = ref([]);
    const chart_options = ref({});
    const player_info = ref({
      rating: null,
      matches: null,
      wins: null,
      losses: null,
      first_name: null,
      last_name: null,
    })
    const player_id = ref();
    player_id.value = props.id;
    const competition_info = ref({
      id: null,
      name: null,
      date: null
    })
    const columns = [
      { name: 'rating', label: 'Рейтинг', align: 'right', field: 'rating', sortable: false, headerStyle: 'width: 100px'},
      { name: 'diff', label: '+/-', align: 'right', field: 'diff', sortable: false, headerStyle: 'width: 100px',
        format: (val, row) => `${val && val > 0 ? '+' : ''}${val || val === 0 ? val : ''}`,
        style: row => (row.diff > 0 ? 'color: green' : 'color: red')
      },
      { name: 'left_team', label: 'Команда 1', align: 'right', field: 'left_team_first', sortable: false},

      { name: 'score', label: 'Счет', align: 'center', field: 'score', sortable: false },
      { name: 'right_team', label: 'Команда 2', align: 'left', field: 'right_team_first', sortable: false}
    ];
    const loading = ref(true);
    const rows = ref([]);

    const chart_mathes_options = ref({
      chart: {
        name: 'matches_chart',
        type: 'donut',
        height: '200px',
        width: '200px'
      },
      labels: ['Побед', 'Поражений', 'Ничья'],

      plotOptions: {
        pie: {
          donut: {
            labels: {
              show: true,
              total: {
                label: "Матчей",
                showAlways: true,
                show: true
              }
            }
          }
        }
      }

    })
    const chart_mathes_series = ref([]);

    const fetchMatches = () => {
      api.players.get_player_competition(props.id, props.competition_id)
      .then((response) => {
        const responce_data = response.data
        rows.value.splice(0, rows.value.length, ...responce_data)
        loading.value = false;

        chart_options.value = {
          chart: {
            type: 'line',
            height: '250px'
          },
          xaxis: {
            categories: responce_data.map(function(item) {
                return item.diff;
            })
          },

        }

        chart_series.value = [{
          name: 'rating',
          data: responce_data.map(function(item) {
              return item.rating;
          })
        }]

        const series = responce_data.reduce((acc, el)=>{
            const name = el.wins_diff === 1 ? 'Побед' : el.losses_diff === 1 ? 'Поражений' : 'Ничья'
            if (!acc.hasOwnProperty(name)) {
              acc[name] = 1
            }
            else {
              acc[name] += 1
            }
            return acc;
          },
          {}
        );

        chart_mathes_series.value = [series['Побед'] | 0, series['Поражений'] | 0, series['Ничья'] | 0]

      })
      .catch((e) => {
        console.log(e)
        $q.notify({
          color: 'negative',
          position: 'top',
          message: 'Ошибка загрузки',
          icon: 'report_problem'
        });
      });
    };
    const fetchPlayerInfo = () => {

      api.players.get_player_info(props.id)
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

    const fetchCompetitionInfo = () => {

      api.players.get_competition_info(props.competition_id)
      .then((response) => {
        const responce_data = response.data

        competition_info.value = {
          id: responce_data.id,
          name: responce_data.name,
          date: responce_data.date
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

    async function onRequest () {
      loading.value = true
      // Загрузка данных
      fetchMatches();
    }

    function load_data(){
      fetchPlayerInfo();
      fetchCompetitionInfo();
      fetchMatches()
    }

    watch(() => props.id, (new_id, prev_id) => {
      player_id.value = new_id;
      load_data();
    });

    // Загрузка данных при инициализации таблицы
    onMounted(() => {
      load_data()
    });

    return {
      columns,
      rows,
      loading,
      player_info,
      competition_info,
      player_id,
      chart_options,
      chart_series,
      chart_mathes_options,
      chart_mathes_series
    }
  }
});
</script>


<!--get_player_competition-->
