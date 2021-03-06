from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from identity_verification.rest import (
    IdentityVerificationViewSet,
    IdentityAttachmentUploadViewSet,
)

router = DefaultRouter()




router.register(r'identity', IdentityVerificationViewSet, base_name='identify')
router.register(r'identity-attachment', IdentityAttachmentUploadViewSet, base_name='identify-attachment')


api_urlpatterns = [
]

api_urlpatterns += router.urls


urlpatterns = [
    url(r'^api/', include(
        api_urlpatterns,
        namespace='api_identity_verification'),
        name='api_identity_verification'),
]
