from django.contrib import admin
from django.urls import path,re_path,include
from workapp import views
from rest_framework_jwt.views import obtain_jwt_token  # 验证密码后返回token


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('register/', views.RegisterView.as_view(),name='register'),  # 注册用户
    re_path('login/', obtain_jwt_token,name='login'),  # 用户登录后返回token
    re_path('userlist/', views.UserList.as_view()),  # 测试需要携带token才能访问
    re_path('submitEditUser/',views.SubmitEditUser.as_view()), # 修改用户数据
    re_path('requestUserDelete/',views.RequestUserDelete.as_view()),  # 进行用户删除
    re_path('rolelist/', views.Rolelist.as_view()),
    re_path('flowconf/', views.Flowconf.as_view()),# 传递工单数据
    re_path('addwork/', views.Addwork.as_view()), # 添加工单
    re_path('updatework/', views.Updatework.as_view()), # 修改工单
    re_path('addrole/', views.Addrole.as_view()), # 添加角色
    re_path('adddepartment/', views.Adddepartment.as_view()), # 添加部门
    re_path('user_role/', views.User_role.as_view()), # 用户添加角色
    re_path('departmentlist/', views.Departmentlist.as_view()), # 获取部门
    re_path('newFlowUserRoleActionConf/', views.NewFlowUserRoleActionConf.as_view()), # 获取审批流
    re_path('delflowuserrole/', views.NewFlowUserRoleActionConf.as_view()), # 审批流删除
    re_path('updateflow/', views.updateflow.as_view()), # 审批流编辑
    re_path('addAutoActionConf/', views.addAutoActionConf.as_view()), # 审批流编辑
    re_path('addAuto/', views.addAuto.as_view()), # 审批流
    re_path('getFlowConf/', views.getFlowConf.as_view()), # 审批流
]


