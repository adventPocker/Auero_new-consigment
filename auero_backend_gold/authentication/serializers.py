from rest_framework import serializers
from .models import CustomUser, VendorProfile, Address
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country']

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Basic serializer for user registration (customer/normal user)
    Only includes essential fields needed for initial signup
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class VendorProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for vendor profile details
    Used when creating or updating vendor specific information
    """
    class Meta:
        model = VendorProfile
        fields = ['vendor_type', 'company_name', 'approved', 'profile_image', 'business_name', 'business_website', 'phone', 'country']

class VendorSignupSerializer(serializers.ModelSerializer):
    """
    Complete serializer for vendor registration
    Includes both user and vendor profile fields
    """
    vendor_profile = VendorProfileSerializer()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone_number', 'user_type', 'vendor_profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract vendor profile data
        vendor_profile_data = validated_data.pop('vendor_profile')
        # Force user_type to 'vendor'
        validated_data['user_type'] = 'vendor'
        
        # Create user
        user = CustomUser.objects.create_user(**validated_data)
        
        # Create associated vendor profile
        VendorProfile.objects.create(user=user, **vendor_profile_data)
        
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for returning user data in token responses
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['user_id'] = user.id
        token['email'] = user.email
        
        # Check if user is superuser first
        if user.is_superuser:
            token['user_type'] = 'admin'
        elif hasattr(user, 'user_type') and user.user_type:
            token['user_type'] = user.user_type
            
        token['username'] = user.username
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add token data for frontend
        refresh = self.get_token(self.user)
        
        # Structure the response to match frontend expectations
        user_data = UserSerializer(self.user).data
        
        # Format the response structure
        response = {
            'user': user_data,
            'tokens': {
                'access': data['access'],
                'refresh': data['refresh'],
            }
        }
        
        return response
