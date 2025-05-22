from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


from .serializers import (
    CustomUserSerializer, 
    VendorSignupSerializer,
    AddressSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer
)
from .models import CustomUser, Address

class CustomerSignupView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                # Use UserSerializer to format user data
                user_data = UserSerializer(user).data
                
                return Response({
                    'status': 'success',
                    'message': 'Customer registration successful',
                    'user': user_data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED)
            return Response({
                'status': 'error',
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VendorSignupView(generics.CreateAPIView):
    serializer_class = VendorSignupSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            # Ensure all required fields are present
            required_user_fields = ['username', 'email', 'password']
            required_vendor_fields = ['vendor_type']
            
            # Validate user fields
            missing_user_fields = [field for field in required_user_fields 
                                 if not request.data.get(field)]
                       
            if missing_user_fields:
                print("mssing user fields")
                return Response({
                    'status': 'error',
                    'message': f'Missing required user fields: {", ".join(missing_user_fields)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate vendor fields
            vendor_data = request.data.get('vendor_profile', {})
            missing_vendor_fields = [field for field in required_vendor_fields 
                                   if not vendor_data.get(field)]
            
            # Additional validation for company type vendors
            if vendor_data.get('vendor_type') == 'company':
                company_fields = ['company_name', 'contact_person']
                missing_company_fields = [field for field in company_fields 
                                        if not vendor_data.get(field)]
                if missing_company_fields:
                    print(f'Company vendors must provide: {", ".join(missing_company_fields)}')
                    return Response({
                        'status': 'error',
                        'message': f'Company vendors must provide: {", ".join(missing_company_fields)}'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Prepare the complete data for serialization
            complete_data = {
                'username': request.data.get('username'),
                'email': request.data.get('email'),
                'password': request.data.get('password'),
                'phone_number': request.data.get('phone_number'),
                'user_type': 'vendor',  # Force user_type to vendor
                'vendor_profile': {
                    'vendor_type':'individual',
                    'company_name': vendor_data.get('company_name'),
                    'profile_image': vendor_data.get('profile_image')
                }
            }

            serializer = self.serializer_class(data=complete_data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                # Use UserSerializer for consistent user data format
                user_data = UserSerializer(user).data
                
                # Add vendor profile data to the response
                if hasattr(user, 'vendor_profile'):
                    user_data['vendor_profile'] = {
                        'vendor_type': user.vendor_profile.vendor_type,
                        'company_name': user.vendor_profile.company_name,
                        'approved': user.vendor_profile.approved
                    }
                
                response_data = {
                    'status': 'success',
                    'message': 'Vendor registration successful',
                    'user': user_data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response({
                'status': 'error',
                'message': 'Invalid data provided',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            print("its validation error")
            print(e.detail)
            return Response({
                'status': 'error',
                'message': 'Validation error',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("an occur suring regusteration")
            print(str(e))
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred during registration',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            # The serializer expects 'username' field, but frontend sends 'email'
            data = request.data.copy()  # Make a mutable copy of the data
            
            # If the request contains 'email' but not 'username', use email as username
            if 'email' in data and not 'username' in data:
                data['username'] = data['email']
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({
                'status': 'error',
                'message': 'Invalid credentials'
            }, status=e.status_code)
        except ValidationError as e:
            return Response({
                'status': 'error',
                'message': 'Validation error',
                'errors': e.detail
            }, status=e.status_code)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An unexpected error occurred',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
                
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({"status": "success", "message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    """
    View to retrieve and update current authenticated user's information
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user)
            response_data = serializer.data
            if user.user_type == 'vendor' and hasattr(user, 'vendor_profile'):
                response_data['vendor_profile'] = {
                    'vendor_type': user.vendor_profile.vendor_type,
                    'company_name': user.vendor_profile.company_name,
                    'contact_person': getattr(user.vendor_profile, 'contact_person', None),
                    'approved': user.vendor_profile.approved,
                    'profile_image': request.build_absolute_uri(user.vendor_profile.profile_image.url) if user.vendor_profile.profile_image else None
                }
            return Response({
                'status': 'success',
                'user': response_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'user': serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({'status': 'error', 'message': 'Old password is incorrect.'}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({'status': 'success', 'message': 'Password changed successfully.'})

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        from .models import CustomUser
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'status': 'error', 'message': 'User with this email does not exist.'}, status=404)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        # Mock email sending: return token and uid in response
        return Response({'status': 'success', 'uid': uid, 'token': token, 'message': 'Password reset link (mocked) generated.'})

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            from .models import CustomUser
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({'status': 'error', 'message': 'Invalid link.'}, status=400)
        if not default_token_generator.check_token(user, token):
            return Response({'status': 'error', 'message': 'Invalid or expired token.'}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({'status': 'success', 'message': 'Password has been reset successfully.'})
