<template>
    <div>
        <el-form ref="form" :model="form" label-width="80px">
            <el-form-item label="业务">
                <el-select v-model="form.business" @change="get_set_by_biz()" placeholder="请选择业务">
                <el-option v-for="item in biz_options" :key="item.bk_biz_id" :label="item.bk_biz_name" :value="item.bk_biz_id"></el-option>
                <!-- <el-option label="嘉为蓝鲸" value="嘉为蓝鲸"></el-option> -->
                </el-select>
            </el-form-item>
            <el-form-item label="集群">
                <el-select v-model="form.cluster" @change='get_host_by_set()' placeholder="请选择集群">
                <el-option v-for="item in set_options" :key="item.bk_set_id" :label="item.bk_set_name" :value="item.bk_set_id"></el-option>
                <!-- <el-option label="配置平台" value="配置平台"></el-option> -->
                </el-select>
            </el-form-item>
            <el-form-item label="主机">
                <el-select v-model="form.host" placeholder="请选择主机">
                <el-option v-for="item in host_options" :key="item.bk_host_id" :label="item.bk_host_innerip" :value="item.bk_host_id"></el-option>
                <!-- <el-option label="192.168.0.2" value="192.168.0.2"></el-option> -->
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="addHost">立即创建</el-button>
                <el-button>取消</el-button>
            </el-form-item>
        </el-form>

        <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
            <el-tab-pane label="用户管理" name="first">用户管理</el-tab-pane>
            <el-tab-pane label="配置管理" name="second">配置管理</el-tab-pane>
            <el-tab-pane label="角色管理" name="third">角色管理</el-tab-pane>
            <el-tab-pane label="定时任务补偿" name="fourth">定时任务补偿</el-tab-pane>
        </el-tabs>
    </div>
</template>
<script>
  export default {
    data() {
      return {
        form: {
          business: [],
          cluster: '',
          host: ''
        },
        biz_options: [],
        set_options: [],
        host_options: [],
        activeName: 'first'
      }
    },
    created() {
        this.getBiz()
        this.getSet()
    },
    methods: {
        handleClick(tab, event) {
            console.log(tab, event)
        },
        addHost() {
            let params = {
                business: this.form.business,
                cluster: this.form.cluster,
                host: this.form.host
            }
          this.$api.addHost().then(res => {
                console.log(res)
            })
        },
        getBiz() {
            let params = {}
            this.$api.getBiz().then(res => {
                let Adata = res.data
                // for(let i = 0; i < Adata.length; i++) {
                //     console.log(3333333333, Adata[i])
                //     this.biz_options.push(Adata[i].bk_biz_name)
                // }
                this.biz_options = Adata
            })
        },
        // change() {
        //     this.getSet()
        // },
        get_set_by_biz() {
            this.getSet({biz_id: this.form.business})
        },
        getSet(apiparam) {
            let params = {}
            params = Object.assign(params, apiparam)
            this.$api.getSet(params).then(res => {
                this.set_options = res.data
            })
            // this.$store.dispatch('task/getSet', params).then(res => {
                // this.set_options = res.data
            // })
        },
        get_host_by_set() {
            this.getHost({biz_id: this.form.business, set_id: this.form.cluster})
        },
        getHost(apiparams) {
            let params = {}
            params = Object.assign(params, apiparams)
            this.$api.getHost(params).then(res => {
                this.host_options = res.data
            })
        }
    }
  }
</script>
<style lang='scss'>
</style>
