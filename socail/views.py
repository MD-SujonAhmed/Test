from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MessengerMessage
from .serializers import MessengerMessageSerializer

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
