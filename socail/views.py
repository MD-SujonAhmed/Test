from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MessengerMessage
from .serializers import MessengerMessageSerializer




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MessengerMessage
from .serializers import MessengerMessageSerializer

VERIFY_TOKEN = "Test_123"  # Meta dashboard-এ যেটা দেবেন

class MessengerWebhookView(APIView):

    def get(self, request, *args, **kwargs):
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return Response(challenge, status=200)
        else:
            return Response("Verification failed", status=403)

    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            entry = data['entry'][0]
            messaging_event = entry['messaging'][0]
            sender_id = messaging_event['sender']['id']
            message_text = messaging_event['message']['text']

            message = MessengerMessage.objects.create(
                sender_id=sender_id,
                message_text=message_text
            )

            serializer = MessengerMessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError:
            return Response(
                {"error": "Invalid payload"},
                status=status.HTTP_400_BAD_REQUEST
            )


class MessengerWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        # Facebook থেকে আসা JSON ডেটা
        data = request.data

        # সাধারণভাবে message structure দেখতে এমন:
        # {
        #     "object": "page",
        #     "entry": [
        #         {
        #             "messaging": [
        #                 {
        #                     "sender": {"id": "USER_ID"},
        #                     "message": {"text": "Hello"}
        #                 }
        #             ]
        #         }
        #     ]
        # }

        try:
            entry = data['entry'][0]
            messaging_event = entry['messaging'][0]
            sender_id = messaging_event['sender']['id']
            message_text = messaging_event['message']['text']

            # মেসেজ ডাটাবেসে সংরক্ষণ
            message = MessengerMessage.objects.create(
                sender_id=sender_id,
                message_text=message_text
            )

            serializer = MessengerMessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError:
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
