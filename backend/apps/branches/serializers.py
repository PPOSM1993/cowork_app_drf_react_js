from rest_framework import serializers
from .models import Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'city', 'region', 'phone', 'email', 'image']


    def validate(self, data):
        if data['name'] == '':
            raise serializers.ValidationError('Branch name is required')
        elif data['address'] == '':
            raise serializers.ValidationError('Branch address is required')
        elif data['city'] == '':
            raise serializers.ValidationError('Branch city is required')
        elif data['region'] == '':
            raise serializers.ValidationError('Branch region is required')
        elif data['phone'] == '':
            raise serializers.ValidationError('Branch phone is required')
        elif data['email'] == '':
            raise serializers.ValidationError('Branch email is required')
        
        return data
    