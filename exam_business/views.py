# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from .models import Task, TestCase, HostInfo
from .serializers import TaskSerializer, TestCaseSerializer, HostInfoSerializer
from .utils.bk_api import bk_search_bizs, bk_search_sets, bk_search_modules, bk_search_hosts, bk_search_biz_topo, \
    bk_search_users, bk_fast_execute_script, bk_get_job_instance_log, bk_get_job_list, bk_get_job_detail, bk_execute_job
from blueking.component.shortcuts import get_client_by_request,get_client_by_user
from conf.default import APP_ID, APP_TOKEN, BK_TOKEN, BK_USERNAME
import xlrd, xlwt, time, os
from django.http import FileResponse


# Create your views here.


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @list_route(methods=['post'])
    def import_employee_info(self, request, *args, **kwargs):
        """
        导入职员信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        orig_file = request.FILES.get('employee_file', None)
        # serializer = self.get_serializer(data=orig_file)
        # if serializer.is_valid():
        excel_file = ExcelFile.objects.create(employee_file=orig_file)
        info_file = excel_file.employee_file.name
        xl = xlrd.open_workbook(info_file)
        sheet1 = xl.sheet_by_name("Sheet1")
        row_num = sheet1.nrows

        # institution_list = []
        institutions = Institution.objects.all()
        for institution in institutions:
            # institution_list.append(institution.name)
            for row in range(1, row_num):
                employee_data = sheet1.row_values(row)
                # if employee_data[5] in institution_list:
                if employee_data[5] == institution.name:
                    Employee.objects.create(name=employee_data[0],
                                            ID_card=employee_data[1],
                                            phone_number=employee_data[2],
                                            role=employee_data[3],
                                            score=employee_data[4],
                                            # institution=employee_data[5],
                                            institution=institution,
                                            certification=employee_data[6],
                                            major=employee_data[7])
        return Response(data={'message': 'create successfully', 'result': True}, status=status.HTTP_201_CREATED)

    @list_route(methods=['get'])
    def export_employee_info(self, request, *args, **kwargs):
        """
        导出职员信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        work_book = xlwt.Workbook(encoding='utf-8')
        work_sheet = work_book.add_sheet('employee_info_sheet')
        column_index = [u'姓名', u'身份证号', u'手机号', u'职位', u'成绩', u'运维机构', u'证书', u'专业']
        name_list, IDcard_list, phone_number_list, role_list, score_list = [], [], [], [], []
        institution_list, certification_list, major_list = [], [], []

        flag = request.query_params.get('is_checkedall', 'true')
        if flag == 'true':
            employee_infos = Employee.objects.all().order_by('-id')
            for employee_info in employee_infos:
                name_list.append(employee_info.name)
                IDcard_list.append(employee_info.ID_card)
                phone_number_list.append(employee_info.phone_number)
                role_list.append(employee_info.role)
                score_list.append(employee_info.score)
                institution_list.append(employee_info.institution.name)
                certification_list.append(employee_info.certification)
                major_list.append(employee_info.major)
            for i in range(len(column_index)):
                # 写入第1行数据（列索引）
                work_sheet.write(0, i, column_index[i])

            for i in range(len(name_list)):
                # 写入第1列数据（姓名）
                work_sheet.write(i + 1, 0, name_list[i])

            for i in range(len(IDcard_list)):
                # 写入第2列数据（身份证号）
                work_sheet.write(i + 1, 1, IDcard_list[i])

            for i in range(len(phone_number_list)):
                # 写入第3列数据（手机号）
                work_sheet.write(i + 1, 2, phone_number_list[i])

            for i in range(len(role_list)):
                # 写入第4列数据（职位）
                work_sheet.write(i + 1, 3, role_list[i])

            for i in range(len(score_list)):
                # 写入第5列数据（成绩）
                work_sheet.write(i + 1, 4, score_list[i])

            for i in range(len(institution_list)):
                # 写入第6列数据（运维机构）
                work_sheet.write(i + 1, 5, institution_list[i])

            for i in range(len(certification_list)):
                # 写入第7列数据（证书）
                work_sheet.write(i + 1, 6, certification_list[i])

            for i in range(len(major_list)):
                # 写入第8列数据（专业）
                work_sheet.write(i + 1, 7, major_list[i])
            file_name = 'employee_info_' + str(int(time.time())) + '.xls'
            work_book.save(file_name)

            # django实现文件下载
            back_file = open(file_name, 'rb')
            response = FileResponse(back_file)
            # 头信息为'application/octet-stream' 弹出‘文件下载’对话框，决定‘打开’还是‘保存’
            response['Content-Type'] = 'application/octet-stream'
            # 以附件的方式下载，文件名是filename
            response['Content-Disposition'] = 'attachment;filename={}'.format(file_name)
            return response
        ids = request.query_params.get('ids', None)
        id_list = []
        ids_list = ids.split(',')
        for i in ids_list:
            id_list.append(int(i))
        emp_infos = Employee.objects.filter(id__in=id_list)
        for employee_info in emp_infos:
            name_list.append(employee_info.name)
            IDcard_list.append(employee_info.ID_card)
            phone_number_list.append(employee_info.phone_number)
            role_list.append(employee_info.role)
            score_list.append(employee_info.score)
            institution_list.append(employee_info.institution.name)
            certification_list.append(employee_info.certification)
            major_list.append(employee_info.major)
        for i in range(len(column_index)):
            # 写入第1行数据（列索引）
            work_sheet.write(0, i, column_index[i])

        for i in range(len(name_list)):
            # 写入第1列数据（姓名）
            work_sheet.write(i + 1, 0, name_list[i])

        for i in range(len(IDcard_list)):
            # 写入第2列数据（身份证号）
            work_sheet.write(i + 1, 1, IDcard_list[i])

        for i in range(len(phone_number_list)):
            # 写入第3列数据（手机号）
            work_sheet.write(i + 1, 2, phone_number_list[i])

        for i in range(len(role_list)):
            # 写入第4列数据（职位）
            work_sheet.write(i + 1, 3, role_list[i])

        for i in range(len(score_list)):
            # 写入第5列数据（成绩）
            work_sheet.write(i + 1, 4, score_list[i])

        for i in range(len(institution_list)):
            # 写入第6列数据（运维机构）
            work_sheet.write(i + 1, 5, institution_list[i])

        for i in range(len(certification_list)):
            # 写入第7列数据（证书）
            work_sheet.write(i + 1, 6, certification_list[i])

        for i in range(len(major_list)):
            # 写入第8列数据（专业）
            work_sheet.write(i + 1, 7, major_list[i])
        file_name = 'employee_info_' + str(int(time.time())) + '.xls'
        work_book.save(file_name)

        # django实现文件下载
        back_file = open(file_name, 'rb')
        response = FileResponse(back_file)
        # 头信息为'application/octet-stream' 弹出‘文件下载’对话框，决定‘打开’还是‘保存’
        response['Content-Type'] = 'application/octet-stream'
        # 以附件的方式下载，文件名是filename
        response['Content-Disposition'] = 'attachment;filename={}'.format(file_name)
        return response

    @list_route(methods=['get'])
    def download_template(self, request, *args, **kwargs):
        # django实现文件下载
        root_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(root_path, 'utils')
        file = os.path.join(file_path, 'employee_info_temp.xlsx')
        back_file = open(file, 'rb')
        response = FileResponse(back_file)
        # 头信息为'application/octet-stream' 弹出‘文件下载’对话框，决定‘打开’还是‘保存’
        response['Content-Type'] = 'application/octet-stream'
        # 以附件的方式下载，文件名是filename
        response['Content-Disposition'] = 'attachment;filename={}'.format('employee_temp.xlsx')
        return response

    @list_route(methods=['get'])
    def search_bizs(self, request, *args, **kwargs):
        client = get_client_by_request(request)
        bk_token = 'S80KPRcOObzj1ytTj5eStYEcX8oWGdZsVeEaYvKOX6Q'
        bk_username = 'leiqingsong'
        # resp = client.cc.search_business(bk_app_code=APP_ID, bk_app_secret=APP_TOKEN, bk_token=bk_token)
        code, data, message = bk_search_bizs(client, bk_app_code=APP_ID, bk_app_secret=APP_TOKEN,
                                             bk_username=BK_USERNAME)
        # print 11111111111111111111, code
        # print 22222222222222222222, data
        # print 33333333333333333333, message
        # return Response(data=resp, status=status.HTTP_200_OK)
        return Response(data={'code': code, 'data': data, 'message': message}, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def search_sets(self, request, *args, **kwargs):
        client = get_client_by_request(request)
        bk_biz_id = request.query_params.get('biz_id', None)
        # bk_biz_id = 2
        bk_token = 'LKWTUgvv-LEogscX3MOe0xQ9rwxh0UE_GPnts8DIfRk'
        code, data, message = bk_search_sets(client, bk_app_code=APP_ID, bk_app_secret=APP_TOKEN,
                                             bk_username=BK_USERNAME, bk_biz_id=bk_biz_id)
        # resp = client.cc.search_set(bk_app_code=APP_ID, bk_app_secret=APP_TOKEN, bk_token=bk_token, bk_biz_id=bk_biz_id)
        print code, data, message
        # return Response(data=resp, status=status.HTTP_200_OK)
        return Response(data={'code': code, 'data': data, 'message': message}, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def search_modules(self, request, *args, **kwargs):
        biz_id = request.query_params.get('biz_id', '')
        set_id = request.query_params.get('set_id', '')
        bk_biz_id = biz_id
        bk_set_id = set_id
        client = get_client_by_request(request)
        code, data, message = bk_search_modules(client, bk_app_code=APP_ID, bk_app_secret=APP_TOKEN,
                                                bk_username=BK_USERNAME, bk_biz_id=bk_biz_id, bk_set_id=bk_set_id)
        return Response(data={'code': code, 'data': data, 'message': message}, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def search_hosts(self, request, *args, **kwargs):
        # ips = request.query_params.get('ips', '')
        # module_id = request.query_params.get('module_id', '')
        # set_id = request.query_params.get('set_id', '')
        # biz_id = request.query_params.get('biz_id', '')
        # set_id = 3
        # biz_id = 3
        bk_token = 'LKWTUgvv-LEogscX3MOe0xQ9rwxh0UE_GPnts8DIfRk'
        kwargs = {
            'condition': [
                {
                    'bk_obj_id': 'host',
                    'fields': [],
                    'condition': []
                },
                {
                    'bk_obj_id': 'module',
                    'fields': ['bk_module_id', 'bk_module_name'],
                    'condition': []
                },
                {
                    'bk_obj_id': 'set',
                    'fields': ['bk_set_id', 'bk_set_name'],
                    'condition': []
                },
                {
                    'bk_obj_id': 'biz',
                    'fields': ['bk_biz_id', 'bk_biz_name'],
                    'condition': []
                }
            ]
        }
        # if module_id:
        #     args = {'field': 'bk_module_id', 'operator': '$eq', 'value': int(module_id)}
        #     kwargs['condition'][1]['condition'].append(args)
        # if set_id:
        #     args = {'field': 'bk_set_id', 'operator': '$eq', 'value': int(set_id)}
        #     kwargs['condition'][2]['condition'].append(args)
        # if biz_id:
        #     args = {'fields': 'bk_biz_id', 'operator': '$eq', 'value': int(biz_id)}
        #     kwargs['condition'][3]['condition'].append(args)
        # if ips:
        #     ips = ips.strip()
        #     ip_list = ips.split('\n')
        #     kwargs['ip'] = {
        #         'data': ip_list,
        #         'exact': 1,
        #         'flag': 'bk_host_innerip|bk_host_outerip'
        #     }
        client = get_client_by_request(request)
        code, data, message = bk_search_hosts(client, bk_app_code=APP_ID, bk_app_secret=APP_TOKEN,
                                              bk_username=BK_USERNAME, kwargs=kwargs)
        return Response(data={'code': code, 'data': data, 'message': message}, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def search_biz_inst_topo(self, request, *args, **kwargs):
        biz_id = request.query_params.get('biz_id', '')
        bk_biz_id = biz_id
        bk_username = 'leiqingsong'
        client = get_client_by_request(request)
        code, data, message = bk_search_biz_topo(client, bk_app_code=APP_ID, bk_app_secret=APP_TOKEN,
                                                 bk_username=bk_username, bk_biz_id=bk_biz_id)
        return Response(data={'code': code, 'data': data, 'message': message}, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def get_all_users(self, request, *args, **kwargs):
        client = get_client_by_request(request)
        # code, data, message = bk_search_users(client)
        bk_token = 'LKWTUgvv-LEogscX3MOe0xQ9rwxh0UE_GPnts8DIfRk'
        resp = client.bk_login.get_all_users(APP_ID, APP_TOKEN, bk_token)
        return Response(data=resp, status=status.HTTP_200_OK)
        # return Response(data={'code': code, 'data': data, 'message': message}, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def fast_execute_script(self, request, *args, **kwargs):
        biz_id = 2
        check_obj = {
            'bk_biz_id': 2,
            'ip_list': [
                {'ip': '197.68.2.61', 'bk_cloud_id': 0},
                {'ip': '197.68.2.62', 'bk_cloud_id': 0}
            ]
        }
        execute_account = 'root'
        script_content = 'hostname'
        client = get_client_by_request(request)
        code_script, job_instance_id, message_script = bk_fast_execute_script(check_obj,
                                                                              client,
                                                                              execute_account,
                                                                              script_content)
        if code_script:
            code_log, log_content, message_log = bk_get_job_instance_log(client, biz_id, job_instance_id)
            return Response(data={'code_log': code_log, 'log_content': log_content, 'message_log': message_log},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={'code_script': code_script,
                                  'job_instance_id': job_instance_id,
                                  'message_script': message_script},
                            status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def get_job_list(self, request, *args, **kwargs):
        biz_id = 2
        kwargs = {'bk_biz_id': biz_id}
        client = get_client_by_request(request)
        code, data, message = bk_get_job_list(client, kwargs)
        return Response(data={'code': code, 'data': data, 'message': message},
                        status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def execute_job(self, request, *args, **kwargs):
        biz_id = 2
        job_id = 16
        ip_list = [
            {"ip": "197.68.2.64", "bk_cloud_id": 0},
            {"ip": "197.68.2.65", "bk_cloud_id": 0},
        ]
        client = get_client_by_request(request)
        kwargs = {
            'bk_biz_id': biz_id,
            'bk_job_id': job_id
        }
        # step1:查询作业模板详情:查询全局参数和步骤
        code_detail, global_vars_ids, steps_ids, message_detail = bk_get_job_detail(client, kwargs)
        if code_detail:
            # 执行作业返回结果
            if global_vars_ids:
                kwargs['global_vars'] = [{'id': g, 'ip_list': ip_list} for g in global_vars_ids]
            if steps_ids:
                kwargs['steps'] = [{'step_id': s, 'ip_list': ip_list} for s in steps_ids]
            code_job, job_instance_id, message_job = bk_execute_job(client, kwargs)
            if code_job:
                code_log, log_content, message_log = bk_get_job_instance_log(client, biz_id, job_instance_id)
                return Response(data={'code_log': code_log, 'log_content': log_content, 'message_log': message_log},
                                status=status.HTTP_200_OK)
            else:
                return Response(data={'code_job': code_job,
                                      'job_instance_id': job_instance_id,
                                      'message_job': message_job},
                                status=status.HTTP_200_OK)
        else:
            return Response(data={'code_detail': code_detail, 'data': [], 'message_detail': message_detail},
                            status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def search_inst(self, request, *args, **kwargs):
        client = get_client_by_user("admin")
        resp = client.cc.search_inst(
                                     bk_obj_id='oracle', bk_supplier_account="0",)
        return Response(data=resp, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def search_user_group(self, request, *args, **kwargs):
        client = get_client_by_request(request)
        resp = client.cc.search_user_group(bk_app_code=APP_ID, bk_app_secret=APP_TOKEN, bk_token=BK_TOKEN,
                                           bk_supplier_account=0)
        return Response(data=resp, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def search(self, request):
        client = get_client_by_request(request)
        bk_app_code = request.data.get('bk_app_code')
        bk_app_secret = request.data.get('bk_app_secret')
        bk_token = 'LKWTUgvv-LEogscX3MOe0xQ9rwxh0UE_GPnts8DIfRk'
        # bk_app_code = 'vick-test'
        # bk_app_secret = '1560c2f8-de05-4a7c-992f-046f03712601'
        # resp = client.cc.search_host(bk_app_code=bk_app_code, bk_app_secret=bk_app_secret)
        resp = client.cc.search_host(bk_app_code=APP_ID, bk_app_secret=APP_TOKEN, bk_username=BK_USERNAME)
        # resp = bk_search_hosts(client)
        if resp['result']:
            ret_list = []
            host_list = resp['data']['info']
            for host in host_list:
                ret_list.append(host['host']['bk_host_innerip'])
        print 11111111111111111, ret_list
        return Response(data=resp, status=status.HTTP_200_OK)


class TestCaseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer

    def list(self, request, *args, **kwargs):
        return Response(data={'username': 'admin',
                              'phone': '18800000000',
                              'last_login': '2019-10-25 10:00:00',
                              'result': True,
                              'email': 'admin@qq.com'})


class HostInfoViewSet(viewsets.ModelViewSet):
    queryset = HostInfo.objects.all()
    serializer_class = HostInfoSerializer

    @list_route(methods=['get'])
    def get_host(self, request, *args, **kwargs):
        business = request.query_params.get('business', '')
        host = self.queryset.filter(business=business)
        serializer = self.serializer_class(instance=host, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def search_bizs(self, request, *args, **kwargs):
        client = get_client_by_request(request)
        code, data, message = bk_search_bizs(client, **kwargs)
        print 11111111111111111111, code
        print 22222222222222222222, data
        print 33333333333333333333, message
        return Response(data={'code': code, 'data': data, 'message': message}, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def search_hosts(self, request, *args, **kwargs):
        # ips = request.query_params.get('ips', '')
        # module_id = request.query_params.get('module_id', '')
        # set_id = request.query_params.get('set_id', '')
        biz_id = request.query_params.get('biz_id', '')
        # print 111111111111111155, biz_id
        # biz_id = 2
        kwargs = {
            'condition': [
                {
                    'bk_obj_id': 'host',
                    'fields': [],
                    'condition': []
                },
                {
                    'bk_obj_id': 'module',
                    'fields': ['bk_module_id', 'bk_module_name'],
                    'condition': []
                },
                {
                    'bk_obj_id': 'set',
                    'fields': ['bk_set_id', 'bk_set_name'],
                    'condition': []
                },
                {
                    'bk_obj_id': 'biz',
                    'fields': ['bk_biz_id', 'bk_biz_name'],
                    'condition': []
                }
            ]
        }
        # if module_id:
        #     args = {'field': 'bk_module_id', 'operator': '$eq', 'value': int(module_id)}
        #     kwargs['condition'][1]['condition'].append(args)
        # if set_id:
        #     args = {'field': 'bk_set_id', 'operator': '$eq', 'value': int(set_id)}
        #     kwargs['condition'][2]['condition'].append(args)
        if biz_id:
            args = {'fields': 'bk_biz_id', 'operator': '$eq', 'value': int(biz_id)}
            kwargs['condition'][3]['condition'].append(args)
        # if ips:
        #     ips = ips.strip()
        #     ip_list = ips.split('\n')
        #     kwargs['ip'] = {
        #         'data': ip_list,
        #         'exact': 1,
        #         'flag': 'bk_host_innerip|bk_host_outerip'
        #     }
        # kwargs = {
        #     'bk_biz_id': biz_id
        # }
        client = get_client_by_request(request)
        # code, data, message = bk_search_hosts(client, bk_app_code=APP_ID, bk_app_secret=APP_TOKEN,
        #                                       bk_username=BK_USERNAME, kwargs=kwargs)
        # return Response(data={'code': code, 'data': data, 'message': message}, status=status.HTTP_200_OK)
        resp = client.cc.search_host(bk_app_code=APP_ID, bk_app_secret=APP_TOKEN, bk_username=BK_USERNAME, **kwargs)
        if not resp['result']:
            return 0, [], resp['message']
        ret_list = []
        host_list = resp['data']['info']
        for host in host_list:
            host['host']['bk_mem'] = '---'
            host['host']['bk_disk'] = '---'
            host['host']['bk_cpu'] = '---'
            ret_list.append(host['host'])
            # ret_list.append('\n')
        # return 1, host_list, 'success'
        return Response(data={'data': ret_list}, status=status.HTTP_200_OK)
