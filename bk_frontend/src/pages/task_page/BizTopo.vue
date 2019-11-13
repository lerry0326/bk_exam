<template>
    <div>
        <el-button @click="transfertooper">备份操作</el-button>
        <el-button @click="transfertoreco">备份记录</el-button>
        <el-form ref="form" label-width="120px" :model="formApply" :rules="rulesApply">
            <el-form-item label="业务">
                <el-select @change="get_set_by_biz()" v-model="formApply.business"
                            placeholder="请选择">
                    <el-option
                            v-for="item in biz_options"
                            :key="item.bk_biz_id"
                            :label="item.bk_biz_name"
                            :value="item.bk_biz_id">
                    </el-option>
                </el-select>
            </el-form-item>
            <!-- <el-tree
            :props="biz_topo"
            :load="loadNode"
            lazy
            show-checkbox
            @check-change="handleCheckChange">
            </el-tree> -->
            <el-form-item label="集群">
                <el-select v-model="formApply.cluster" @change='get_module_by_set()' placeholder="请选择集群">
                <el-option v-for="item in set_options" :key="item.bk_set_id" :label="item.bk_set_name" :value="item.bk_set_id"></el-option>
                <!-- <el-option label="配置平台" value="配置平台"></el-option> -->
                </el-select>
            </el-form-item>
            <el-form-item label="模块">
                <el-select v-model="formApply.module" @change='get_host_by_module()' placeholder="请选择模块">
                <el-option v-for="item in module_options" :key="item.bk_module_id" :label="item.bk_module_name" :value="item.bk_module_id"></el-option>
                <!-- <el-option label="配置平台" value="配置平台"></el-option> -->
                </el-select>
            </el-form-item>
            <el-form-item label="主机">
                <el-input type="textarea" v-model="formApply.host"></el-input>
            </el-form-item>
        </el-form>
        <div class="search">
            <span class="aglin">目录：</span>
            <el-input style="width: 30%" class="aglin-input" size="mini" v-model="inputEmpName" clearable
                      placeholder="请输入内容"></el-input>
            <span class="aglin">文件名：</span>
            <el-input style="width: 30%" class="aglin-input" size="mini" v-model="inputEmpName" clearable
                      placeholder="请输入内容"></el-input>
            <el-button size="mini" type="primary" @click.native="search">立即搜索</el-button>
        </div>
        <el-table :data="tableData" stripe style="width: 100%">
            <el-table-column prop="name" label="序号" width="80"></el-table-column>
            <el-table-column prop="name" label="IP" width="180"></el-table-column>
            <el-table-column prop="status" label="文件列表" width="180"></el-table-column>
            <el-table-column prop="type" label="文件数量"></el-table-column>
            <el-table-column prop="status" label="文件总大小" width="180"></el-table-column>
            <el-table-column prop="type" label="操作"></el-table-column>
        </el-table>
    </div>
</template>
<script>
export default {
    data() {
        return {
            biz_options: [],
            set_options: [],
            module_options: [],
            formApply: {
                business: '',
                cluster: '',
                module: '',
                host: []
            },
            rulesApply: {
                business: [
                    {required: true, message: '请选择业务'},
                ]
            },
            biz_topo: [],
            tableData: []
        }
    },
    created() {
        this.get_biz_options()
        this.get_set_by_biz()
        this.get_module_by_set()
        this.get_host_by_module()
    },
    methods: {
        transfertoreco() {
            this.$router.replace('/bak_reco')
        },
        get_biz_options() {
            let params = {}
            this.$api.getBiz().then(res => {
                let Adata = res.data
                this.biz_options = Adata
            })
        },
        get_set_by_biz() {
            this.getSet({biz_id: this.formApply.business})
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
        get_module_by_set() {
            this.getModule({
                biz_id: this.formApply.business,
                set_id: this.formApply.cluster
            })
        },
        getModule(apiparam) {
            let params = {}
            params = Object.assign(params, apiparam)
            this.$api.getModule(params).then(res => {
                this.module_options = res.data
            })
        },
        get_host_by_module() {
            this.getHost({
                biz_id: this.formApply.business,
                set_id: this.formApply.cluster,
                module_id: this.formApply.module
            })
        },
        getHost(apiparam) {
            let params = {}
            params = Object.assign(params, apiparam)
            this.$api.getHost(params).then(res => {
                for(let i = 0; i < res.data.length; i++) {
                    console.log(3333333333, res.data[i])
                    this.formApply.host.push(res.data[i])
                    this.formApply.host.push('\n')
                }
                // this.formApply.host = res.data
            })
        },
        get_topo_by_biz() {
            this.getTopo({biz_id: this.formApply.business})
        },
        getTopo(apiparam) {
            let params = {}
            params = Object.assign(params, apiparam)
            this.$api.getTopo(params).then(res => {
                this.biz_topo = res.data
            })
        },
        handleCheckChange(data, checked, indeterminate) {
            console.log(data, checked, indeterminate);
        },
        handleNodeClick(data) {
            console.log(data);
        },
        loadNode(node, resolve) {
            if (node.level === 0) {
            return resolve([{ name: this.biz_topo.bk_obj_name }, { name: this.biz_topo.bk_obj_name }]);
            }
            if (node.level > 3) return resolve([]);

            var hasChild;
            if (node.data.name === this.biz_topo.bk_obj_name) {
            hasChild = true;
            } else if (node.data.name === this.biz_topo.bk_obj_name) {
            hasChild = false;
            } else {
            hasChild = Math.random() > 0.5;
            }
            setTimeout(() => {
                var data;
                if (hasChild) {
                    data = [{
                    // name: 'zone' + this.count++
                    name: this.biz_topo.bk_obj_name
                    }, {
                    // name: 'zone' + this.count++
                    name: this.biz_topo.bk_obj_name
                    }];
                } else {
                    data = [];
                }

                resolve(data);
                }, 500);
        }
    }
}
</script>
<style lang="scss">
</style>
