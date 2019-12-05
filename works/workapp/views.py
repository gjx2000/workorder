import json
from rest_framework.views import APIView,Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from workapp.serializers import UserSerializer
from workapp import models
from workapp import serializers
# 用户注册
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

# 重新用户登录返回函数
def jwt_response_payload_handler(token, user=None, request=None):
    '''
    :param token: jwt生成的token值
    :param user: User对象
    :param request: 请求
    '''
    return {
        'token': token,
        'user': user.username,
        'userid': user.id
    }

# 测试必须携带token才能访问接口
class UserList(APIView):
    permission_classes = [IsAuthenticated]  # 接口中加权限
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self,request, *args, **kwargs):
        user = models.User.objects.all()
        userlist = serializers.UserSerializer(instance=user,many=True)
        return Response(data=userlist.data)

# 进行用户信息的修改
class SubmitEditUser(APIView):
    def post(self,request, *args, **kwargs):
        id = request.data.get('id')
        mobile = request.data.get('mobile')
        weixinid = request.data.get('weixinid')
        email = request.data.get('email')
        if id:
            one_user = models.User.objects.get(id=id)
            one_user.mobile = mobile
            one_user.weixinid = weixinid
            one_user.email = email
            one_user.save()
            return Response(status=200)
        else:
            return Response(status=300)

# 进行用户的删除操作
class RequestUserDelete(APIView):
    def post(self,request, *args, **kwargs):
        id = request.data.get('id')
        models.User.objects.get(id=id).delete()
        return Response(status=200)

# 获取到角色列表进行渲染
class Rolelist(APIView):
    def get(self,request, *args, **kwargs):
        role = models.Role.objects.all()
        rolelist = serializers.RoleSerializer(instance=role,many=True)
        return Response(data=rolelist.data)


# 传递工单数据
class Flowconf(APIView):
    def get(self,request, *args, **kwargs):
        flowconf = models.FlowConf.objects.all()
        flowconflist = serializers.FlowconfSerializer(instance=flowconf,many=True)
        return Response(data=flowconflist.data)
    def post(self,request):
        p = request.data.get('p')
        print(type(p))
        if p=='':
            return Response()
        else:
            flowconf = models.FlowConf.objects.filter(name__icontains=p)
            flowconflist = serializers.FlowconfSerializer(instance=flowconf,many=True)
            return Response(data=flowconflist.data)

# 添加工单
class Addwork(APIView):
    def post(self,request):
        creator_id = request.data.get('id')
        name = request.data.get('name')
        callback = request.data.get('callback')
        customfield = request.data.get('customfield')
        description = request.data.get('description')
        models.FlowConf.objects.create(
            name = name,
            callback = callback,
            customfield = customfield,
            description = description,
            creator_id = creator_id
        )
        return Response(status=200)

# 进行工单的编辑
class Updatework(APIView):
    def post(self,request):
        id = request.data.get('id')
        name = request.data.get('name')
        callback = request.data.get('callback')
        customfield = request.data.get('customfield')
        description = request.data.get('description')
        if id:
            one_user = models.FlowConf.objects.get(id=id)
            one_user.name = name
            one_user.callback = callback
            one_user.customfield = customfield
            one_user.description = description
            one_user.save()
            return Response(status=200)
        else:
            return Response(status=300)

# 添加角色
class Addrole(APIView):
    def post(self,request):
        zh_name = request.data.get('zh_name')
        name = request.data.get('name')
        description = request.data.get('description')
        models.Role.objects.create(
            zh_name = zh_name,
            name = name,
            description = description,
        )
        return Response(status=200)

# 添加部门
class Adddepartment(APIView):
    def post(self, request):
        name = request.data.get('name')
        models.Department.objects.create(
            name=name,
        )
        return Response(status=200)

# 为用户添加角色，实质为用户角色外键的修改
class User_role(APIView):
    def post(self,request):
        name = request.data.getlist('name')
        id = request.data.get('id')
        user = models.User.objects.get(id=id)
        ur = user.ur.all()
        user.ur.remove(*ur)
        for i in name:
            role = models.Role.objects.get(name=i)
            user.ur.add(role.id)
        return Response()

# 为工单添加审批流并传递工单数据
class Departmentlist(APIView):
    def get(self,request):
        department = models.Department.objects.all()
        department = serializers.DepartmentSerializer(instance=department,many=True)
        return Response(data=department.data)
    def post(self,request):
        approvetorole = request.data.get('approvetorole') # 是否组审批  true 为组审批,存1
        region5 = request.data.get('region5')  # 审批人或组的ID
        num = request.data.get('num')  # 序列id 第几个人审批
        is_auto = request.data.get('is_auto') # 是否自动化  true 为自动化,存1
        id = request.data.get('id')
        flowconf = models.FlowConf.objects.get(id=id)
        if approvetorole=='true':
            approvetorole = 1
            name = models.Department.objects.get(id=region5)
        else:
            approvetorole = 0
            name = models.User.objects.get(id=region5)
        if is_auto == 'true':
            is_auto=1
        else:
            is_auto=0
        models.NewFlowUserRoleActionConf.objects.create(
            approvetorole=approvetorole,
            sequence=num,
            approve_type_id=str(name),
            is_auto=is_auto,
            flowconf = flowconf
        )
        return Response(status=200)

