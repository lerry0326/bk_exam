<template>
    <div class="employee">
        <el-button @click="transferto">任务列表页</el-button>
        <div class="search">
            <span class="aglin">姓名：</span>
            <el-input style="width: 30%" class="aglin-input" size="mini" v-model="inputEmpName" clearable
                      placeholder="请输入内容"></el-input>
            <el-button size="mini" type="primary" @click.native="search">查询</el-button>
            <el-button size="mini" @click.native="reset">重置</el-button>
            <div class="new" style="float: right;margin-bottom: 20px">
                <el-button size="mini" type="primary" @click="handleNew">添加</el-button>
                <el-button size="mini" type="primary" @click="handleDeleteAll" id="deleteAll">删除
                </el-button>
                <!--<el-button size="mini" type="primary" @click="handleUpdate">编辑</el-button>-->
                <el-button size="mini" type="primary" @click="handleImport">导入</el-button>
                <el-button size="mini" type="primary" @click="handleExport">导出</el-button>
            </div>
        </div>
        <div class="table">
            <el-table
                    row-key="id"
                    stripe
                    ref=""
                    :data="data"
                    v-loading="loadingEmployee"
                    style="width: 100%"
                    :height=tableHeight
                    @select-all="select_all"
                    @selection-change="handleSelectionChange">
                <el-table-column
                        reserve-selection
                        type="selection"
                        show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                        prop="name"
                        label="姓名"
                        show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                        prop="role"
                        label="职位"
                        show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                        prop="institution"
                        label="外协机构"
                        show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                        prop="score"
                        label="成绩"
                        show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                        prop="major"
                        label="专业"
                        show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                        prop="certification"
                        label="证书"
                        show-overflow-tooltip>
                </el-table-column>
                <el-table-column
                        prop="handle"
                        label="操作"
                        fixed="right"
                        width="150">
                    <template slot-scope="scope">
                        <el-button type="text" @click="handleEdit(scope)">编辑</el-button>
                        <el-button type="text" @click="handleDetail(scope.row)">详情</el-button>
                        <el-button type="text" @click="handleDelete(scope)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <pagination
                style=" position: relative;margin-top: 20px;float: right"
                :total="totalNumber"
                @page-size-change="pageSizeChange">
        </pagination>
        <div style="height: 20px">
        </div>
        <new-edit ref="newEdit" :title="title" @handle-success="handleSuccess" dialog-action="dialogAction"
                  :width="width">
            <div slot="dialog-content">
                <el-tabs v-model="activeName" :before-leave="leaveTab">
                    <el-tab-pane label="角色信息" name="first">
                        <el-form ref="refformEmployee" :label-position="labelPosition" label-width="120px"
                                 :model="formEmployee" :rules="rulesGroups">
                            <el-form-item label="姓名" prop="name">
                                <el-input class="form-content" v-model="formEmployee.name"></el-input>
                            </el-form-item>
                            <el-form-item label="身份证号" prop="ID_card">
                                <el-input class="form-content" v-model="formEmployee.ID_card"></el-input>
                            </el-form-item>
                            <el-form-item label="手机号" prop="phone_number">
                                <el-input class="form-content"
                                          v-model="formEmployee.phone_number"></el-input>
                            </el-form-item>
                            <el-form-item label="职位" prop="role">
                                <el-input class="form-content" v-model="formEmployee.role"></el-input>
                            </el-form-item>
                            <el-form-item label="外协机构" prop="institution">
                                <!--<el-input class="form-content" size="mini"
                                          v-model="formEmployee.institution"></el-input>-->
                                <el-select style="width: 85%" v-model="formEmployee.institution" placeholder="请选择">
                                    <el-option
                                            v-for="item in firm_options"
                                            :key="item.id"
                                            :label="item.name"
                                            :value="item.id">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="成绩" prop="score">
                                <el-input class="form-content" v-model="formEmployee.score"></el-input>
                            </el-form-item>
                            <el-form-item label="专业" prop="major">
                                <el-input class="form-content" v-model="formEmployee.major"></el-input>
                            </el-form-item>
                            <el-form-item label="证书">
                                <el-input class="form-content" type="textarea"
                                          v-model="formEmployee.certification"></el-input>
                            </el-form-item>
                        </el-form>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </new-edit>
        <new-edit ref="newImport" :title="title" @handle-success="handleSuccess" dialog-action="dialogAction"
                  :width="width">
            <div slot="dialog-content">
                <el-tabs v-model="activeName" :before-leave="leaveTab">
                    <!--<el-input class="form-content" v-model="formEmployee.name"-->
                    <!--type="file"></el-input>-->
                    <el-button size="small" type="primary" @click="downTemplate">下载模板</el-button>
                    <el-upload
                            name="employee_file"
                            class="upload-demo"
                            action="/person/api/employee/import_employee_info/"
                            :on-preview="handlePreview"
                            :on-remove="handleRemove"
                            :on-success="upload_success"
                            multiple
                            :headers="headers"
                            :limit="10"
                            style="display: inline">
                        <el-button size="small" type="primary">点击上传</el-button>
                        <!--<div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>-->
                    </el-upload>
                </el-tabs>
            </div>
        </new-edit>
        <new-edit ref="newUpdate" :title="title" @handle-success="handleSuccess" dialog-action="dialogAction"
                  :width="width">
            <div slot="dialog-content">
                <el-tabs v-model="activeName" :before-leave="leaveTab">
                    <el-tab-pane label="角色信息" name="first">
                        <el-form ref="refformEmployee" :label-position="labelPosition" label-width="120px"
                                 :model="formEmployee" :rules="rulesGroups">
                            <el-form-item label="姓名" prop="name">
                                <el-input class="form-content" v-model="formEmployee.name"></el-input>
                            </el-form-item>
                            <el-form-item label="职位" prop="display_name">
                                <el-input class="form-content"
                                          v-model="formEmployee.role"></el-input>
                            </el-form-item>
                            <el-form-item label="外协机构" prop="display_name">
                                <!--<el-input class="form-content" size="mini"
                                          v-model="formEmployee.institution"></el-input>-->
                                <el-select class="form-content" v-model="formEmployee.institution" placeholder="请选择">
                                    <el-option
                                            v-for="item in firm_options"
                                            :key="item.id"
                                            :label="item.name"
                                            :value="item.id">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="成绩" prop="display_name">
                                <el-input class="form-content"
                                          v-model="formEmployee.score"></el-input>
                            </el-form-item>
                            <el-form-item label="证书">
                                <el-input class="form-content" type="textarea"
                                          v-model="formEmployee.certification"></el-input>
                            </el-form-item>
                        </el-form>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </new-edit>
        <el-drawer
                size="40%"
                title="详情"
                :visible.sync="drawer">
            <div class="demo-drawer__content" style="margin: 5% 5%">
                <el-form :inline="true" :model="formEmployee" :label-position="labelPosition" label-width="100px">
                    <el-form-item style="width: 45%" label="姓名：">
                        <span>{{formEmployee.name}}</span>
                    </el-form-item>
                    <el-form-item style="width: 50%" label="身份证号：">
                        <span>{{formEmployee.ID_card}}</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="手机号：">
                        <span>{{formEmployee.phone_number}}</span>
                    </el-form-item>
                    <el-form-item style="width: 50%" label="职位：">
                        <span>{{formEmployee.role}}</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="外协机构：">
                        <span>{{formEmployee.institution}}</span>
                    </el-form-item>
                    <el-form-item style="width: 50%" label="成绩：">
                        <span>{{formEmployee.score}}</span>
                    </el-form-item>
                    <el-form-item style="width: 45%" label="专业：">
                        <span>{{formEmployee.major}}</span>
                    </el-form-item>
                    <el-form-item style="width: 50%" label="证书：">
                        <span>{{formEmployee.certification}}</span>
                    </el-form-item>
                </el-form>
            </div>
        </el-drawer>
    </div>
