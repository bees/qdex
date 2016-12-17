<template lang="pug">
.app
  header
    .wrap.nav
      el-button(type="text" icon="menu").browse
      el-input(
        placeholder="Search"
        v-model="search"
      ).search
      el-select(v-model='value', placeholder='Select').gen-select
        el-option(v-for='item in options', :label='item.label', :value='item.value')
  section.wrap.main
    .infobar
      .details
        h1 {{ poke.name }}
        div
          el-tag(v-for="type in poke.types" v-bind:class="[typeClasses[type.id]]") 
            | {{ type.string }}
        div.stat 
          span.label
            | Gender Ratios
          span.ratios
            span.female
              | &#x2640; {{ poke.breeding.female / 10 }}%
            |  /
            span.male
              |  &#x2642; {{ poke.breeding.male / 10 }}%
        div.stat 
          span.label
            | Catch rate 
          span.data
            | {{poke.training.catchRate}}%
        div.stat 
          span.label
            | Hatch Cycles
          span.data
            | {{ poke.breeding.cycles }}

      el-menu.el-menu-demo(mode='horizontal').actions
        el-submenu(index='1')
          template(slot='title') Workspace
          el-menu-item(index='1-1') item one
          el-menu-item(index='1-2') item two
          el-menu-item(index='1-3') item three
    
</template>

<script>
import store from 'store'
import { mapActions, mapGetters } from 'vuex'
import poke from './services/pokeStats'
export default {
  store,
  computed: mapGetters([
    'countPlural'
  ]),
  data () {
    return {
      search: '',
      poke: poke,
      typeClasses: [
        'fire',
        'poison'
      ],
      options: [
        {
          value: 7,
          label: 'Gen VII'
        }, {
          value: 6,
          label: 'Gen VI'
        }
      ],
      value: 7
    }
  },
  methods: {
    ...mapActions([
      'increment'
    ]),
    onLangClick (lang) {
      this.setLang(lang) // mixin method
      this.increment() // store action
    }
  }
}
</script>

<style lang="stylus">

body
  margin 0
  background #bdbdbd

header
  background red
  a
    color white

.wrap
  &.nav
    display flex
    .el-input
      width 100%
      height 100%
  +above(960px)
    lost-center 960px

.main
  background #e0e0e0

.infobar 
  background #fff
  height 60px
  h1 
    margin-left 1em
  .details
    lost-column 3/4
  .actions
    lost-align right
    lost-column 1/4
    height 100%
  .el-menu
    background #fff


.search.el-input
  padding 5px
  input
    background darkRed
    color #fff
    &::placeholder
      color #fff


.gen-select 
  max-width 6em
  .el-input__inner
    background #2196F3
    color #fff
    height 100%


button.browse
  color white
  border-radius 0
  padding  .5em
  &:focus,&:active
    color white
  &:hover
    color red
    background #fff

.infobar .details
  display flex
  align-items center
  > *
    margin-right 15px

.female
  color #e91e63

.male
  color #2196f3

.stat 
  display flex
  flex-direction column
  .label
    font-weight bold

.el-tag
  border none
  border-radius 0px
  margin-right 15px
  display inline-block
  &.poison 
    background #A040A0

  &.fire 
    background #f08030
</style>
