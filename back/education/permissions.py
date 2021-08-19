from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    else:
      return request.user.is_staff

class NotDeleteIfNotAdmin(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method == 'DELETE':
      return request.user.is_staff
    else:
      return True

class IsAdminOrReadCreateOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    safe_methods = list(permissions.SAFE_METHODS[:])
    safe_methods.append('POST')
    if request.method in safe_methods:
      return True
    else:
      return request.user.is_staff

class IsAdminOrOptionOwnerOrNoUpdateDelete(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    user = request.user

    if user.is_staff:
      return True
    elif (user.specialist is not None) and (obj.specialist == user.specialist):
      return True
    else:
      return request.method in permissions.SAFE_METHODS

class IsAdminOrOption_fileOwnerOrNoUpdateDelete(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    user = request.user

    if user.is_staff:
      return True
    elif (user.specialist is not None) and (obj.option.specialist == user.specialist):
      return True
    else:
      return request.method in permissions.SAFE_METHODS

class CreateOptionIfHaveSpecialtyOrIsAdmin(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method == 'POST':
      user = request.user
      if user.is_staff:
        return True
      elif user.specialist is not None:
        activity_id = request.POST.get('activity_id', None)
        if activity_id is None:
          return False
        return user.specialist.activities.filter(pk=activity_id).exists()
      else:
        return False
    else:
      return True