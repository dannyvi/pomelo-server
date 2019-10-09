from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from .serializers import BaseUserSerializer, UserNameSerializer
# from rest_framework.permissions import IsAdminUser
from rest_framework import permissions
from rest_framework.decorators import action
from pomelo.serializers import PasswordSerializer
from pomelo.permissions import IsUserInstance
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

UserModel = get_user_model()

test_param = openapi.Parameter('search',
                               openapi.IN_QUERY,
                               description=_('search email | phone '),
                               type=openapi.TYPE_STRING)
user_response = openapi.Response(_('User infomation'), UserNameSerializer)


#  Keep for some moment


# auth_400_response = openapi.Response('用户帐号/密码不能为空', Auth400ErrorSerializer,
# examples={'application/json': {'success': False, 'messages': '用户帐号名必须存在, 请发送用户名!'}})

# auth_403_response = openapi.Response('用户帐号/密码错误', Auth400ErrorSerializer,
# examples={'application/json': {'success': False, 'messages': '用户名:alan 密码错误, 请输入正确密码!'}})

# auth_success_response = openapi.Response('认证成功，创建TOKEN并返回token与用户信息',
#  AuthSuccessSerializer, examples={'application/json': {'success': True,
#  'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9',"messages": "认证成功!",
#  "user": {"id": 305, "username": "alan","nickname": "傅", "email": "yaolin.fu@sagene.com.cn", "is_admin": False} }})


@swagger_auto_schema(method='get', operation_description=_('get username by email or phone'),
                     manual_parameters=[test_param], responses={200: user_response})
@api_view(['get'])
def get_username(request):
    """get username by email or phone."""
    q_str = request.GET.get('search', None)
    q = Q(phone=q_str) | Q(email=q_str)
    try:
        user = UserModel.objects.filter(q)[0]
        serializer = UserNameSerializer(user)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        raise NotFound(_(f'user not found:  {q_str} '))
    except IndexError:
        raise NotFound(_(f'user not found:  {q_str} '))

@method_decorator(name='list',
                  decorator=swagger_auto_schema(
                      operation_description=_('Only Admin User can get User list.'),
                      responses={'200': BaseUserSerializer(many=True)}))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description=_('Create new user.'),
    request_body=openapi.Schema(
        title=_('Create'),
        type=openapi.TYPE_OBJECT,
        required=['password', ],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING,  description=_('At least one of email|phone field.'))
    }),
    responses={'200': BaseUserSerializer}
))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(
                      operation_description=_('Get User infomation. \n Permissions: Is Owner.'),
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description=_('Update user info.\n Permissions: Is Owner.'),
    request_body=openapi.Schema(
        title=_('BaseUser'),
        type=openapi.TYPE_OBJECT,
        required=['password', ],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description=_('Anyone or both.'))
        }
    ),
    responses={'200': BaseUserSerializer}
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_description=_('Delete user.')))
class BaseUserViewset(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = UserModel.objects.all()
    serializer_class = BaseUserSerializer

    def get_permissions(self):
        """
        Allow anyone to sign up.
        AdminUser can query user list.
        Owner can edit itself.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated, IsUserInstance]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(method='post', operation_description=_('set password'))
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
