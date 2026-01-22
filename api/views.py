from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import Project, BlogPost, ContactMessage
from .serializers import ProjectSerializer, BlogPostSerializer, ContactMessageSerializer, UserSerializer
from .auth import generate_jwt_token, verify_jwt_token, JWTAuthentication

from rest_framework.viewsets import GenericViewSet


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def featured(self, request):
        """Ottieni i progetti in evidenza"""
        featured_projects = Project.objects.filter(featured=True)
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def by_category(self, request):
        """Filtra progetti per categoria"""
        category = request.query_params.get('category', None)
        if category:
            projects = Project.objects.filter(category=category)
        else:
            projects = Project.objects.all()
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            return BlogPost.objects.all()
        return BlogPost.objects.filter(published=True)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def recent(self, request):
        """Ottieni gli ultimi articoli pubblicati"""
        limit = request.query_params.get('limit', 5)
        recent_posts = BlogPost.objects.filter(published=True)[:int(limit)]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_as_read(self, request):
        """Segna i messaggi come letti"""
        message_ids = request.data.get('message_ids', [])
        ContactMessage.objects.filter(id__in=message_ids).update(read=True)
        return Response({'status': 'messaggi segnati come letti'})


# class AuthViewSet(GenericViewSet):
#     """ViewSet per l'autenticazione"""
#
#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def login(self, request):
#         """Login con username e password"""
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         if not username or not password:
#             return Response(
#                 {'error': 'Username e password sono obbligatori'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         try:
#             user = User.objects.get(username=username)
#             if check_password(password, user.password):
#                 token = generate_jwt_token(user)
#                 return Response({
#                     'token': token,
#                     'user': UserSerializer(user).data
#                 })
#             else:
#                 return Response(
#                     {'error': 'Credenziali non valide'},
#                     status=status.HTTP_401_UNAUTHORIZED
#                 )
#         except User.DoesNotExist:
#             return Response(
#                 {'error': 'Utente non trovato'},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
#
#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def register(self, request):
#         """Registra un nuovo utente (solo per admin)"""
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         if not all([username, email, password]):
#             return Response(
#                 {'error': 'Username, email e password sono obbligatori'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         if User.objects.filter(username=username).exists():
#             return Response(
#                 {'error': 'Username già esistente'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         if User.objects.filter(email=email).exists():
#             return Response(
#                 {'error': 'Email già registrata'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         user = User.objects.create(
#             username=username,
#             email=email,
#             password=make_password(password)
#         )
#
#         token = generate_jwt_token(user)
#         return Response({
#             'token': token,
#             'user': UserSerializer(user).data
#         }, status=status.HTTP_201_CREATED)
#
#     @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
#     def me(self, request):
#         """Ottieni i dati dell'utente autenticato"""
#         return Response(UserSerializer(request.user).data)
