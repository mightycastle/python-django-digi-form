from rest_framework import viewsets
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)
from rest_framework.response import Response

from core.rest_pagination import get_pagination_class
from .models import (
    FormDocument,
    FormDocumentResponse,
)
from .serializers import (
    FormDocumentSerializer,
    FormDocumentDetailSerializer,
    FormDocumentResponseSerializer,
)
from form_document.models import AUTO_SAVED


class FormDocumentViewSet(viewsets.ModelViewSet):
    queryset = FormDocument.objects.all()
    serializer_class = FormDocumentSerializer
    pagination_class = get_pagination_class(page_size=10)
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def get_object_kwarg(self):
        kwargs = {}
        if self.request.user.is_authenticated():
            kwargs['owner'] = self.request.user
        return kwargs

    def perform_create(self, serializer):
        kwargs = self.get_object_kwarg()
        return serializer.save(**kwargs)

    def perform_update(self, serializer):
        return serializer.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        else:
            return FormDocumentDetailSerializer

    def get_form_response(self, response_id):
        # get FormDocumentResponse object
        try:
            form_response = FormDocumentResponse.objects.get(id=response_id)
        except FormDocumentResponse.DoesNotExist:
            return None
        serializer = FormDocumentResponseSerializer(form_response)
        return serializer.data


class FormDocumentResponseViewSet(viewsets.ModelViewSet):
    queryset = FormDocumentResponse.objects
    serializer_class = FormDocumentResponseSerializer

    def get_object_kwarg(self):
        request_action = self.request.data['request_action']
        form_document = None
        form_id = self.request.data['form_id']
        if form_id:
            form_document = FormDocument.objects.get(pk=form_id)
        kwargs = {}
        if form_document:
            kwargs['form_document'] = form_document
        if 'FORM_AUTOSAVE' == request_action:
            kwargs['status'] = AUTO_SAVED
        if self.request.user.is_authenticated():
            kwargs['receiver_user'] = self.request.user

        return kwargs

    def perform_create(self, serializer):
        kwargs = self.get_object_kwarg()
        inst = serializer.save(**kwargs)
        return inst

    def perform_update(self, serializer):
        kwargs = self.get_object_kwarg()
        inst = serializer.save(**kwargs)
        return inst
