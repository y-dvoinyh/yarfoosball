<template>
  <q-page>
    <div class="q-pa-md">
      <q-breadcrumbs>
        <q-breadcrumbs-el to="/" label="Главная" icon="home" />
        <q-breadcrumbs-el
          :label="player_info.first_name ? player_info.first_name + ' ' + player_info.last_name : ''"
          :to="{ name: 'player_page_route', params: {id: player_id}}"
        />
        <q-breadcrumbs-el
          :label="`${competition_info.name} (${competition_info.date})`"
        />
      </q-breadcrumbs>
      <div id="chart"/>
        <q-table
          :title="null"
          row-key="id"
          :columns="columns"
          :rows="rows"
          :rows-per-page-options="[0 ]"
          :loading="loading">
          <template v-slot:pagination=""></template>
        </q-table>
    </div>
  </q-page>
</template>

<script>
import {defineComponent, onMounted, ref} from "vue";
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
    const player_id = props.id;
    const competition_id = props.competition_id;
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
      { name: 'left_team', label: ' ', align: 'right', field: 'left_team_first', sortable: false,
        format: (val, row) => `${val} ${row.left_team_second_id? '/': ''} ${row.left_team_second}`},

      { name: 'score', label: 'Счет', align: 'center', field: 'score', sortable: false },

      { name: 'right_team', label: ' ', align: 'left', field: 'right_team_first', sortable: false,
        format: (val, row) => `${val}  ${row.right_second_id? '/': ''} ${row.right_second}`},



      // { name: 'percent_win', label: 'Процент побед', align: 'left', field: 'wins_diff', sortable: false,
      //   format: (val, row) => `${Math.round((val/row.matches_diff) * 100)}%`},
    ];
    const loading = ref(true);
    const rows = ref([]);

    const fetchMatches = () => {
      api.players.get_player_competition(player_id, competition_id)
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

    const fetchCompetitionInfo = () => {

      api.players.get_competition_info(competition_id)
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

    // Загрузка данных при инициализации таблицы
    onMounted(() => {
      fetchPlayerInfo();
      fetchCompetitionInfo();
      fetchMatches()
    });

    return {
      columns,
      rows,
      loading,
      player_info,
      player_id,
      competition_info
    }
  }
});
</script>


<!--get_player_competition-->
