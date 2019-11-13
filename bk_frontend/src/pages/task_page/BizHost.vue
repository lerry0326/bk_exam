<template>
    <div>
        <el-form ref="form" :model="form" label-width="80px">
            <el-form-item label="业务">
                <el-select v-model="form.business" @change="get_host_by_biz()" placeholder="请选择业务">
                <el-option v-for="item in biz_options" :key="item.bk_biz_id" :label="item.bk_biz_name" :value="item.bk_biz_id"></el-option>
                <!-- <el-option label="嘉为蓝鲸" value="嘉为蓝鲸"></el-option> -->
                </el-select>
            </el-form-item>
            <el-form-item label="主机">
                <el-input type="textarea" v-model="form.host"></el-input>
            </el-form-item>
        </el-form>
        <div class="table">
            <el-table :data="tableData" stripe style="width: 100%">
                <el-table-column prop="bk_host_innerip" label="内网IP" width="180"></el-table-column>
                <el-table-column prop="bk_os_name" label="系统名" width="180"></el-table-column>
                <el-table-column prop="bk_host_name" label="主机名"></el-table-column>
                <el-table-column prop="" label="云区域" width="180"></el-table-column>
                <el-table-column prop="bk_mem" label="Mem(%)" width="180"></el-table-column>
                <el-table-column prop="bk_disk" label="Disk(%)" width="180"></el-table-column>
                <el-table-column prop="bk_cpu" label="CPU(%)" width="180"></el-table-column>
                <el-table-column
                        fixed="right"
                        label="操作">
                    <template slot-scope="scope">
                        <el-button v-if="scope.row.status==1" @click="send_apply_task(scope.row)" type="text"
                                   size="small">发起
                        </el-button>
                        <el-button @click="approve_apply(scope.row)" v-if="scope.row.status==2" type="text"
                                   size="small">审批
                        </el-button>
                        <el-button @click="search_perf(scope.row)" type="text" size="small">查询性能</el-button>
                        <el-button v-if="is_show" @click="add_mon(scope.row)" type="text" size="small">加入监控</el-button>
                        <el-button v-if="is_display" @click="cancel_mon(scope.row)" type="text" size="small">取消监控</el-button>
                        <el-button @click="modify(scope.row)" v-if="scope.row.status==1" type="text"
                                   size="small">编辑
                        </el-button>
                        <el-button @click="delete_apply_task(scope.row)" type="text" size="small"
                                   v-if="scope.row.status==1">
                            删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            form: {
                business: [],
                host: []
            },
            biz_options: [],
            tableData: [],
            bk_mem: '',
            is_show: true,
            is_display: false
        }
    },
    created() {
        this.getBiz()
        this.get_host_by_biz()
        // this.is_show = false
    },
    methods: {
        getBiz() {
            let patams = {}
            this.$api.getBiz().then(res => {
                this.biz_options = res.data
            })
        },
        get_host_by_biz() {
            this.getHost({
                biz_id: this.form.business
            })
        },
        getHost(apiparam) {
            let params = {}
            params = Object.assign(params, apiparam)
            this.$api.getHost(params).then(res => {
                for(let i = 0; i < res.data.length; i++) {
                    // this.form.host.push(res.data[i])
                    // this.form.host.push('\r\n')
                    this.tableData = res.data
                    console.log(11111111111, this.tableData)
                }
            })
        },
        search_perf(row) {
            console.log(22222, row)
            this.bk_mem = row.bk_mem
            // this.is_show = !this.is_show
            // if(this.is_show) {
            //     this.is_show = false
            // }else{
            //     this.is_show = true
            // }
        },
        add_mon(row) {
            this.$alert('确定加入监控队列', '标题名称', {
          confirmButtonText: 'OK',
          callback: action => {
            this.is_show = false;
            this.is_display = true
          }
        })
        },
        cancel_mon(row) {
            this.$alert('确定取消监控队列', '标题名称', {
          confirmButtonText: 'OK',
          callback: action => {
            this.is_show = true;
            this.is_display = false
          }
        })
        },
    }
}
</script>
<style lang="sass">
</style>
