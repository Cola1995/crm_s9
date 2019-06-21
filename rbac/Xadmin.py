from Xadmin.service.Xadmin import site,ModelXadmin
from rbac.models import *
class UserConfig(ModelXadmin):
    list_display = ["name","roles"]
site.register(User,UserConfig)
class RoleConfig(ModelXadmin):
    list_display = ["title","permissions"]
site.register(Role,RoleConfig)
class PerssionConfig(ModelXadmin):
    list_display = ["title","url","action","group"]
site.register(Permission,PerssionConfig)
site.register(PermissionGroup)