from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import User

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class UserSerializer(serializers.ModelSerializer):
    role = ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    # def validate(self, data):
    #     if self.context['request'].user == data['following']:
    #         raise serializers.ValidationError(
    #             'Вы не можете подписываться на самого себя.')
    #     if Follow.objects.filter(
    #         user=self.context['request'].user,
    #         following=data['following']
    #     ).exists():
    #         raise serializers.ValidationError(
    #             'Вы уже подписаны на этого автора.')
    #     return data


class UserMeSerializer(serializers.ModelSerializer):
    role = ChoiceField(choices=User.ROLE_CHOICES, read_only=True)


    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        model = User