</template>

<script>
    import Pagination from '@/components/Pagination'
    import NewEdit from '@/components/NewEdit'
    import * as commonValidate from '@/common/js/validate'
    import * as commonMethods from '@/common/js/common'

    export default {
        components: {
            'pagination': Pagination,
            'new-edit': NewEdit,
        },
        data() {
            return {
                tableHeight: window.innerHeight - 248,
                headers: {},
                is_select_all: false,
                firm_options: [],
                drawer: false,
                inputEmpName: '',
                title: '',
                dialogAction: '',
                activeName: 'first',
                width: '40%',
                institutionValue: undefined,
                empName: '',
                empRole: '',
                empInstitution: '',
                empScore: '',
                empMajor: '',
                empCertification: '',
                labelPosition: 'right',
                totalNumber: 0,
                currentPage: 1,
                pageSize: 10,
                loadingEmployee: false,
                loadingLeft: false,
                loadingRight: false,
                cacheLeftData: [], // 左侧缓存数据
                cacheRightData: [], // 右侧缓存数据
                data: [],
                multipleSelection: [],
                leftData: [],
                rightData: [],
                //fileList: [{name: 'food.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'}, {name: 'food2.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'}],
                formEmployee: {
                    name: '',
                    role: '',
                    institution: '',
                    score: '',
                    major: '',
                    certification: '',
                    ID_card: '',
                    phone_number: '',
                },
                options: [{
                    value: '选项1',
                    label: '嘉为'
                }, {
                    value: '选项2',
                    label: '中软'
                }, {
                    value: '选项3',
                    label: '腾讯'
                }],
                value: '',
                rulesGroups: {
                    name: [
                        {required: true, message: '请输入姓名'},
                        {max: 20, message: '长度在20个字符之内'},
                        {validator: commonValidate.validateChName}
                    ],
                    ID_card: [
                        {required: true, message: '请输入身份证号'},
                        {max: 20, message: '长度在20个字符之内'},
                        {validator: commonValidate.validateNameUnderline}
                    ],
                    phone_number: [
                        {required: true, message: '请输入手机号'},
                        {max: 11, message: '请输入正确的手机号'},
                        {validator: commonValidate.matchPhoneNum}
                    ],
                    role: [
                        {required: true, message: '请输入职位'},
                        {validator: commonValidate.validateChName}
                    ],
                    institution: [
                        {required: true, message: '请输入外协机构'},
                        {validator: commonValidate.validateChName}
                    ],
                    score: [
                        {required: true, message: '请输入成绩'},
                    ],
                    major: [
                        {required: true, message: '请输入专业'},
                        {max: 14, message: '长度在14个字符之内'},
                        {validator: commonValidate.validateChName}
                    ],
                    certification: [
                        {required: true, message: '请输入证书'},
                        {max: 14, message: '长度在14个字符之内'},
                        {validator: commonValidate.validateChName}
                    ],
                },
            }
        },
        created() {
            let xsrfCookieName = 'csrftoken'
            this.getEmployee()
            this.get_firm()
            let regex = new RegExp(xsrfCookieName + '=([^;.]*).*$')
            this.headers = {'X-CSRFToken': document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1]}
        },
        methods: {
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePreview(file) {
                console.log(file);
            },
            downTemplate() {
                window.location.href = window.siteUrl + 'person/api/employee/download_template/'
            },
            select_all(selection) {
                this.is_select_all = !this.is_select_all
            },
            get_firm(apiParam) {
                this.$store.dispatch('operationfirm/getFirm', {}).then(res => {
                        this.firm_options = res.items
                    }
                )
            },
            search() {
                let params = {
                    page: this.currentPage,
                    page_size: this.pageSize,
                    name: this.inputEmpName,
                    role: this.empRole,
                    omit: 'menus,permissions'
                }
                this.loadingEmployee = true
                this.$store.dispatch('employee/getEmployee', params).then(res => {
                    if (res.count > 0) {
                        this.loadingEmployee = false
                        this.data = res.items
                        this.totalNumber = res.count
                    } else {
                        this.loadingEmployee = false
                        this.data = res.items
                        this.totalNumber = res.count
                    }
                })
            },
            getEmployee() {
                let params = {
                    page: this.currentPage,
                    page_size: this.pageSize,
                }
                this.$store.dispatch('employee/getEmployee', params).then(res => {
                    console.log(res)
                    if (res.count > 0) {
                        this.data = res.items
                        this.totalNumber = res.count
                    }
                })
            },
            pageSizeChange(val) {
                this.currentPage = val.currentPage
                this.pageSize = val.pageSize
                this.search({page: this.currentPage, page_size: this.pageSize})
            },
            reset() {
                this.inputEmpName = ''
                this.search()
            },
            handleEdit(scope) {
                this.activeName = 'first'
                this.dialogAction = 'edit'
                this.title = '编辑'
                this.$refs['newEdit'].open()
                this.formEmployee = JSON.parse(JSON.stringify(scope.row))
                this.formEmployee.users = this.formEmployee.users.map(item => item.id)
                this.rightData = scope.row.users
                this.leftData = []
                this.getLeftUser()
            },
            leaveTab(val) {
                let res = true
                this.$refs.refformEmployee.validate((valid) => {
                    if (!valid) {
                        res = false
                    } else {
                        res = true
                    }
                })
                return res
            },
            handleNew() {
                this.activeName = 'first'
                this.dialogAction = 'new'
                this.title = '添加'
                this.$refs['newEdit'].open()
                this.$nextTick(() => {
                    this.$refs['refformEmployee'].clearValidate()
                })
                this.leftData = []
                this.rightData = []
                this.getLeftUser()
                this.formEmployee = {}
            },
            handleImport() {
                this.activeName = 'first'
                this.dialogAction = 'import'
                this.title = '导入用户信息'
                this.$refs['newImport'].open()
                this.$nextTick(() => {
                    this.$refs['refformEmployee'].clearValidate()
                })
                this.leftData = []
                this.rightData = []
                this.getLeftUser()
                this.formEmployee = {}
            },
            handleExport() {
                if (this.multipleSelection.length == 0) {
                    this.$message({type: 'error', message: '请选择！'})
                    return
                }
                let params = {
                    'is_checkedall': this.is_select_all,
                    'ids': this.multipleSelection.map(item => item.id)
                }
                window.location.href = window.siteUrl + 'person/api/employee/export_employee_info/?is_checkedall=' + this.is_select_all + '&ids=' + params.ids
                // this.$http({
                //     method: 'POST',
                //     url: 'person/api/employee/export_employee_info/',
                //     data: params,
                //     responseType: 'blob'
                // }).then(res => {
                //     //调用成功，在html中创建一个a元素
                //     let aTag = document.createElement('a');
                //     //创建一个blob对象
                //     let blob = new Blob([res], {
                //         type: 'application/octet-binary',
                //     });
                //     aTag.download = '人员信息.xls';
                //     aTag.href = window.URL.createObjectURL(blob);
                //     aTag.click();
                //     document.body.removeChild(aTag)
                //     window.URL.revokeObjectURL(blob);
                // })
            },
            handleUpdate() {
                this.activeName = 'first'
                this.dialogAction = 'new'
                this.title = '编辑'
                this.$refs['newUpdate'].open()
                this.$nextTick(() => {
                    this.$refs['refformEmployee'].clearValidate()
                })
                this.leftData = []
                this.rightData = []
                this.getLeftUser()
                this.formEmployee = {}
            },
            handleDeleteAll() {
                if (this.multipleSelection.length == 0) {
                    this.$message({type: 'error', message: '请选择！'})
                    return
                }
                this.$confirm('是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    let params = {
                        is_checkedall: this.is_select_all,
                        ids: this.multipleSelection.map(item => item.id)
                    }
                    console.log('params')
                    this.$store.dispatch('employee/batchDeteleEmployee', params).then(res => {
                        if (res.result == false) {
                            this.$message({type: 'error', message: '删除失败'})
                        } else {
                            this.search()
                            this.$message({type: 'success', message: '删除成功'})
                        }
                    })
                })
            },
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            checkboxChange(row) {
                let tipEnable = row.is_enable ? '是否启用' : '是否禁用'
                this.$confirm(tipEnable, '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    if (row.is_enable == true) {
                        let params = {
                            groups: [row.id],
                            enable: true
                        }
                        this.$store.dispatch('group/groupsStatus', params).then(res => {
                            if (res.result) {
                                this.$message({type: 'success', message: '禁用成功'})
                            } else {
                                row.is_enable = !row.is_enable
                                this.$message({type: 'error', message: '禁用失败'})
                            }
                        });
                    } else if (row.is_enable == false) {
                        let params = {
                            groups: [row.id],
                            enable: false
                        }
                        this.$store.dispatch('group/groupsStatus', params).then(res => {
                            if (res.result) {
                                this.$message({type: 'success', message: '启用成功'})
                            } else {
                                row.is_enable = !row.is_enable
                                this.$message({type: 'error', message: '启用失败'})
                            }
                        });
                    }
                }).catch(() => {
                    row.is_enable = !row.is_enable
                    this.$message({type: 'info', message: '调取接口失败'})
                })
            },
            handleAuthority(data) {
                this.$router.push(data)
            },
            handleDetail(row) {
                this.drawer = true
                this.formEmployee = row
                console.log(row);
            },
            transferto() {
                this.$router.replace('/task_list')
            },
            handleSuccess(dialogAction) {
                if (this.dialogAction == 'new') {
                    let params = {
                        name: this.formEmployee.name,
                        role: this.formEmployee.role,
                        institution: this.formEmployee.institution,
                        score: this.formEmployee.score,
                        major: this.formEmployee.major,
                        certification: this.formEmployee.certification,
                        ID_card: this.formEmployee.ID_card,
                        phone_number: this.formEmployee.phone_number
                    }
                    this.$store.dispatch('employee/addEmployee', params).then(res => {
                        if (res.result == false) {
                            this.$message({type: 'error', message: '新建失败！'})
                        } else {
                            this.search()
                            this.$message({type: 'success', message: '新建成功'})
                        }
                        console.log(res)
                    }).catch(() => {
                        this.$message({type: 'info', message: '接口调用失败'})
                    })
                } else if (this.dialogAction == 'edit') {
                    this.rightDataId = this.rightData.map(item => item.id)
                    this.formEmployee.users = this.rightDataId
                    for (let i = 0; i < this.firm_options.length; i++) {
                        if (this.firm_options[i].name == this.formEmployee.institution) {
                            this.formEmployee.institution = this.firm_options[i].id
                        }
                    }
                    let params = this.formEmployee
                    this.$store.dispatch('employee/modifyEmployee', params).then(res => {
                        if (res.result == false) {
                            this.$message({type: 'error', message: '编辑失败'})
                        } else {
                            this.search()
                            this.$message({type: 'success', message: '编辑成功'})
                        }
                    }).catch(() => {
                        this.$message({type: 'info', message: '接口调用失败'})
                    })
                } else if (this.dialogAction == 'import') {
                }
                this.$refs['newEdit'].cancel()
            },
            handleDelete(scope) {
                this.$confirm('是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    let params = {
                        id: scope.row.id
                    }
                    this.$store.dispatch('employee/deteleEmployee', params).then(res => {
                        if (res.result == false) {
                            this.$message({type: 'error', message: '删除失败'})
                        } else {
                            this.search()
                            this.$message({type: 'success', message: '删除成功'})
                        }
                    })
                }).catch(() => {
                    this.$message({type: 'info', message: '已取消'})
                })
            },
            // 左侧所有用户数据
            getLeftUser() {
                this.$store.dispatch('group/getAllUser').then(res => {
                    if (res.result) {
                        if (this.dialogAction == 'new') {
                            this.leftData = res.data
                        } else if (this.dialogAction == 'edit') {
                            this.leftData = res.data.filter((item) => {
                                for (let i of this.rightData) {
                                    if (item.id == i.id) {
                                        return false
                                    }
                                }
                                return true
                            })
                        }
                    }
                })
            },
            // 向右侧添加数据
            turnRightItems() {
                // 合并左侧选中数据和右侧数据
                this.rightData.push.apply(this.rightData, this.cacheLeftData)
                // 删除左侧勾选数据\
                let indexLeft = 0
                for (let i of this.cacheLeftData) {
                    this.leftData.splice(i.rowIndex - indexLeft, 1)
                    indexLeft++
                }
                this.cacheLeftData = []
            },
            // 向左侧添加数据
            turnLeftItems() {
                // 合并左侧选中数据和右侧数据
                this.leftData.push.apply(this.leftData, this.cacheRightData)
                // 删除右侧勾选数据
                let indexRight = 0
                for (let i of this.cacheRightData) {
                    this.rightData.splice(i.indexRight - indexRight, 1)
                    indexRight++
                }
                this.cacheRightData = []
            },
            // 左侧选择项发生变化
            handleLeftChange(val) {
                this.cacheLeftData = val
            },
            // 右侧选择项发生变化
            handleRightChange(val) {
                this.cacheRightData = val
            },
            // 左侧表格的每行数据对象中加入索引字段
            leftRow({row, rowIndex}) {
                row.rowIndex = rowIndex
            },
            // 右侧表格的每行数据对象中加入索引字段
            rightRow({row, rowIndex}) {
                row.rowIndex = rowIndex
            },
            upload_success(response, file, fileList) {
                console.log()
                this.search(fileList)
                this.$refs['newImport'].cancel()
            },
        },
        computed: {
            leftButtonColor() {
                if (this.leftData.length == 0) {
                    return false
                } else {
                    return true
                }
            },
            rightButtonColor() {
                if (this.rightData.length == 0) {
                    return false
                } else {
                    return true
                }
            },
        },
    }
</script>

<style lang="scss">
    .employee {
        height: 100%;
        padding: 10px 10px;
        background: #fff;
        .search {
            height: 50px;
            line-height: 50px;
            .aglin-input {
                width: 60%;
            }
            .new {
                height: 40px;
            }
            .table {
                .el-table {
                    border-top: 1px solid rgb(235, 238, 245);
                }
            }
        }
    }
</style>
