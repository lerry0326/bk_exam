import {$axios} from './axios'

export default {
  // 调取api Demo
  getDemoApi: params => {
    return $axios.get('/get_demo_api/', { params: params })
  },
  // 测试接口
  getTest: params => {
    return $axios.get('/test/', { params: params })
  },
  // 测试接口
  getTableData: params => {
    return $axios.get('/api/sysmanage/mocks/users/', { params: params })
  },
  // 获取任务状态饼状图
  getTaskState: params => {
    return $axios.get('/api/monitor/mocks/task/state/', { params: params })
  },
  // 获取服务器
  getServerSelect: params => {
    return $axios.get('/api/monitor/mocks/server/select/', { params: params })
  },
  // 获取CPU状态折线图
  getServerPerformance: params => {
    return $axios.get(`/api/monitor/mocks/${params.id}/server/performance/`, { params: params })
  },
  // 获取CPU状态折线图
  getBizServer: params => {
    return $axios.get('/api/monitor/mocks/biz/server/', { params: params })
  },
  // 获取左侧菜单数据
  getMenu: params => {
    return $axios.get('/api/sysmanage/menus/tree/', { params: params })
  },
  // 获取当前用户的权限列表
  getCurrentPermission: params => {
    return $axios.get('/api/sysmanage/users/current_permission/', { params: params })
  },
  // 获取角色列表数据
  getGroups: params => {
    return $axios.get('/api/sysmanage/groups/', { params: params })
  },
  // 新增/编辑角色数据时获取所有用户
  getAllUser: params => {
    return $axios.get('/api/sysmanage/users/all/', { params: params })
  },
  // 新增/编辑角色数据时获取不在app内用户
  getNotInAppUser: params => {
    return $axios.get('/api/sysmanage/users/add/', { params: params })
  },
  // 新增/编辑角色数据时获取所有用户
  getAllGroup: params => {
    return $axios.get('/api/sysmanage/groups/select/', { params: params })
  },
  // 获取菜单树状结构数据
  getMenuTree: params => {
    return $axios.get('/api/sysmanage/menus/tree/', { params: params })
  },
  // 用户列表
  getTableUser: params => {
    return $axios.get('/api/sysmanage/users/', { params: params })
  },
  // 获取操作（功能）权限树状数据
  getPermsTree: params => {
    return $axios.get(`/api/sysmanage/groups/${params.id}/perm_tree/`)
  },
  // 获取单个角色的对应权限数据
  getAuthority: params => {
    return $axios.get(`/api/sysmanage/groups/${params.id}/`, params)
  },
  // 获取用户的关联权限数据
  getUserAuthority: params => {
    return $axios.get(`/api/sysmanage/users/${params.id}/search/perm/`, { params: params })
  },
  // 编辑角色数据
  editGroups: params => {
    return $axios.put(`/api/sysmanage/groups/${params.id}/`, params)
  },
  // 编辑角色数据
  editUser: params => {
    return $axios.put(`/api/sysmanage/users/${params.id}/`, params)
  },
  // 添加角色数据
  addGroups: params => {
    return $axios.post('/api/sysmanage/groups/', params)
  },
  // 添加用户数据
  addUser: params => {
    return $axios.post('/api/sysmanage/users/', params)
  },
  // 设置用户权限
  setUserPerm: params => {
    return $axios.post(`/api/sysmanage/users/${params.id}/set/perm/`, params.params)
  },
  // 删除角色数据
  deleteGroups: params => {
    return $axios.delete(`/api/sysmanage/groups/${params.id}/`, params)
  },
  // 删除角色数据
  deleteUser: params => {
    return $axios.delete(`/api/sysmanage/users/${params.id}/`, params)
  },
  // 启用/禁用角色
  groupsStatus: params => {
    return $axios.put('/api/sysmanage/groups/status/', params)
  },
  // 启用/禁用角色
  usersStatus: params => {
    return $axios.put('/api/sysmanage/users/status/', params)
  },
  // 获取任务列表
  getTaskList: params => {
    return $axios.get('/exam/api/tasks/', { params: params })
  },
  // 创建任务
  createTask: params => {
    return $axios.post('/exam/api/tasks/', params)
  },
  // 新增主机
  addHost: params => {
    return $axios.post('/exam/api/host/', params)
  },
  // 获取主机
  // getHost: params => {
  //   return $axios.get('/exam/api/tasks/search_hosts/', { params: params })
  // },
  getBiz: params => {
    return $axios.get('exam/api/tasks/search_bizs/', { params: params })
  },
  getSet: params => {
    return $axios.get('/exam/api/tasks/search_sets/', { params: params })
  },
  getTopo: params => {
    return $axios.get('/exam/api/tasks/search_biz_inst_topo/', { params: params })
  },
  getModule: params => {
    return $axios.get('/exam/api/tasks/search_modules/', { params: params })
  },
  getHost: params => {
    return $axios.get('/exam/api/host/search_hosts/', { params: params })
  },
}
