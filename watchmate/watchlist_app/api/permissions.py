#Here we will create such that if any user is admin he can access, edit,read .., if any 
#other user he can only read 
#we can refer the document and import it.., see custom permissions

from rest_framework import permissions 


class IsAdminOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        '''
        #admin_permission = super.has_permission(request,view)
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method == "GET" or admin_permission
        '''
        if request.method in permissions.SAFE_METHODS:
            return True 
        else:
            return bool(request.user and request.user.is_staff)



class ReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True 
        else:
            #if any other request other than get request 
            return obj.review_user == request.user or request.user.is_staff
