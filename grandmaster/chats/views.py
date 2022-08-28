from django.core.exceptions import BadRequest
from rest_framework import generics, filters
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.models import User
from chats.models import Chat
from chats.serializers import ChatSerializer, MessageSerializer, MemberSerializer
from profiles.models import SpecialContact


class ChatListView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        if user.contact_type == User.CONTACT.PARENT:
            user = self.get_child()
        self.check_chats_list(user)
        return user.chats.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        params = self.request.query_params
        child_id = params.get('id', None)
        context['child_id'] = child_id
        print(context)
        return context

    def get_child(self):
        params = self.request.query_params
        user = self.request.user
        child_id = params.get('id', None)
        if child_id is None:
            raise NotFound('Parents users need child id')
        child = get_object_or_404(User, id=child_id)
        if child not in user.children.all():
            raise BadRequest('You are not parent of this user')
        return child

    def check_chats_list(self, user):
        if user.contact_type == User.CONTACT.TRAINER:
            students = user.students.all()
            trainers = User.objects.filter(contact_type=User.CONTACT.TRAINER).exclude(pk=self.request.user.pk)
            specialists = [User.objects.get(id=id_['user']) for id_ in SpecialContact.objects.values('user')]
            self.create_dms(students)
            self.create_dms(trainers)
            self.create_dms(specialists)
        elif user.contact_type == User.CONTACT.MODERATOR:
            moderators = User.objects.filter(contact_type=User.CONTACT.MODERATOR)
            trainers = User.objects.filter(contact_type=User.CONTACT.TRAINER).exclude(pk=self.request.user.pk)
            specialists = [User.objects.get(id=id_['user']) for id_ in SpecialContact.objects.values('user')]
            students = User.objects.filter(contact_type=User.CONTACT.SPORTSMAN)
            self.create_dms(moderators)
            self.create_dms(trainers)
            self.create_dms(specialists)
            self.create_dms(students)
        elif user.contact_type == User.CONTACT.SPORTSMAN:
            specialists = [User.objects.get(id=id_['user']) for id_ in SpecialContact.objects.values('user')]
            if user.trainer is not None:
                self.create_dm(user.trainer)
            self.create_dms(specialists)
        elif user.contact_type == User.CONTACT.PARENT:
            raise BadRequest('Parent not allowed to own chats')

    def create_dms(self, users):
        for user in users:
            self.create_dm(user)

    def create_dm(self, obj):
        user = self.request.user
        members = [user.id, obj.id]
        name = f'dm_{user.id}{obj.id}'
        if len(user.chats.filter(name=name)) == 0:
            chat = Chat.objects.create(
                name=name,
                type=Chat.Type.DM,
                owner=None
            )
            chat.members.set(members)


# todo: change perms
class ChatDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class MessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_chat(self):
        params = self.request.query_params
        chat_id = params.get('chat', None)
        if chat_id is None:
            raise NotFound
        chat = Chat.objects.filter(id=chat_id)
        if not chat.exists():
            raise NotFound
        return chat[0]

    def get_queryset(self):
        chat = self.get_chat()
        user = self.request.user
        if chat not in user.chats.all():
            raise PermissionDenied
        messages = chat.messages.all().order_by('-created_at')
        self.request.user.readed_messages.add(*messages)
        self.request.user.save()
        return messages


class MembersListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MemberSerializer

    def get_queryset(self):
        user = self.request.user
        if User.Group.MODERATOR in user:
            return User.objects.filter(contact_type__in=[
                User.CONTACT.MODERATOR,
                User.CONTACT.TRAINER,
                User.CONTACT.SPORTSMAN
            ]).order_by('last_name', 'first_name', 'middle_name')
        elif User.Group.TRAINER in user:
            trainers = list(User.objects.filter(contact_type__in=[
                User.CONTACT.TRAINER,
            ]))
            my_students = list(user.students.all())
            return sorted(my_students + trainers, key=lambda x: x.last_name)
        return User.objects.none()


def get_chat(params):
    chat_id = params.get('chat', None)
    if chat_id is None:
        raise NotFound("Need chat id")
    chat = Chat.objects.filter(id=chat_id)
    if not chat.exists():
        raise NotFound("Chat does not exist")
    return chat[0]


def get_member(params):
    member_id = params.get('member', None)
    if member_id is None:
        raise NotFound("Need member id")
    member = User.objects.filter(id=member_id)
    if not member.exists():
        raise NotFound("Member does not exist")
    return member[0]


# TODO: check chat type
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leave_chat(request: Request):
    params = request.query_params
    chat = get_chat(params)
    if request.user not in chat.members.all():
        raise BadRequest('You are not in this chat')
    chat.members.remove(request.user)
    return Response(status=200)


# TODO: check rights
#       check chat type
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def remove_member(request: Request):
    params = request.query_params
    chat = get_chat(params)
    member = get_member(params)
    if member not in chat.members.all():
        raise BadRequest('User is not in this chat')
    chat.members.remove(member)
    return Response(status=200)
