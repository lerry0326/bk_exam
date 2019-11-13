<template>
    <div>
        <el-button @click="transfertooper">备份操作</el-button>
        <el-button @click="transfertoreco">备份记录</el-button>
        <el-table :data="tableData" stripe style="width: 100%">
            <el-table-column prop="name" label="序号" width="80"></el-table-column>
            <el-table-column prop="name" label="IP" width="180"></el-table-column>
            <el-table-column prop="status" label="文件列表" width="180"></el-table-column>
            <el-table-column prop="type" label="文件数量"></el-table-column>
            <el-table-column prop="status" label="文件大小" width="180"></el-table-column>
            <el-table-column prop="type" label="备份时间"></el-table-column>
            <el-table-column prop="status" label="备份人" width="180"></el-table-column>
            <el-table-column prop="type" label="JOB链接"></el-table-column>
        </el-table>
    </div>
</template>
<script>
export default {
    data() {
        return {}
    },
    methods: {
        transfertooper() {
            this.$router.replace('/biz_topo')
        },
    }
}
</script>
<style lang="scss">
</style>
