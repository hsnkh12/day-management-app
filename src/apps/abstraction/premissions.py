from rest_framework.permissions import BasePermission,SAFE_METHODS



class UserPrem(BasePermission):

    message = "You do not have the premission"

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return False

        return obj.user == request.user