from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import BaseAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status, serializers
from django.views.generic import ListView
from .models import User, Post, Portfolio
from .serializers import UserCreateSerializer, PasswordSerializer, PostSerializer, PortfolioSerializer


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_active': user.is_active,
            'is_staff': user.is_staff
        })


class Register(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'id': user.pk,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff
                })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #if serializer.is_valid():
        #    serializer.save()
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        #else:
        #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PasswordSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'detail': 'Wrong Password.'},
                                status=status.HTTP_400_BAD_REQUEST)

            if not serializer.data.get('new_password') == serializer.data.get('confirm_password'):
                return Response({'detail': 'Password Not Match.'},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'detail': 'Password Set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "logged out"})



@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    def get(self, request):
        return render(request, template_name='index.html', context={})

@method_decorator(login_required, name='dispatch')
class DashboardView(ListView):
    def get(self, request):
        return render(request, template_name='dashboard.html', context={})


class PostView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id=None):
        if post_id is not None:
            post = get_object_or_404(Post, pk=post_id, user=request.user)
            serializer = PostSerializer(post, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            posts = Post.objects.filter(user=request.user)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_id=None):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id=None):
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        return Response({"detail":"deleted"}, status=status.HTTP_200_OK)


class PortfolioView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, work_id=None):
        if work_id is not None:
            work = get_object_or_404(Portfolio, pk=work_id, user=request.user)
            serializer = PortfolioSerializer(work, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            works = Portfolio.objects.filter(user=request.user)
            serializer = PortfolioSerializer(works, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PortfolioSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, work_id=None):
        work = get_object_or_404(Portfolio, pk=work_id)
        serializer = PortfolioSerializer(work, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, work_id=None):
        work = get_object_or_404(Portfolio, pk=work_id)
        work.delete()
        return Response({"detail":"deleted"}, status=status.HTTP_200_OK)


class PostList(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id=None):
        if post_id is not None:
            post = get_object_or_404(Post, pk=post_id)
            serializer = PostSerializer(post, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



class WorkList(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, work_id=None):
        if work_id is not None:
            work = get_object_or_404(Portfolio, pk=work_id)
            serializer = PortfolioSerializer(work, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            works = Portfolio.objects.all()
            serializer = PortfolioSerializer(works, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)