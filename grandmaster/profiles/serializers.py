from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class DocumentsDetailsSerializer(serializers.ModelSerializer):
    other_documents = serializers.SerializerMethodField('get_other_documents')

    class Meta:
        model = User
        fields = [
            'passport_or_birth_certificate',
            'oms_policy',
            'school_ref',
            'insurance_policy',
            'tech_qual_diplo',
            'med_certificate',
            'foreign_passport',
            'inn',
            'diploma',
            'snils',
            'other_documents'
        ]

    def get_other_documents(self, obj):
        request = self.context.get("request")
        return [request.build_absolute_uri(el.image.url) for el in obj.other_documents.all()]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'full_name'
        ]



class UserDetailsSerializer(serializers.ModelSerializer):
    documents = serializers.HyperlinkedIdentityField(
        view_name='documents-detail'
    )
    admitted = serializers.BooleanField(source='is_admitted')
    parents = UserSerializer(many=True)
    children = UserSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'documents',
            'admitted',
            'photo',
            'gender',
            'first_name',
            'last_name',
            'middle_name',
            'birth_date',
            'contact_type',
            'phone_number',
            'sport_school',
            'department',
            'trainer_name',
            'training_place',
            'tech_qualification',
            'sport_qualification',
            'weight',
            'height',
            'region',
            'city',
            'address',
            'school',
            'med_certificate_date',
            'insurance_policy_date',
            'father_full_name',
            'father_birth_date',
            'father_phone_number',
            'father_email',
            'mother_full_name',
            'mother_birth_date',
            'mother_phone_number',
            'mother_email',
            'children',
            'parents',
        ]


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url']

    def to_representation(self, instance):
        return reverse('user-detail', args=[instance.pk])
