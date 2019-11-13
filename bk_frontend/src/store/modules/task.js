import api from '@/api/api'

const actions = {
    getTaskList({commit, state}, param) {
        return api.getTaskList(param)
    },
    createTask({commit, state}, param) {
        return api.createTask(param)
    },
    addHost({commit, state}, param) {
        return api.addHost(param)
    },
    getHost({commit, state}, param) {
        return api.getHost(param)
    },
    getBiz({commit, state}, param) {
        return api.getBiz(param)
    },
    getSet({commit, state}, param) {
        return api.getSet(param)
    },
    getTopo({commit, state}, param) {
        return api.getTopo(param)
    },
    getModule({commit, state}, param) {
        return api.getModule(param)
    }
}
