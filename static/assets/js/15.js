webpackJsonp([15],{Gbpi:function(e,t,s){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=s("BO1k"),r=s.n(a),i=s("woOf"),n=s.n(i),o=s("Dd8w"),l=s.n(o),u=s("cMGX"),c=s("l0np"),h=s("NYxO"),p={components:{pagination:u.a,"new-edit":c.a},data:function(){return{loadingUser:!1,showForm:!0,showAdd:!1,dataUser:[],allUserName:[],notInAppUserName:[],allUser:[],optionsGroup:[],formUser:{username:"",phone:"",email:""},addUserId:"",authUserId:"",rulesUser:{},userDetail:[],userAuthorityList:[],valueGroup:[],stateUser:"",title:"",width:"35%",labelPosition:"120px",totalNumber:0,currentPage:1,pageSize:10}},created:function(){this.getUser(),this.search()},computed:l()({},Object(h.b)("leftmenu",["permissions"])),methods:{getUser:function(e){var t=this,s={page:this.currentPage,page_size:this.pageSize};s=n()(s,e),this.$store.dispatch("user/getTableUser",s).then(function(e){e.result&&(t.totalNumber=e.data.count,t.dataUser=e.data.items)})},show:function(e){13==e.keyCode&&this.getUser()},pageSizeChange:function(e){this.currentPage=e.currentPage,this.pageSize=e.pageSize,this.getUser({page:this.currentPage,page_size:this.pageSize})},handleNewUser:function(){this.showForm=!0,this.formUser={},this.dialogAction="new",this.title="新建",this.$refs.newEdit.open(),this.searchNotInAppUser()},handleAuthority:function(e){var t=this;this.showForm=!1,this.title="权限管理",this.$refs.newEdit.open(),this.authUserId=e.row.id;var s={id:this.authUserId};this.$store.dispatch("user/getUserAuthority",s).then(function(e){e.result&&(t.userAuthorityList=e.data)}),this.$store.dispatch("user/getAllGroup").then(function(e){e.result&&(t.optionsGroup=e.data)})},handleSuccess:function(){var e=this;if(1==this.showForm){var t={id:this.addUserId};this.$store.dispatch("user/addUser",t).then(function(t){t.result?(e.getUser(),e.$message({type:"success",message:"添加用户成功"})):e.$message({type:"error",message:"添加用户失败"})})}else if(0==this.showForm){var s={id:this.authUserId,params:this.userAuthorityList};this.$store.dispatch("user/setUserPerm",s).then(function(t){t.result?(e.getUser(),e.$message({type:"success",message:"设置用户权限成功"})):e.$message({type:"error",message:"设置用户权限失败"})})}this.$refs.newEdit.cancel()},checkboxChange:function(e){var t=this,s=e.is_enable?"是否启用":"是否禁用";this.$confirm(s,"提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){if(1==e.is_enable){var s={users:[e.id],enable:!0};t.$store.dispatch("user/usersStatus",s).then(function(s){s.result?t.$message({type:"success",message:"禁用成功"}):(e.is_enable=!e.is_enable,t.$message({type:"error",message:"禁用失败"}))})}else if(0==e.is_enable){var a={users:[e.id],enable:!1};t.$store.dispatch("user/usersStatus",a).then(function(s){s.result?t.$message({type:"success",message:"启用成功"}):(e.is_enable=!e.is_enable,t.$message({type:"error",message:"启用失败"}))})}}).catch(function(){e.is_enable=!e.is_enable,t.$message({type:"info",message:"调取接口失败"})})},handleDelete:function(e){var t=this;this.$confirm("此操作将永久删除, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){var s={id:e.row.id};t.$store.dispatch("user/deleteUser",s).then(function(e){e.result?(t.getUser(),t.$message({type:"success",message:"删除用户成功"})):t.$message({type:"error",message:"删除用户失败"})})}).catch(function(){t.$message({type:"info",message:"已取消"})})},handleSelect:function(e){this.getUser({chname:e.value})},handleSelectDialog:function(e){this.addUserId=e.id,this.formUser.phone=e.phone,this.formUser.email=e.email},searchNotInAppUser:function(){var e=this;this.userDetail=[],this.$store.dispatch("user/getNotInAppUser").then(function(t){if(t.result){var s=!0,a=!1,i=void 0;try{for(var n,o=r()(t.data);!(s=(n=o.next()).done);s=!0){var l=n.value;e.userDetail.push({value:l.chname,phone:l.phone,email:l.email,id:l.id})}}catch(e){a=!0,i=e}finally{try{!s&&o.return&&o.return()}finally{if(a)throw i}}}})},search:function(){var e=this;this.$store.dispatch("group/getAllUser").then(function(t){if(t.result){var s=!0,a=!1,i=void 0;try{for(var n,o=r()(t.data);!(s=(n=o.next()).done);s=!0){var l=n.value;e.allUserName.push({value:l.chname})}}catch(e){a=!0,i=e}finally{try{!s&&o.return&&o.return()}finally{if(a)throw i}}}})},querySearchDetail:function(e,t){var s=this.userDetail;t(e?s.filter(this.createStateFilterDetail(e)):s)},createStateFilterDetail:function(e){return function(t){return 0===t.value.toLowerCase().indexOf(e.toLowerCase())}},querySearchAsync:function(e,t){var s=this.allUserName;t(e?s.filter(this.createStateFilter(e)):s)},createStateFilter:function(e){return function(t){return 0===t.value.toLowerCase().indexOf(e.toLowerCase())}}},filters:{arrayFormat:function(e){return(e=e.map(function(e){return e.display_name})).join(",")}}},d={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{staticClass:"user"},[s("div",{staticClass:"search"},[s("el-autocomplete",{attrs:{"fetch-suggestions":e.querySearchAsync,placeholder:"请输入用户名",clearable:""},on:{select:e.handleSelect},nativeOn:{keydown:function(t){e.show(t)}},model:{value:e.stateUser,callback:function(t){e.stateUser=t},expression:"stateUser"}})],1),e._v(" "),s("div",{staticClass:"new"},[s("el-button",{directives:[{name:"permission",rawName:"v-permission:add_bkuser",value:e.permissions,expression:"permissions",arg:"add_bkuser"}],attrs:{size:"mini",type:"primary"},on:{click:e.handleNewUser}},[e._v("\n      添加用户\n    ")])],1),e._v(" "),s("div",{staticClass:"table"},[s("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loadingUser,expression:"loadingUser"}],ref:"",staticStyle:{width:"100%"},attrs:{stripe:"",data:e.dataUser,height:"100%"}},[s("el-table-column",{attrs:{prop:"username",label:"用户名","show-overflow-tooltip":""}}),e._v(" "),s("el-table-column",{attrs:{prop:"chname",label:"中文名","show-overflow-tooltip":""}}),e._v(" "),s("el-table-column",{attrs:{prop:"phone",label:"电话","show-overflow-tooltip":""}}),e._v(" "),s("el-table-column",{attrs:{prop:"email",label:"邮箱","show-overflow-tooltip":""}}),e._v(" "),s("el-table-column",{attrs:{prop:"groups",label:"所属角色","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(t){return[s("span",[e._v(e._s(e._f("arrayFormat")(t.row.groups)))])]}}])}),e._v(" "),s("el-table-column",{attrs:{label:"是否启用"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("el-checkbox",{on:{change:function(s){e.checkboxChange(t.row)}},model:{value:t.row.is_enable,callback:function(s){e.$set(t.row,"is_enable",s)},expression:"scope.row.is_enable"}})]}}])}),e._v(" "),s("el-table-column",{attrs:{prop:"handle",label:"操作",fixed:"right",width:"100"},scopedSlots:e._u([{key:"default",fn:function(t){return[s("el-button",{attrs:{type:"text"},on:{click:function(s){e.handleAuthority(t)}}},[e._v("权限")]),e._v(" "),s("el-button",{attrs:{type:"text"},on:{click:function(s){e.handleDelete(t)}}},[e._v("删除")])]}}])})],1)],1),e._v(" "),s("pagination",{attrs:{total:e.totalNumber},on:{"page-size-change":e.pageSizeChange}}),e._v(" "),s("new-edit",{ref:"newEdit",attrs:{title:e.title,"dialog-action":"dialogAction",width:e.width},on:{"handle-success":e.handleSuccess}},[e.showForm?s("div",{attrs:{slot:"dialog-content"},slot:"dialog-content"},[s("el-form",{ref:"formUser",attrs:{"label-position":e.labelPosition,"label-width":"120px",model:e.formUser,rules:e.rulesUser}},[s("el-form-item",{attrs:{label:"用户名",prop:"name"}},[s("el-autocomplete",{staticClass:"inline-input",attrs:{clearable:"",size:"small","fetch-suggestions":e.querySearchDetail,placeholder:"请输入用户名"},on:{select:e.handleSelectDialog},model:{value:e.formUser.username,callback:function(t){e.$set(e.formUser,"username",t)},expression:"formUser.username"}})],1),e._v(" "),s("el-form-item",{attrs:{label:"电话",prop:"phone"}},[s("span",{staticClass:"form-content"},[e._v(e._s(e.formUser.phone))])]),e._v(" "),s("el-form-item",{attrs:{label:"邮箱",prop:"email"}},[s("span",{staticClass:"form-content"},[e._v(e._s(e.formUser.email))])])],1)],1):e._e(),e._v(" "),e.showForm?e._e():s("div",{attrs:{slot:"dialog-content"},slot:"dialog-content"},[s("div",e._l(e.userAuthorityList,function(t,a){return s("div",{key:a,staticClass:"label-position"},[s("label",{staticClass:"label-position-left"},[e._v(e._s(t.display_name))]),e._v(" "),s("div",{staticClass:"label-position-right"},[s("el-select",{attrs:{clearable:"",size:"mini",multiple:"",placeholder:"请选择角色"},model:{value:t.groups,callback:function(s){e.$set(t,"groups",s)},expression:"item.groups"}},e._l(e.optionsGroup,function(e,t){return s("el-option",{key:t,attrs:{label:e.label,value:e.value}})}))],1)])}))])])],1)},staticRenderFns:[]};var f=s("VU/8")(p,d,!1,function(e){s("f/4N")},null,null);t.default=f.exports},"f/4N":function(e,t){}});
//# sourceMappingURL=15.js.map