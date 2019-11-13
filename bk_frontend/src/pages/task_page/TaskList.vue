<template>
    <div class="apply_control">
        <el-button @click="index">首页</el-button>
        <div class="fitter">
            <div style="width: 30%;display: inline-block">
                <el-input size="medium" placeholder="请输入任务名称" v-model="search_name" class="input-with-select">
                    <el-button slot="append" @click="get_task_by_name()"
                               icon="el-icon-search"></el-button>
                </el-input>
            </div>
            <div style="float: right;">
                <el-button type="primary" @click="create()">新建申请</el-button>
            </div>
        </div>
        <el-divider></el-divider>
        <div class="table">
            <el-table
                    stripe
                    :height=tableHeight
                    ref="table"
                    :data="tableData"
                    border
                    style="width: 100%">
                <el-table-column
                        label="任务类型">
                    <template slot-scope="scope">
                        <span v-if="scope.row.type==1">权限申请</span>
                        <span v-else-if="scope.row.type==2">权限修改</span>
                        <span v-else-if="scope.row.type==3">权限回收</span>
                    </template>
                </el-table-column>
                <el-table-column
                        prop="name"
                        label="任务名称">
                </el-table-column>
                <el-table-column
                        prop="employee.name"
                        label="职员名称">
                </el-table-column>
                <el-table-column
                        prop="institution.police_resp"
                        label="申请人">
                </el-table-column>
                <el-table-column
                        label="状态">
                    <template slot-scope="scope">
                        <span class="el-tag el-tag--warning el-tag--light" v-if="scope.row.status==1">草稿</span>
                        <span class="el-tag el-tag--primary el-tag--light" v-else-if="scope.row.status==2">待审批</span>
                        <span class="el-tag el-tag--danger el-tag--light" v-else-if="scope.row.status==3">已驳回</span>
                        <span class="el-tag el-tag--success el-tag--light" v-else-if="scope.row.status==4">已审批</span>
                    </template>
                </el-table-column>
                <el-table-column
                        prop="reject_reason"
                        label="审批意见">
                </el-table-column>
                <el-table-column
                        label="申请时间"
                        prop="create_time">
                </el-table-column>
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
                        <el-button @click="detail_apply_task(scope.row)" type="text" size="small">详情</el-button>
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
        <pagination
                style=" position: relative;margin-top: 20px;float: right;"
                :total="totalNumber"
                @page-size-change="pageSizeChange">
        </pagination>
        <div style="height: 20px">
        </div>
        <new-edit ref="newEdit" :show_save="show_save" title="填写申请信息" @handle-save="handleSave"
                  @handle-success="handleSuccess"
                  dialog-action="dialogAction"
                  width="30">
            <div slot="dialog-content">
                <el-form ref="refformScene" label-width="120px"
                         :model="formApply" :rules="rulesApply">
                    <el-form-item label="任务名称" prop="name">
                        <el-input class="form-content" v-model="formApply.name"></el-input>
                    </el-form-item>
                    <el-form-item label="外协机构" prop="institution">
                        <el-select @change="get_user_by_firm()" style="width: 85%" v-model="formApply.institution"
                                   placeholder="请选择">
                            <el-option
                                    v-for="item in options"
                                    :key="item.id"
                                    :label="item.name"
                                    :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="职员名称" prop="employee">
                        <el-select style="width: 85%" class="form-content" v-model="formApply.employee"
                                   @change="change_username">
                            <el-option
                                    v-for="item in emloyee_options"
                                    :key="item.id"
                                    :label="item.name"
                                    :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="申请类别" prop="apply_type">
                        <el-checkbox-group v-model="formApply.apply_type" @change="change_type">
                            <el-checkbox label="4A" name="type"></el-checkbox>
                            <el-checkbox label="HAC" name="type"></el-checkbox>
                            <el-checkbox label="AD" name="type"></el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>
                    <div v-for="(i, index) in  formApply.apply_type" :key="index">
                        <el-form-item v-show=" '4A' == i" label="" prop="type">
                            <div style="padding:10px 10px;box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)">
                                <span>4A账号信息：</span>
                                <div>
                                    <label style="display:inline-block;width: 60px">用户名</label>
                                    <el-input placeholder="请输入用户名,长度不小于7" style="width:80%;margin-bottom: 10px"
                                              v-model="formApply.foura_username"></el-input>
                                </div>
                                <div>
                                    <label style="display:inline-block;width: 60px">密码</label>
                                    <el-input show-password placeholder="请输入密码" style="width:80%;margin-bottom: 10px"
                                              v-model="formApply.foura_password"></el-input>
                                </div>
                                <div>
                                    <label style="display:inline-block;width: 60px"> 业务系统</label>
                                    <el-select style="width: 80%" v-model="formApply.foura_access_system" multiple
                                               placeholder="请选择">
                                        <el-option
                                                v-for="item in foura_options"
                                                :key="item.value"
                                                :label="item.label"
                                                :value="item.value">
                                        </el-option>
                                    </el-select>
                                </div>
                            </div>
                        </el-form-item>
                        <el-form-item v-show=" 'HAC' == i" label="" prop="type">
                            <div style="padding:10px 10px;box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)">
                                <span>HAC账号信息：</span>
                                <div>
                                    <label style="display:inline-block;width: 60px">用户名</label>
                                    <el-input placeholder="请输入用户名,,长度不小于7" style="width:80%;margin-bottom: 10px"
                                              v-model="formApply.hac_username"></el-input>
                                </div>
                                <div>
                                    <label style="display:inline-block;width: 60px">密码</label>
                                    <el-input show-password placeholder="请输入密码" style="width:80%;margin-bottom: 10px"
                                              v-model="formApply.hac_password"></el-input>
                                </div>
                                <div>
                                    <label style="display:inline-block;width: 60px">授权设备组</label>
                                    <el-select style="width: 80%" v-model="formApply.hac_available_server" multiple
                                               placeholder="请选择">
                                        <el-option
                                                v-for="item in hac_options"
                                                :key="item.value"
                                                :label="item.label"
                                                :value="item.value">
                                        </el-option>
                                    </el-select>
                                </div>
                            </div>
                        </el-form-item>
                        <el-form-item v-show=" 'AD' == i" label="" prop="type">
                            <div style="padding:10px 10px;box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)">
                                <span>AD账号信息：</span>
                                <div>
                                    <label style="display:inline-block;width: 60px">用户名</label>
                                    <el-input placeholder="请输入用户名,,长度不小于7" style="width:80%;margin-bottom: 10px"
                                              v-model="formApply.ad_username"></el-input>
                                </div>
                                <div>
                                    <label style="display:inline-block;width: 60px">密码</label>
                                    <el-input show-password placeholder="请输入密码,规则为英文+!+数字"
                                              style="width:80%;margin-bottom: 10px"
                                              v-model="formApply.ad_password"></el-input>
                                </div>
                                <div>
                                    <label style="display:inline-block;width: 60px">授权所属组</label>
                                    <el-select style="width: 80%" v-model="formApply.ad_group" multiple
                                               placeholder="请选择">
                                        <el-option
                                                v-for="item in ad_options"
                                                :key="item"
                                                :label="item"
                                                :value="item">
                                        </el-option>
                                    </el-select>
                                </div>
                            </div>
                        </el-form-item>
                    </div>
                </el-form>
            </div>
        </new-edit>
        <el-drawer
                size="45%"
                title="详情"
                :visible.sync="drawer">
            <div class="demo-drawer__content" style="margin: 5% 5%;height: 500px;overflow-y: auto">
                <el-form :inline="true" :model="formApply">
                    <el-form-item style="width: 45%" label="任务名称：" label-width="100">
                        <span>{{formApply.name}}</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="申请类型：" label-width="100">
                        <span v-if="formApply.type=='1'">权限申请</span>
                        <span v-if="formApply.type=='2'">权限修改</span>
                        <span v-if="formApply.type=='3'">权限回收</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="申请时间：" label-width="100">
                        <span>{{formApply.create_time}}</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="职员名称：" label-width="100">
                        <span>{{formApply.employee.name}}</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="专业：" label-width="100">
                        <span>{{formApply.employee.role}}</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="成绩：" label-width="100">
                        <span>{{formApply.employee.score}}</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="证书：" label-width="100">
                        <span>{{formApply.employee.certification}}</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="外协机构：" label-width="100">
                        <span>{{formApply.institution.name}}</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="申请人：" label-width="100">
                        <span>{{formApply.institution.police_resp}}</span>
                    </el-form-item>

                    <el-form-item style="width: 45%" label="状态：" label-width="100">
                        <span v-if="formApply.status==1">待申请</span>
                        <span v-else-if="formApply.status==2">待审批</span>
                        <span v-else-if="formApply.status==3">已驳回</span>
                        <span v-else-if="formApply.status==4">已审批</span>
                    </el-form-item>
                    <el-form-item style="width: 90%" label="审批意见：" label-width="100">
                        <span>{{formApply.reject_reason}}</span>
                    </el-form-item>
                    <el-form-item v-show="formApply.foura_access_system !== '[]'" style="width: 90%" label="4A账号："
                                  label-width="100">

                        <span>{{formApply.foura_username}}</span>

                    </el-form-item>
                    <el-form-item v-show="formApply.foura_access_system !== '[]'" style="width: 90%" label="业务系统："
                                  label-width="100">
                        <div class="el-textarea" style="display: inline-block;line-height: normal;width: 400px">
                            <span v-if="formApply.foura_access_system">{{formApply.foura_access_system.toString().replace('[','').replace(']','')}}</span>
                        </div>
                    </el-form-item>
                    <el-form-item v-show="formApply.hac_available_server !== '[]'" style="width: 90%" label="HAC账号："
                                  label-width="100">
                        <span>{{formApply.hac_username}}</span>
                    </el-form-item>
                    <el-form-item v-show="formApply.hac_available_server !== '[]'" style="width: 90%" label="授权设备组："
                                  label-width="100">
                        <div class="el-textarea" style="display: inline-block;line-height: normal;width:400px">
                            <span v-if="formApply.hac_available_server">{{formApply.hac_available_server.toString().replace('[','').replace(']','')}}</span>
                        </div>
                    </el-form-item>
                    <el-form-item v-show="formApply.ad_group !== '[]'" style="width: 90%" label="AD账号："
                                  label-width="100">
                        <span>{{formApply.ad_username}}</span>
                    </el-form-item>
                    <el-form-item v-show="formApply.ad_group !== '[]'" style="width: 90%" label="授权所属组："
                                  label-width="100">
                        <div class="el-textarea" style="display: inline-block;line-height: normal;width: 400px">
                            <span v-if="formApply.ad_group">{{formApply.ad_group.toString().replace('[','').replace(']','')}}</span>
                        </div>
                    </el-form-item>

                </el-form>
            </div>
        </el-drawer>
    </div>
