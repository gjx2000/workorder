from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=24)
    weixinid = models.CharField(max_length=24)
    email = models.CharField(max_length=64)
    ur = models.ManyToManyField(to='Role')
    def __str__(self):
        return self.username

class Role(models.Model):
    zh_name = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=32)

    def __str__(self):
        return self.zh_name

class Department(models.Model):
    name = models.CharField(max_length=64)
    fid = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)
    user = models.ManyToManyField('User')

    def __str__(self):
        return self.name

class FlowConf(models.Model):
    name = models.CharField(max_length=64,verbose_name='工单名称')
    callback = models.CharField(max_length=64,verbose_name='回调地址')
    creator = models.ForeignKey(to=User,verbose_name='创建者',on_delete=models.CASCADE)
    customfield = models.TextField(verbose_name='自定义字段')
    description = models.TextField(verbose_name='描述')

    class Meta:
        verbose_name_plural = '工单模板'

    def __str__(self):
        return self.name

class NewFlowUserRoleActionConf(models.Model):
    flowconf = models.ForeignKey(to='FlowConf',verbose_name='工单名称',on_delete=models.CASCADE)
    sequence = models.IntegerField(verbose_name='审批序号')    # 审批流的序号  如：1,2,3
    approvetorole = models.BooleanField(verbose_name='是否角色组审批')
    approve_type_id = models.CharField(verbose_name='审批者',max_length=64)    # 哪个人审批的  （审批者id）
    is_auto = models.BooleanField(verbose_name='是否自动化工单')
    class Meta:
        verbose_name_plural = '工单审批流配置'


class AutoActionConf(models.Model):
    flowconf = models.OneToOneField(to='NewFlowUserRoleActionConf',on_delete=models.CASCADE ,verbose_name='审批角色配置')
    url = models.CharField(max_length=128,verbose_name='自动化工单url')
    method = models.CharField(max_length=32,verbose_name='请求方式')
    timeout = models.CharField(max_length=12,verbose_name='超时时间')
    class Meta:
        verbose_name_plural = '子工单自动化配置'

class WorkOrder(models.Model):
    flowconf = models.ForeignKey(to='FlowConf',on_delete=models.CASCADE,verbose_name='工单名称')
    create_user = models.ForeignKey(to=User,on_delete=models.CASCADE,verbose_name='创建者')
    create_ts = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    status_cat = (
        ('0', '审批中'),
        ('1', '被退回'),
        ('2', '完成'),
    )
    order_status = models.CharField(max_length=5, verbose_name='工单状态', choices=status_cat, default='0')
    parameter = models.TextField(verbose_name='新工单参数',default={})
    description = models.TextField(verbose_name='工单描述',default='')

    class Meta:
        verbose_name_plural = '实例化工单'


class SubOrder(models.Model):
    action_cat = (
        ('0', '待处理'),
        ('1', '通过'),
        ('2', '退回'),
        ('3', '否决'),
        ('4', '确认')
    )
    suborder_cat = (
        ('0', '待上一节点处理'),
        ('1', '待处理'),
        ('2', '已经处理'),
    )
    mainorder = models.ForeignKey(WorkOrder,on_delete=models.CASCADE, verbose_name='实例工单名称')
    approve_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, default='')
    approve_user_role = models.CharField(verbose_name='审批角色', max_length=50)
    approve_userrole_id = models.IntegerField(verbose_name='审批角色ID', null=True, blank=True)
    sequence_number = models.IntegerField(verbose_name='审批序号')
    approve_ts = models.DateTimeField(verbose_name='审批时间', null=True, blank=True)
    action_status = models.CharField(verbose_name='审批状态', choices=action_cat, max_length=10)
    suborder_status = models.CharField(verbose_name='子任务状态', choices=suborder_cat, max_length=20)
    approve_text = models.TextField(verbose_name='审批意见', blank=True)
    is_auto = models.BooleanField(default=False, verbose_name='自动工单')
    timeout = models.CharField(verbose_name='超时时间', default='10',max_length=32)

    class Meta:
        verbose_name_plural = '子工单实例'


class WorkorderCallbacklog(models.Model):
    status_cat = (
        ('0', '待执行'),
        ('1', '完成'),
        ('2', '执行异常'),
    )
    workorder = models.OneToOneField(WorkOrder,on_delete=models.CASCADE,verbose_name='实例化工单名称')
    callbackurl = models.CharField(max_length=255, null=True, blank=True,verbose_name='回调url')
    status = models.CharField(max_length=5, verbose_name='回调状态', choices=status_cat)
    executetime = models.DateTimeField(verbose_name='执行时间', null=True, blank=True)
    log = models.TextField()

    class Meta:
        verbose_name_plural = '工单审批完成自动执行状态'


class SubOrderCallbacklog(models.Model):
    status_cat = (
        ('0', '待执行'),
        ('1', '完成'),
        ('2', '执行异常'),
    )
    sub_order = models.OneToOneField(SubOrder,verbose_name='子工单名称',on_delete=models.CASCADE)
    callbackconf = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=5, verbose_name='回调状态', choices=status_cat)
    executetime = models.DateTimeField(verbose_name='执行时间', null=True, blank=True)
    log = models.TextField()
    method = models.CharField(blank=True, null=True, max_length=24)

    class Meta:
        verbose_name_plural = '子工单审批完成自动执行状态'


