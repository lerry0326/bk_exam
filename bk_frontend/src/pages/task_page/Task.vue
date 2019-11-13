<template>
    <div class='new'>
        <h3>hello task</h3>
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <el-form-item label="审批人">
            <el-input v-model="formInline.user" placeholder="审批人"></el-input>
        </el-form-item>
        <el-form-item label="活动区域">
            <el-select v-model="formInline.region" placeholder="活动区域">
            <el-option label="区域一" value="shanghai"></el-option>
            <el-option label="区域二" value="beijing"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onSubmit">查询</el-button>
        </el-form-item>
        </el-form>
        <div>姓名：
            <el-input v-model="username" placeholder="请输入内容" clearable></el-input>
            <el-button type="primary" icon="el-icon-search">搜索</el-button>
        </div>
        <el-select v-model="value" placeholder="请选择">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
        <el-button type="text" @click="add">添加</el-button>
        <el-button type="text" @click="destroy">删除</el-button>
        <el-form :model="ruleForm" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="任务名称" prop="name">
                <el-input v-model="ruleForm.name"></el-input>
            </el-form-item>
            <el-form-item label="任务状态" prop="status">
                <el-select v-model="ruleForm.status" placeholder="请选择任务状态">
                <el-option label="待审批" value="1"></el-option>
                <el-option label="已审批" value="2"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="任务类型" prop="status">
                <el-select v-model="ruleForm.type" placeholder="请选择任务类型">
                <el-option label="新建" value="1"></el-option>
                <el-option label="编辑" value="2"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="createTask()">创建</el-button>
                <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
        </el-form>
        <el-table :data="tableData" stripe style="width: 100%">
            <el-table-column prop="name" label="任务名称" width="180"></el-table-column>
            <el-table-column prop="status" label="任务状态" width="180"></el-table-column>
            <el-table-column prop="type" label="任务类型"></el-table-column>
        </el-table>
        <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage4"
            :page-sizes="[10, 20, 30, 40]"
            :page-size="10"
            layout="total, sizes, prev, pager, next, jumper"
            :total="totalNumber">
        </el-pagination>
    </div>
</template>
<script>
    export default {
        data() {
            return {
                username: '',
                options: [{
                    value: '选项1',
                    label: '黄金糕'
                    }, {
                    value: '选项2',
                    label: '双皮奶'
                    }, {
                    value: '选项3',
                    label: '蚵仔煎'
                    }, {
                    value: '选项4',
                    label: '龙须面'
                    }, {
                    value: '选项5',
                    label: '北京烤鸭'
                    }],
                value: '',
                totalNumber: 0,
                tableData: [],
                currentPage4: 1,
                formInline: {
                    user: '',
                    region: ''
                },
                ruleForm: {
                    name: '',
                    status: '',
                    type: ''
                },
            }
        },
        created() {
            this.getTask()
        },
        methods: {
            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
            },
            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
            },
            getTask() {
                this.$api.getTaskList().then(res => {
                    console.log(res)
                    if (res.count > 0) {
                        this.tableData = res.items
                        this.totalNumber = res.count
                    }
                })
            },
            createTask() {
                let params = {
                    name: this.ruleForm.name,
                    status: this.ruleForm.status,
                    type: this.ruleForm.type
                }
                this.$api.createTask().then(res => {
                    console.log(11111, res)
                    if (res.result) {
                        alert('submit!');
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },
            add() {
                this.$prompt('请输入邮箱', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
                inputErrorMessage: '邮箱格式不正确'
                }).then(({ value }) => {
                this.$message({
                    type: 'success',
                    message: '你的邮箱是: ' + value
                });
                }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '取消输入'
                });
                });
            },
            destroy() {
                this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                this.$message({
                    type: 'success',
                    message: '删除成功!'
                });
                }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
                });
            },
            onSubmit() {
                console.log('submit!');
            },
        },
    }
</script>
<style lang='scss'>
.new {
    height: 100%;
    padding: 15px 20px 0 20px;
}
</style>