</template>
<script>
    import Container from '../../components/layout/container';
    import Pagination from '@/components/Pagination'
    import NewEdit from '@/components/NewEdit'
    import * as commonValidate from '@/common/js/validate'
    // import pinyin from '../../../static/js/Convert_Pinyin.js'

    // const utils = require('../../../static/js/Convert_Pinyin.js')
    export default {
        components: {'pagination': Pagination, 'new-edit': NewEdit},
        data() {
            let validate = (rule, value, callback) => {
                //后台方法
                let parmas = {
                    id: this.formApply.employee
                }
                this.$store.dispatch('applytask/is_pass', parmas).then(res => {
                        if (!res.result) {
                            callback(new Error(res.message))
                        }
                    }
                )
            }
            return {
                // pinyin: pinyin,
                show_save: true,
                action: 'create',
                drawer: false,
                tableHeight: window.innerHeight - 245,
                tableData: [],
                totalNumber: 0,
                currentPage: 1,
                pageSize: 10,
                options: [],
                foura_options: [],
                hac_options: [],
                ad_options: [],
                emloyee_options: [],
                search_name: '',
                formApply: {
                    apply_type: [],
                    name: '',
                    status: '',
                    employee: '',
                    institution: '',
                    foura_access_system: [],
                    hac_available_server: [],
                    ad_group: [],
                    ad_username: '',
                    ad_password: '',
                    foura_username: '',
                    foura_password: '',
                    hac_username: '',
                    hac_password: '',
                },
                rulesApply: {
                    name: [
                        {required: true, message: '请输入名称'},
                        {max: 20, message: '长度在20个字符之内'},
                        {validator: commonValidate.validateChName}
                    ],
                    employee: [
                        {required: true, message: '请输入职员名称'},
                        {validator: validate}
                    ],
                    institution: [
                        {required: true, message: '请选择外协机构'},
                    ],
                    apply_type: [
                        {required: true, message: '请选择申请类别'},
                    ],
                },
            }
        },
        created() {
            this.get_emloyee()
            this.get_task()
            this.get_firm()
            this.get_ad_options()
        },
        methods: {
            get_user_by_firm() {
                this.get_emloyee({institution: this.formApply.institution})
            },
            change_username(value) {
                let obj = {};
                obj = this.emloyee_options.find((item) => {
                    return item.id === value;
                });
                let getName = ''
                getName = obj.name;
                if (obj.ad_username !== null) { //用已经申请的用户名
                    this.formApply.ad_username = obj.ad_username
                } else { //如果都没有，就表明是空的，默认给用户加一个
                    // this.formApply.ad_username = utils.PINYIN.getFullChars(getName).length < 7 ? utils.PINYIN.getFullChars(getName) + utils.PINYIN.getFullChars(getName) : utils.PINYIN.getFullChars(getName)
                }
                if (obj.foura_username !== null) {
                    this.formApply.foura_username = obj.foura_username
                } else {
                    // this.formApply.foura_username = utils.PINYIN.getFullChars(getName).length < 7 ? utils.PINYIN.getFullChars(getName) + utils.PINYIN.getFullChars(getName) : utils.PINYIN.getFullChars(getName)
                }
                if (obj.hac_username !== null) {
                    this.formApply.hac_username = obj.hac_username
                } else {
                    // this.formApply.hac_username = utils.PINYIN.getFullChars(getName).length < 7 ? utils.PINYIN.getFullChars(getName) + utils.PINYIN.getFullChars(getName) : utils.PINYIN.getFullChars(getName)
                }
                if (obj.ad_password !== null) { //用已经申请的用户名
                    this.formApply.ad_password = obj.ad_password
                } else { //如果都没有，就表明是空的，默认给用户加一个
                    this.formApply.ad_password = this.formApply.ad_username + '!1234'
                }
                if (obj.foura_password !== null) {
                    this.formApply.foura_password = obj.foura_password
                } else {
                    this.formApply.foura_password = this.formApply.foura_username + '!1234'
                }
                if (obj.hac_password !== null) {
                    this.formApply.hac_password = obj.hac_password
                } else {
                    this.formApply.hac_password = this.formApply.hac_username + '!1234'
                }
                let institutionObj = this.options.find((item) => {
                    return item.name === obj.institution;
                });
                this.formApply.institution = institutionObj.id
            },
            change_type(value) {
                this.formApply.apply_type = value
            },
            get_ad_options() {
                let params = {}
                this.$store.dispatch('ad/getAd', params).then(res => {
                        this.ad_options = res.groups
                    }
                )
            },
            approve_apply(row) {
                this.$router.replace('/approve_apply/' + row.id)
            },
            send_apply_task(row) {
                this.$confirm('确定发起？')
                    .then(_ => {
                        this.loading = true;
                        setTimeout(() => {
                            this.loading = false;
                            let parmas = {
                                id: row.id
                            }
                            this.$store.dispatch('applytask/sendTask', parmas).then(res => {
                                    if (!res.result) {
                                        this.$message({type: 'error', message: '发起失败！'})
                                    } else {
                                        this.$message({type: 'success', message: '发起成功！'})
                                        this.get_task()
                                    }
                                }
                            )
                        }, 500);
                    })
                    .catch(_ => {
                    });
            },
            detail_apply_task(row) {
                this.formApply = JSON.parse(JSON.stringify(row))
                this.formApply.apply_type = []
                this.drawer = true
            },
            delete_apply_task(row) {
                this.$confirm('确定删除？')
                    .then(_ => {
                        this.loading = true;
                        setTimeout(() => {
                            this.loading = false;
                            let parmas = {
                                id: row.id
                            }
                            this.$store.dispatch('applytask/deleteTask', parmas).then(res => {
                                    if (!res.result) {
                                        this.$message({type: 'success', message: '删除成功！'})
                                        this.get_task()
                                    } else {
                                        this.$message({type: 'error', message: '删除失败！'})
                                    }
                                }
                            )
                        }, 500);
                    })
                    .catch(_ => {
                    });
            },
            modify(row) {
                console.log(row)
                this.action = 'modify'
                this.formApply = JSON.parse(JSON.stringify(row))
                this.formApply.employee = row.employee.id
                this.formApply.institution = row.institution.id
                this.formApply.ad_group = JSON.parse(row.ad_group)
                this.formApply.foura_access_system = JSON.parse(row.foura_access_system)
                this.formApply.hac_available_server = JSON.parse(row.hac_available_server)
                this.$set(this.formApply, 'apply_type', [])
                if (row.ad_group !== '[]') {
                    this.formApply.apply_type.push('AD')
                }
                if (row.foura_access_system !== '[]') {
                    this.formApply.apply_type.push('4A')
                }
                if (row.hac_available_server !== '[]') {
                    this.formApply.apply_type.push('HAC')
                }
                console.log(this.formApply)
                this.show_save = false
                this.$refs['newEdit'].open();
            },
            handleSave(apiParam) {
                if (this.action == 'create') {
                    let params = this.formApply
                    params.ad_group = JSON.stringify(this.formApply.ad_group)
                    params.foura_access_system = JSON.stringify(this.formApply.foura_access_system)
                    params.hac_available_server = JSON.stringify(this.formApply.hac_available_server)
                    //params = Object.assign(params, apiParam)
                    //把不勾选的置null
                    if (!this.formApply.apply_type.includes('AD')) {
                        params.ad_username = null
                        params.ad_password = null
                    }
                    if (!this.formApply.apply_type.includes('HAC')) {
                        params.hac_username = null
                        params.hac_password = null
                    }
                    if (!this.formApply.apply_type.includes('4A')) {
                        params.foura_username = null
                        params.foura_password = null
                    }
                    if (params.employee == null || params.employee == undefined) {
                        this.$message({type: 'error', message: '请选择职员名称！'})
                        return false
                    }
                    if (params.ad_username !== null && params.ad_username.length < 7) {
                        this.$message({type: 'error', message: 'AD用户名长度不能小于7！'})
                        return false
                    }
                    if (params.hac_username !== null && params.hac_username.length < 7) {
                        this.$message({type: 'error', message: 'hac用户名长度不能小于7！'})
                        return false
                    }
                    if (params.foura_username !== null && params.foura_username.length < 7) {
                        this.$message({type: 'error', message: '4A用户名长度不能小于7！'})
                        return false
                    }
                    params.status = 1
                    params.type = 1
                    if (this.formApply.ad_group.length == 0 && this.formApply.foura_access_system.length == 0 && this.formApply.hac_available_server.length == 0) {
                        this.$message({type: 'error', message: '申请权限不能为空！'})
                        return false
                    }
                    this.$store.dispatch('applytask/saveTask', params).then(res => {
                            if (!res.result) {
                                this.$message({type: 'error', message: res.message})
                            } else {
                                this.$message({type: 'success', message: '保存成功！'})
                                this.get_task()
                            }
                        }
                    )
                }
                this.$refs['newEdit'].cancel()
            },
            modify_apply_task(apiParam) {
                let params = JSON.parse(JSON.stringify(this.formApply))
                params = Object.assign(params, apiParam)
                params.ad_group = JSON.stringify(this.formApply.ad_group)
                params.foura_access_system = JSON.stringify(this.formApply.foura_access_system)
                params.hac_available_server = JSON.stringify(this.formApply.hac_available_server)
                params.institution = Object.prototype.toString.call(this.formApply.institution) === '[object Object]' ? this.formApply.institution.id : this.formApply.institution
                params.employee = Object.prototype.toString.call(this.formApply.employee) === '[object Object]' ? this.formApply.employee.id : this.formApply.employee
                params.type = 1
                console.log(params)
                this.$store.dispatch('applytask/modifyTask', params).then(res => {
                        if (res.result == false) {
                            this.$message({type: 'error', message: '编辑失败！' + res.message})
                        } else {
                            this.$message({type: 'success', message: '编辑成功！'})
                            this.get_task()
                        }
                    }
                )
            },
            get_emloyee(apiParam) {
                let params = {}
                params = Object.assign(params, apiParam)
                this.$store.dispatch('employee/getEmployee', params).then(res => {
                        this.emloyee_options = res.items
                    }
                )
            },
            get_firm() {
                this.$store.dispatch('operationfirm/getFirm', {}).then(res => {
                        this.options = res.items
                    }
                )
            },
            pageSizeChange(val) {
                this.currentPage = val.currentPage
                this.pageSize = val.pageSize
                this.get_task({page: this.currentPage, page_size: this.pageSize})
            },
            leaveTab(val) {
                let res = true
                this.$refs.refScene.validate((valid) => {
                    if (!valid) {
                        res = false
                    } else {
                        res = true
                    }
                })
                return res
            },
            handleSuccess() {
                if (this.action == 'create') {
                    this.create_apply_task()
                } else {
                    this.modify_apply_task()
                }
                this.$refs['newEdit'].cancel()
            },
            index() {
                this.$router.replace('/index')
            },
            create_apply_task(apiParam) {
                let params = this.formApply
                params.type = 1
                params.ad_group = JSON.stringify(this.formApply.ad_group)
                params.foura_access_system = JSON.stringify(this.formApply.foura_access_system)
                params.hac_available_server = JSON.stringify(this.formApply.hac_available_server)
                params = Object.assign(params, apiParam)
                //把不勾选的置空
                if (!this.formApply.apply_type.includes('AD')) {
                    params.ad_username = null
                    params.ad_password = null
                }
                if (!this.formApply.apply_type.includes('HAC')) {
                    params.hac_username = null
                    params.hac_password = null
                }
                if (!this.formApply.apply_type.includes('4A')) {
                    params.foura_username = null
                    params.foura_password = null
                }
                if (params.ad_username !== null && params.ad_username.length < 7) {
                    this.$message({type: 'error', message: 'AD用户名长度不能小于7！'})
                    return false
                }
                if (params.hac_username !== null && params.hac_username.length < 7) {
                    this.$message({type: 'error', message: 'hac用户名长度不能小于7！'})
                    return false
                }
                if (params.foura_username !== null && params.foura_username.length < 7) {
                    this.$message({type: 'error', message: '4A用户名长度不能小于7！'})
                    return false
                }
                if (this.formApply.ad_group.length == 0 && this.formApply.foura_access_system.length == 0 && this.formApply.hac_available_server.length == 0) {
                    this.$message({type: 'error', message: '申请权限不能为空！'})
                    return false
                }
                this.$store.dispatch('applytask/createTask', params).then(res => {
                        console.log(res)
                        if (res.result == false) {
                            this.$message({type: 'error', message: '新建失败！' + res.message})
                        } else {
                            this.$message({type: 'success', message: '新建成功！'})
                            this.get_task()
                        }
                    }
                )
            },
            create() {
                this.action = 'create'
                this.show_save = true
                let date = new Date()
                this.formApply = {
                    name: '权限申请' + date.getFullYear() + (date.getMonth() + 1) + date.getDate(),
                    status: 2,
                    employee: '',
                    institution: '',
                    apply_type: [],
                    foura_access_system: [],
                    hac_available_server: [],
                    ad_group: [],
                    ad_username: '',
                    ad_password: '',
                    foura_username: '',
                    foura_password: '',
                    hac_username: '',
                    hac_password: '',
                }
                this.$refs['newEdit'].open();
            },
            get_task(apiParam) {
                let params = {
                    page: this.currentPage,
                    page_size: this.pageSize,
                    name: this.search_name
                }
                params = Object.assign(params, apiParam)
                this.$store.dispatch('applytask/getTask', params).then(res => {
                        this.totalNumber = res.count
                        this.tableData = res.items
                    }
                )
            },
            get_task_by_name() {
                this.get_task({name__contains: this.search_name})
            }
        },
    }
</script>
<style lang='scss'>
    .apply_control {
        padding: 10px 10px;
        .fitter {
            padding: 0px 0px !important;
        }
        .el-divider--horizontal {
            margin: 10px 0 !important;
        }
        .el-form-item__content {
            width: 70%;
        }
    }

    .table {
        .el-table {
            border-top: 1px solid rgb(235, 238, 245);
        }
    }

</style>
