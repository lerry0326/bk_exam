webpackJsonp([12],{QLTy:function(t,e){},liin:function(t,e,o){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var l=o("woOf"),i=o.n(l),s={data:function(){return{biz_options:[],set_options:[],module_options:[],formApply:{business:"",cluster:"",module:"",host:[]},rulesApply:{business:[{required:!0,message:"请选择业务"}]},biz_topo:[],tableData:[]}},created:function(){this.get_biz_options(),this.get_set_by_biz(),this.get_module_by_set(),this.get_host_by_module()},methods:{transfertoreco:function(){this.$router.replace("/bak_reco")},get_biz_options:function(){var t=this;this.$api.getBiz().then(function(e){var o=e.data;t.biz_options=o})},get_set_by_biz:function(){this.getSet({biz_id:this.formApply.business})},getSet:function(t){var e=this,o={};o=i()(o,t),this.$api.getSet(o).then(function(t){e.set_options=t.data})},get_module_by_set:function(){this.getModule({biz_id:this.formApply.business,set_id:this.formApply.cluster})},getModule:function(t){var e=this,o={};o=i()(o,t),this.$api.getModule(o).then(function(t){e.module_options=t.data})},get_host_by_module:function(){this.getHost({biz_id:this.formApply.business,set_id:this.formApply.cluster,module_id:this.formApply.module})},getHost:function(t){var e=this,o={};o=i()(o,t),this.$api.getHost(o).then(function(t){for(var o=0;o<t.data.length;o++)console.log(3333333333,t.data[o]),e.formApply.host.push(t.data[o]),e.formApply.host.push("\n")})},get_topo_by_biz:function(){this.getTopo({biz_id:this.formApply.business})},getTopo:function(t){var e=this,o={};o=i()(o,t),this.$api.getTopo(o).then(function(t){e.biz_topo=t.data})},handleCheckChange:function(t,e,o){console.log(t,e,o)},handleNodeClick:function(t){console.log(t)},loadNode:function(t,e){var o,l=this;return 0===t.level?e([{name:this.biz_topo.bk_obj_name},{name:this.biz_topo.bk_obj_name}]):t.level>3?e([]):(o=t.data.name===this.biz_topo.bk_obj_name||t.data.name!==this.biz_topo.bk_obj_name&&Math.random()>.5,void setTimeout(function(){var t;t=o?[{name:l.biz_topo.bk_obj_name},{name:l.biz_topo.bk_obj_name}]:[],e(t)},500))}}},n={render:function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",[o("el-button",{on:{click:t.transfertooper}},[t._v("备份操作")]),t._v(" "),o("el-button",{on:{click:t.transfertoreco}},[t._v("备份记录")]),t._v(" "),o("el-form",{ref:"form",attrs:{"label-width":"120px",model:t.formApply,rules:t.rulesApply}},[o("el-form-item",{attrs:{label:"业务"}},[o("el-select",{attrs:{placeholder:"请选择"},on:{change:function(e){t.get_set_by_biz()}},model:{value:t.formApply.business,callback:function(e){t.$set(t.formApply,"business",e)},expression:"formApply.business"}},t._l(t.biz_options,function(t){return o("el-option",{key:t.bk_biz_id,attrs:{label:t.bk_biz_name,value:t.bk_biz_id}})}))],1),t._v(" "),o("el-form-item",{attrs:{label:"集群"}},[o("el-select",{attrs:{placeholder:"请选择集群"},on:{change:function(e){t.get_module_by_set()}},model:{value:t.formApply.cluster,callback:function(e){t.$set(t.formApply,"cluster",e)},expression:"formApply.cluster"}},t._l(t.set_options,function(t){return o("el-option",{key:t.bk_set_id,attrs:{label:t.bk_set_name,value:t.bk_set_id}})}))],1),t._v(" "),o("el-form-item",{attrs:{label:"模块"}},[o("el-select",{attrs:{placeholder:"请选择模块"},on:{change:function(e){t.get_host_by_module()}},model:{value:t.formApply.module,callback:function(e){t.$set(t.formApply,"module",e)},expression:"formApply.module"}},t._l(t.module_options,function(t){return o("el-option",{key:t.bk_module_id,attrs:{label:t.bk_module_name,value:t.bk_module_id}})}))],1),t._v(" "),o("el-form-item",{attrs:{label:"主机"}},[o("el-input",{attrs:{type:"textarea"},model:{value:t.formApply.host,callback:function(e){t.$set(t.formApply,"host",e)},expression:"formApply.host"}})],1)],1),t._v(" "),o("div",{staticClass:"search"},[o("span",{staticClass:"aglin"},[t._v("目录：")]),t._v(" "),o("el-input",{staticClass:"aglin-input",staticStyle:{width:"30%"},attrs:{size:"mini",clearable:"",placeholder:"请输入内容"},model:{value:t.inputEmpName,callback:function(e){t.inputEmpName=e},expression:"inputEmpName"}}),t._v(" "),o("span",{staticClass:"aglin"},[t._v("文件名：")]),t._v(" "),o("el-input",{staticClass:"aglin-input",staticStyle:{width:"30%"},attrs:{size:"mini",clearable:"",placeholder:"请输入内容"},model:{value:t.inputEmpName,callback:function(e){t.inputEmpName=e},expression:"inputEmpName"}}),t._v(" "),o("el-button",{attrs:{size:"mini",type:"primary"},nativeOn:{click:function(e){return t.search(e)}}},[t._v("立即搜索")])],1),t._v(" "),o("el-table",{staticStyle:{width:"100%"},attrs:{data:t.tableData,stripe:""}},[o("el-table-column",{attrs:{prop:"name",label:"序号",width:"80"}}),t._v(" "),o("el-table-column",{attrs:{prop:"name",label:"IP",width:"180"}}),t._v(" "),o("el-table-column",{attrs:{prop:"status",label:"文件列表",width:"180"}}),t._v(" "),o("el-table-column",{attrs:{prop:"type",label:"文件数量"}}),t._v(" "),o("el-table-column",{attrs:{prop:"status",label:"文件总大小",width:"180"}}),t._v(" "),o("el-table-column",{attrs:{prop:"type",label:"操作"}})],1)],1)},staticRenderFns:[]};var a=o("VU/8")(s,n,!1,function(t){o("QLTy")},null,null);e.default=a.exports}});
//# sourceMappingURL=12.js.map