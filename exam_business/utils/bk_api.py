# -*- coding: utf-8 -*-
import base64, time


# 查询业务
def bk_search_bizs(client, bk_app_code, bk_app_secret, bk_username):
    try:
        resp = client.cc.search_business(bk_app_code=bk_app_code, bk_app_secret=bk_app_secret, bk_username=bk_username)
        if not resp['result']:
            print 'false false false'
            return 0, [], resp['message']
        biz_list = resp['data']['info']
        return 1, biz_list, 'success'
    except Exception as e:
        print 'error error error'
        errmsg = e.message if e.message else str(e)
        return 0, [], errmsg


# 查询集群
def bk_search_sets(client, bk_app_code, bk_app_secret, bk_username, bk_biz_id):
    try:
        resp = client.cc.search_set(bk_app_code=bk_app_code, bk_app_secret=bk_app_secret, bk_username=bk_username, bk_biz_id=bk_biz_id)
        if not resp['result']:
            return 0, [], resp['message']
        return 1, resp['data']['info'], 'success'
    except Exception as e:
        errmsg = e.message if e.message else str(e)
        return 0, [], errmsg


# 查询模块
def bk_search_modules(client, bk_app_code, bk_app_secret, bk_username, bk_biz_id, bk_set_id):
    try:
        resp = client.cc.search_module(bk_app_code=bk_app_code, bk_app_secret=bk_app_secret, bk_username=bk_username, bk_biz_id=bk_biz_id, bk_set_id=bk_set_id)
        if not resp['result']:
            return 0, [], resp['message']
        return 1, resp['data']['info'], 'success'
    except Exception as e:
        errmsg = e.message if e.message else str(e)
        return 0, [], errmsg


# 查询主机
def bk_search_hosts(client, bk_app_code, bk_app_secret, bk_username, kwargs):
    try:
        resp = client.cc.search_host(bk_app_code=bk_app_code, bk_app_secret=bk_app_secret, bk_username=bk_username, **kwargs)
        if not resp['result']:
            return 0, [], resp['message']
        ret_list = []
        host_list = resp['data']['info']
        for host in host_list:
            ret_list.append(host['host']['bk_host_innerip'])
            # ret_list.append('\n')
        return 1, ret_list, 'success'
    except Exception as e:
        errmsg = e.message if e.message else str(e)
        return 0, [], errmsg


# 查询业务拓扑
def bk_search_biz_topo(client, bk_app_code, bk_app_secret, bk_username, bk_biz_id):
    try:
        resp = client.cc.search_biz_inst_topo(bk_app_code=bk_app_code, bk_app_secret=bk_app_secret, bk_username=bk_username, bk_biz_id=bk_biz_id)
        if not resp['result']:
            return 0, [], resp['message']
        return 1, resp['data'], 'success'
    except Exception as e:
        errmsg = e.message if e.message else str(e)
        return 0, [], errmsg


# 获取所有用户
def bk_search_users(client, bk_app_code, bk_app_secret, bk_token):
    try:
        resp = client.bk_login.get_all_users(bk_app_code, bk_app_secret, bk_token)
        if not resp['result']:
            return 0, [], resp['message']
        return 1, resp['data'], 'success'
    except Exception as e:
        errmsg = e.message if e.message else str(e)
        return 0, [], errmsg


# 快速执行脚本
def bk_fast_execute_script(check_obj, client, execute_account, script_content, param_content='', script_timeout=1000):
    try:
        kwargs = {
            'bk_biz_id': check_obj['bk_biz_id'],
            'script_type': 1,
            'script_content': base64.b64encode(script_content),
            'ip_list': check_obj['ip_list'],
            'account': execute_account,
            'script_param': base64.b64encode(param_content),
            'script_timeout': script_timeout
        }
        resp = client.job.fast_execute_script(kwargs)
        if not resp['result']:
            return 0, 0, resp['message']
        return 1, resp['data']['job_instance_id'], 'success'
    except Exception as e:
        errmsg = e.message if e.message else str(e)
        return 0, 0, errmsg


# 获取作业结果(目前只获取第一步结果)
def bk_get_job_instance_log(client, biz_id, job_instance_id, count=0):
    kwargs = {
        "bk_biz_id": int(biz_id),
        "job_instance_id": int(job_instance_id)
    }
    req = client.job.get_job_instance_log(kwargs)
    if not req['result']:
        count += 1
        if count > 5:
            return 0, [], req['message']
        time.sleep(3)
        return bk_get_job_instance_log(client, biz_id, job_instance_id, count)
    if req["data"][0]["is_finished"]:
        log_content = []
        for i in req["data"][0]["step_results"]:
            log_content += [{"ip": u["ip"], "log_content": u["log_content"].strip(), "bk_cloud_id": u["bk_cloud_id"],
                             "is_success": i['ip_status'] == 9} for u in
                            i["ip_logs"]]
        return 1, log_content, "success"
    time.sleep(3)
    return bk_get_job_instance_log(client, biz_id, job_instance_id)


# 获取作业模板
def bk_get_job_list(client, kwargs):
    try:
        req = client.job.get_job_list(kwargs)
        if not req['result']:
            return 0, [], req['message']
        return 1, req['data'], 'success'
    except Exception as e:
        err_msg = e.message if e.message else str(e)
        return 0, [], err_msg


# 获取作业模板详情
def bk_get_job_detail(client, kwargs):
    try:
        req = client.job.get_job_detail(kwargs)
        if not req['result']:
            return 0, [], [], req['message']
        global_vars = req['data'].get('global_vars', [])
        global_vars_ids = [i['id'] for i in global_vars]
        steps = req['data']['steps']
        steps_ids = [s['step_id'] for s in steps]
        return 1, global_vars_ids, steps_ids, 'success'
    except Exception as e:
        err_msg = e.message if e.message else str(e)
        return 0, [], [], err_msg


# 启动作业
def bk_execute_job(client, kwargs):
    try:
        req = client.job.execute_job(kwargs)
        if not req['result']:
            return 0, 0, req['message']
        return 1, req["data"]["job_instance_id"], 'success'
    except Exception as e:
        err_msg = e.message if e.message else str(e)
        return 0, [], err_msg
