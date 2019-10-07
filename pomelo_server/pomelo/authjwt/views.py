from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django.utils.translation import gettext as _
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from .serializers import BaseUserSerializer
# from rest_framework.permissions import IsAdminUser
from rest_framework import permissions
from rest_framework.decorators import action
from pomelo.serializers import PasswordSerializer
from pomelo.permissions import IsUserInstance
from rest_framework import status

UserModel = get_user_model()


@api_view(['get'])
def get_username(request):
    q_str = request.GET.get('query', None)
    q = Q(phone=q_str) | Q(email=q_str)
    try:
        user = UserModel.objects.filter(q)[0]
        username = user.username
        return Response({'username': username})
    except ObjectDoesNotExist:
        raise NotFound(_(f"user not found:  {q_str} "))
    except IndexError:
        raise NotFound(_(f"user not found:  {q_str} "))


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
