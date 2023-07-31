from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError
from .models import *

class UserloginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ['username','password']
    def validate(self, attrs):
        username = attrs.get('username')
        password=attrs.get('password')
        user =  User.objects.filter(username=username)
        if user is not None:
            if check_password(password,user.password):
                return super().validate(attrs)
            else:
                raise ValidationError('password not match')
        else:
            raise ValidationError('user not found')
            
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number','password','first_name','last_name']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    def update(self,instance,validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        password = validated_data.get('password')
        print(password)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
    def partial_update(self, instance, validated_data):
        # Perform partial update for the specified fields only
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Update the password if provided
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
class ListPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        if self.many and hasattr(value, 'all'):
            # For many=True, return a list of primary keys
            return [str(item) for item in value.all()]
        return super().to_representation(value)

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
        
class RoomSerializer(serializers.ModelSerializer):
    # host = serializers.SerializerMethodField()
    # topic = serializers.SerializerMethodField()
    # host = UserSerializer(read_only=True)
    # topic = TopicSerializer(read_only=True)
    participants = UserSerializer(many=True)
    # participants = serializers.ListField(
    #     child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # )
    # participants = serializers.ManyRelatedField(
       
        
       
        
    #     child_relation='participants',
    # )
    host = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())
    # participants = serializers.SerializerMethodField()
    # participants = ListPrimaryKeyRelatedField(queryset=User.objects.all())
    # host_id = serializers.IntegerField(write_only=True)
    # topic_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Room
        fields = ['id','host','topic','name','description','participants']
    def to_representation(self, instance):
        # Get the request method from the context
        method = self.context['request'].method

        # Customize the serialization output based on the request method
        if method == 'GET':
            # For GET requests, use nested serialization
            return {
                **super().to_representation(instance),
                'host': UserSerializer(instance.host).data,
                'topic': TopicSerializer(instance.topic).data
                # 'participants': UserSerializer()
            }
        # else:
        #     # For other requests (e.g., POST), use primary key serialization
        #     return super().to_representation(instance)
    # def get_host(self, obj):
    #     # Check if the request method is GET
    #     if self.context['request'].method == 'GET':
    #         # Use nested serialization for GET requests
    #         print(obj)
    #         return UserSerializer(obj.host).data
    #     else:
    #         # Use primary key serialization for other requests (e.g., POST)
    #         return obj.host_id

    # def get_topic(self, obj):
    #     # Check if the request method is GET
    #     if self.context['request'].method == 'GET':
    #         # Use nested serialization for GET requests
    #         return TopicSerializer(obj.topic).data
    #     else:
    #         # Use primary key serialization for other requests (e.g., POST)
    #         return obj.topic_id
    def create(self, validated_data):
        # Get the nested host data from the validated data
        print(validated_data)
        host = validated_data.pop('host')
        topic = validated_data.pop('topic')
        print(validated_data)
        # host = User.objects.filter(id=host_id)
        # topic = Topic.objects.filter(id=topic_id)
        # print(host_id)


        # Create or update the host based on the provided data
        # host, created = User.objects.get_or_create(**host_data)
        # topic,created = Topic.objects.get_or_create(id=topic_id)
        participants_data = validated_data.pop('participants')

        # Create the Room instance using the remaining validated data
        room = Room.objects.create(host=host,topic = topic,**validated_data)
        # room.host.set(host)
        # room.topic.set(topic)

        # Handle the participants, if provided
        if participants_data is not None:
            for participant_data in participants_data:
                participant, created = User.objects.get_or_create(**participant_data)
                room.participants.set(participant)

        return room

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Message
        fields = '__all__'