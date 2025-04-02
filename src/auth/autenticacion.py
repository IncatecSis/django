from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from src.models import *


class UsuarioBackend(BaseBackend):
    def authenticate(self, reqquest, username=None, password=None, **kwargs):
        try:
            usuario = Usuario.objects.get(documento_identidad=username)
            if not usuario.estado:
                return None
            if check_password(password, usuario.password):
                return usuario
        except Usuario.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None