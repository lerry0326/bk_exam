import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import { mapGetters } from 'vuex'
const MonitorPanel = () => import('@/pages/monitor_panel_page/index')
const User = () => import('@/pages/user_page/user')
const Group = () => import('@/pages/group_page/Group')
const Permission = () => import('@/pages/group_page/Permission')
const Test = () => import('@/pages/test_page/Test')
const Task = () => import('@/pages/task_page/Task')
const AddTask = () => import('@/pages/task_page/AddTask')
const AddHost = () => import('@/pages/task_page/AddHost')
const GetHost = () => import('@/pages/task_page/GetHost')
const Index = () => import('@/pages/task_page/Index')
const TaskList = () => import('@/pages/task_page/TaskList')
const BizTopo = () => import('@/pages/task_page/BizTopo')
const BakReco = () => import('@/pages/task_page/scriptBak')
const BizHost = () => import('@/pages/task_page/BizHost')
Vue.use(Router);

let routerVue = new Vue({
    store,
    methods: {
        // 当前用户是否有路由权限
        async isRouterNameAuthority(routerName) {
            // 当前用户能访问的路由列表是否已获取,如果没有获取,则请求获取路由权限接口
            if (!this.isGetUserPerm) {
                await this.$store.dispatch('leftmenu/getCurrentPermission')
            }
            // 判断当前用户能访问的路由
            // 第一步，首先判断用户是否为管理员
            if (this.isAdmin) {
                return true
            }
            let authorityRes = false
            for(let i = 0; i < this.routerList; i++) {
                if (this.routerList[i].name == routerName) {
                    authorityRes = true
                    break
                }
            }
            return authorityRes
        }
    },
    computed: {
        ...mapGetters('leftmenu', ['isAdmin', 'isGetUserPerm', 'routerList'])
    }
})

let router = new Router({
    routes: [
        {
            path: '/',
            redirect: 'biz_host'
        },
        {
            path: '/403',
            component: resolve => require(['@/pages/403'], resolve)
        },
        {
            path: '/404',
            component: resolve => require(['@/pages/404'], resolve)
        },
        {
            path: '/test',
            name: 'test',
            component: Test,
            meta: {
                bread: [
                    {displayName: '测试页面', path: '/test'},
                ],
                currentMenu: '/test'
            }
        },
        {
            path: '/monitor_panel',
            name: 'monitor_panel',
            component: MonitorPanel,
            meta: {
                bread: [
                    {displayName: '首页', path: ''},
                    {displayName: '监控面板', path: '/monitor_panel'},
                ],
                currentMenu: '/monitor_panel'
            }
        },
        {
            path: '/user',
            name: 'user',
            component: User,
            meta: {
                bread: [
                    {displayName: '系统管理', path: ''},
                    {displayName: '用户管理', path: '/user'},
                ],
                currentMenu: '/user'
            }
        },
        {
            path: '/group',
            name: 'group',
            component: Group,
            meta: {
                bread: [
                    {displayName: '系统管理', path: ''},
                    {displayName: '角色管理', path: '/group'},
                ],
                currentMenu: '/group'
            },
        },
        {
          path: '/permission/:group_id',
          name: 'permission',
          component: Permission,
          meta: {
              bread: [
                  {displayName: '系统管理', path: ''},
                  {displayName: '角色管理', path: '/group'},
                  {displayName: '功能权限', path: ''},
              ],
              currentMenu: '/group'
          }
        },
        {
            path: '/tasks',
            name: 'tasks',
            component: Task,
            meta: {
                bread: [
                    {displayName: '任务管理', path: ''},
                ],
                currentMenu: '/tasks'
            }
        },
        {
            path: '/add_task',
            name: 'add_task',
            component: AddTask,
            meta: {
                bread: [
                    {displayName: '创建任务', path: ''},
                ],
                currentMenu: '/add_task'
            }
        },
        {
            path: '/add_host',
            name: 'add_host',
            component: AddHost,
            meta: {
                bread: [
                    {displayName: '新增主机', path: ''},
                ],
                currentMenu: '/add_host'
            }
        },
        {
            path: '/get_host',
            name: 'get_host',
            component: GetHost,
            meta: {
                bread: [
                    {displayName: '获取主机', path: ''},
                ],
                currentMenu: '/get_host'
            }
        },
        {
            path: '/index',
            name: 'index',
            component: Index,
            meta: {
                bread: [
                    {displayName: '首页', path: ''},
                ],
                currentMenu: '/index'
            }
        },
        {
            path: '/task_list',
            name: 'task_list',
            component: TaskList,
            meta: {
                bread: [
                    {displayName: '任务列表', path: ''},
                ],
                currentMenu: '/task_list'
            }
        },
        {
            path: '/biz_topo',
            name: 'biz_topo',
            component: BizTopo,
            meta: {
                bread: [
                    {displayName: '业务拓扑', path: ''},
                ],
                currentMenu: '/biz_topo'
            }
        },
        {
            path: '/bak_reco',
            name: 'bak_reco',
            component: BakReco,
            meta: {
                bread: [
                    {displayName: '备份记录', path: ''},
                ],
                currentMenu: '/bak_reco'
            }
        },
        {
            path: '/biz_host',
            name: 'biz_host',
            component: BizHost,
            meta: {
                bread: [
                    {displayName: '业务主机', path: ''},
                ],
                currentMenu: '/biz_host'
            }
        },
    ]
});

router.beforeEach(async (to, from, next) => {
    if (to.matched.length === 0) {
        from.name ? next({name: from.name}) : next('/404');
    } else {
        let authorityResult = await routerVue.isRouterNameAuthority(to.name)
        if (authorityResult || ['/403', '/404'].indexOf(to.path != -1)) {
            next();
        } else {
            next('/403');
        }
    }
});
export default router
