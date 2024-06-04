import {api} from 'src/boot/axios'
import playersModule from './players'

export default {
  players: playersModule(api)
}
