from rest_framework.permissions import BasePermission

from store.market import Market


class CategoryPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True if request.user.is_admin else False
        else:
            return False

    def has_object_permission(self, request, view, obj):
        pass


class ProductPermissionCreate(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return True
            elif request.user.is_department_admin:
                return True

        return False

class ProductPermissionEdit(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return True
            elif request.user.is_department_admin:
                market = Market(request)
                if market.product.selectById(request.parser_context["kwargs"]['pk']).store in request.user.admins.all():
                    return True
        return False