<template>
    <div>
        <!-- <el-form ref="form" :model="form" label-width="80px">
            <el-form-item label="业务">
                <el-select v-model="form.business" placeholder="请选择业务">
                <el-option label="蓝鲸" value="蓝鲸"></el-option>
                <el-option label="嘉为蓝鲸" value="嘉为蓝鲸"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="主机">
                <el-select v-model="form.host" placeholder="请选择主机">
                <el-option label="192.168.0.1" value="192.168.0.1"></el-option>
                <el-option label="192.168.0.2" value="192.168.0.2"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="getHost">查询</el-button>
            </el-form-item>
        </el-form>
        <el-table :data="tableData" stripe style="width: 100%">
            <el-table-column prop="business" label="业务" width="180"></el-table-column>
            <el-table-column prop="cluster" label="集群" width="180"></el-table-column>
            <el-table-column prop="host" label="主机"></el-table-column>
        </el-table> -->
      <div id="myChart" :style="{width: '300px', height: '300px'}"></div>
      <div id="main1" style="float:left;width:100%;height: 300px"></div>
    </div>
</template>
<script>
let echarts = require('echarts/lib/echarts')
require('echarts/lib/chart/pie')
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')
  export default {
    data () {
      return {
        form: {
          business: '',
          cluster: '',
          host: ''
        },
        tableData: {
            business: '',
          cluster: '',
          host: ''
        },
        msg: 'hello world',
      }
    },
    mounted() {
      this.drawLine()
      this.initData()
    },
    methods: {
      getHost() {
          let params = {
              business: this.form.business,
              host: this.form.host
          }
          this.$api.getHost().then(res => {
              console.log(res)
          })
      },
      drawLine() {
        let myChart = this.$echarts.init(document.getElementById('myChart'))
        myChart.setOption({
          title: { text: 'echart练习' },
          tooltip: {},
          xAxis: {
            data: [ '衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子' ]
          },
          yAxis: {},
          series: [{
            name: '销量',
            type: 'bar',
            data: [ 5, 20, 36, 10, 10, 20 ]
          }]
        })
      },
      initData() {
        var myChart2 = echarts.init(document.getElementById('main1'));
        myChart2.setOption({
          title: {
            text: '饼图pratice',
            subtext: '纯属练习',
            x: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{ a } <br/>{b} : {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            bottom: 'bottom',
            data: ['直接访问', '邮件营销', '联盟广告', '视频广告', '搜索引擎']
          },
          series: [{
            name: '访问来源',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [
              {value: 335, name: '直接访问'},
              {value: 310, name: '邮件营销'},
              {value: 234, name: '联盟广告'},
              {value: 135, name: '视频广告'},
              {value: 1548, name: '搜索引擎'}
            ],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }]
        })
      }
    }
  }
</script>
<style lang='scss'>
</style>
