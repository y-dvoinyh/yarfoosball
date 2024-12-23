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

         <q-card class="my-card col-grow">
          <q-card-section>
            <div class="text-subtitle2">График рейтинга</div>
          </q-card-section>
          <q-card-section>
            <div id="chart"/>
          </q-card-section>
        </q-card>

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
                <q-td :props="props" v-if="(props.col.name === 'left_team_sp')">
                  <q-btn
                    flat color="primary"
                    :label="props.value"
                    :to="{ name: 'competition_page_route', params: {id: props.row.left_team_second_id, competition_id: competition_info.id}}"
                  />
                </q-td>
                <q-td :props="props" v-else-if="props.col.name === 'left_team_fp'">
                  <q-btn
                    flat color="primary"
                    :label="props.value"
                    :to="{ name: 'competition_page_route', params: {id: props.row.left_team_first_id, competition_id: competition_info.id}}"
                  />
                </q-td>
                <q-td :props="props" v-else-if="props.col.name === 'right_team_fp'">
                  <q-btn
                    flat color="primary"
                    :label="props.value"
                    :to="{ name: 'competition_page_route', params: {id: props.row.right_team_first_id, competition_id: competition_info.id}}"
                  />
                </q-td>
                <q-td :props="props" v-else-if="props.col.name === 'right_team_sp'">
                  <q-btn
                    flat color="primary"
                    :label="props.value"
                    :to="{ name: 'competition_page_route', params: {id: props.row.right_second_id, competition_id: competition_info.id}}"
                  />
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
import ApexCharts from 'apexcharts'

export default defineComponent({
  props: {
    id: String,
    competition_id: String
  },
  name: 'CompetitionPage',
  setup (props) {
    const $q = useQuasar()
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
      { name: 'left_team_sp', label: ' ', align: 'right', field: 'left_team_second', sortable: false},
      { name: 'left_team_fp', label: ' ', align: 'left', field: 'left_team_first', sortable: false},

      { name: 'score', label: 'Счет', align: 'center', field: 'score', sortable: false },

      { name: 'right_team_fp', label: ' ', align: 'right', field: 'right_team_first', sortable: false},
      { name: 'right_team_sp', label: ' ', align: 'left', field: 'right_second', sortable: false}
    ];
    const loading = ref(true);
    const rows = ref([]);

    const fetchMatches = () => {
      api.players.get_player_competition(props.id, props.competition_id)
      .then((response) => {
        const responce_data = response.data
        rows.value.splice(0, rows.value.length, ...responce_data)
        loading.value = false;

        const chart_options = {
          chart: {
            type: 'line',
            height: '250px'
          },
          series: [{
            name: 'rating',
            data: responce_data.map(function(item) {
                return item.rating;
            })
          }],
          xaxis: {
            categories: responce_data.map(function(item) {
                return item.diff;
            })
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
      player_id
    }
  }
});
</script>


<!--get_player_competition-->