# 传递审批流
class NewFlowUserRoleActionConf(APIView):
    def get(self,request):
        id = request.GET.get('id')
        newFlowUserRoleActionConf = models.NewFlowUserRoleActionConf.objects.filter(flowconf=id)
        newFlowUserRoleActionConf = serializers.NewFlowUserRoleActionConfSerializer(instance=newFlowUserRoleActionConf,many=True)
        return Response(data=newFlowUserRoleActionConf.data,status=200)
    def post(self,request):
        id = request.data.get('id')
        models.NewFlowUserRoleActionConf.objects.get(id=id).delete()
        return Response(status=200)

# 进行审批流的编辑
class updateflow(APIView):
    def post(self,request):
        approvetorole = request.data.get('approvetorole') # 是否组审批  true 为组审批,存1
        region5 = request.data.get('region5')  # 审批人或组的ID
        is_auto = request.data.get('is_auto') # 是否自动化  true 为自动化,存1
        id = request.data.get('id')  # 审批流ID
        newFlowUserRoleActionConf = models.NewFlowUserRoleActionConf.objects.get(id=id)
        if approvetorole=='true':
            approvetorole = True
            name = models.Department.objects.get(id=region5)
        else:
            approvetorole = False
            name = models.User.objects.get(id=region5)
        if is_auto == 'true':
            is_auto=True
        else:
            is_auto=False
        models.NewFlowUserRoleActionConf.objects.filter(approvetorole=newFlowUserRoleActionConf.approvetorole).update(approvetorole=approvetorole)
        models.NewFlowUserRoleActionConf.objects.filter(approve_type_id=newFlowUserRoleActionConf.approve_type_id).update(approve_type_id=str(name))
        models.NewFlowUserRoleActionConf.objects.filter(is_auto=newFlowUserRoleActionConf.is_auto).update(is_auto=is_auto)
        return Response(status=200)

# 添加自动化配置
class addAutoActionConf(APIView):
    def post(self,request):
        url = request.data.get('url')
        num = request.data.get('num')
        methods = request.data.get('methods')
        id = request.data.get('id')
        flowconf = models.NewFlowUserRoleActionConf.objects.get(id=id)
        a1 = models.AutoActionConf(
            url=url,
            timeout=num,
            method = methods,
            flowconf = flowconf)
        a1.save()
        return Response(status=200)

# 传递审批流
class addAuto(APIView):
    def get(self,request):
        id = request.GET.get('id')
        newFlowUserRoleActionConf = models.NewFlowUserRoleActionConf.objects.filter(flowconf=id)
        newFlowUserRoleActionConf = serializers.NewFlowUserRoleActionConfSerializer(instance=newFlowUserRoleActionConf,many=True)
        # print(newFlowUserRoleActionConf.data[0]['id'])
        list=[]
        for i in newFlowUserRoleActionConf.data:
            # print(i)
            list.append(i['approve_type_id'])
        # print(list)
        return Response(data=list,status=200)

# 传递信息
class getFlowConf(APIView):
    def get(self, request):
        '''
        :param request: 前端request请求
        :param flowconfid: FlowConf表中共的模板id
        :return:
        '''

        id = request.GET.get('id')
        # 通过工单id，找到对应工单
        flowconfobj = models.FlowConf.objects.get(id=id)
        # 获取自定义字段
        department = models.Department.objects.filter(user=flowconfobj.creator_id)
        lists = []
        for i in department:
            mydeptpath = str(i)
            lists.append(mydeptpath)
        # print(lists)
        data = json.loads(flowconfobj.customfield)
        flowconfname = flowconfobj.name
        flowconf_desc = flowconfobj.description
        # 每个工单都有的字段
        fixed_param = {
            "ruleForm": {
                "workorder_name": "",
                "mydeptpath": "",
                "flowconf_desc": ""
            },
            "rules": {

            },
            "field_list": [{
                "field_type": "input",
                "verbos_name": "工单名称",
                "name": "workorder_name",
                "external": False,
                "msg": "提示信息",
                "field_datasource": [],
                "is_disabled": True,
                "value": flowconfname
            }, {
                "field_type": "select",
                "verbos_name": "我的部门",
                "name": "mydeptpath",
                "external": False,
                "msg": "选择部门",
                "field_datasource": lists,
                "is_disabled": False,
                "value": lists
            }, {
                "field_type": "textarea",
                "verbos_name": "工单描述",
                "name": "flowconf_desc",
                "external": False,
                "msg": "输入工单描述信息",
                "field_datasource": [],
                "is_disabled": False,
                "value": ""
            }]
        }
        data['ruleForm'].update(fixed_param['ruleForm'])
        data['rules'].update(fixed_param['rules'])
        data['field_list'] = fixed_param['field_list'] + data['field_list']
        return Response(data)
    def post(self,request):
        input_field = request.data.get('det[input_field]')
        workorder_name = request.data.get('det[workorder_name]')
        workorder_name = models.FlowConf.objects.get(name=workorder_name)
        user = workorder_name.creator
        mydeptpath = request.data.get('det[mydeptpath]')
        flowconf_desc = request.data.get('det[flowconf_desc]')
        models.WorkOrder.objects.create(
            flowconf =workorder_name,
            parameter = input_field,
            create_user = user,
            description = flowconf_desc
        )
        return Response(status=200)










