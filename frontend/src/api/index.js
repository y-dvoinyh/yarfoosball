import {api} from 'src/boot/axios'
import playersModule from './players'
import ratingModule from './rating'

export default {
  players: playersModule(api),
  rating: ratingModule(api)
}
