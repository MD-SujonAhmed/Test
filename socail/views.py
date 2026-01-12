from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MessengerMessage
from .serializers import MessengerMessageSerializer

VERIFY_TOKEN = "Test_123"  # Meta Dashboard verify token


class MessengerWebhookView(APIView):

    def get(self, request, *args, **kwargs):
        """
        1. Facebook Webhook verification
        2. Normal GET request → message list
        """

        # Facebook webhook verification parameters
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        # Webhook verification request
        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                return Response(challenge, status=status.HTTP_200_OK)
            return Response("Verification failed", status=status.HTTP_403_FORBIDDEN)

        # Normal GET request → return saved messages
        messages = MessengerMessage.objects.all().order_by('-timestamp')
        serializer = MessengerMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Receive Facebook Messenger webhook POST events
        """

        data = request.data

        # Required structure validation
        if 'entry' not in data:
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = data['entry'][0]
            messaging = entry.get('messaging', [])

            if not messaging:
                return Response({"error": "No messaging data"}, status=status.HTTP_200_OK)

            event = messaging[0]

            # Ignore non-message events
            if 'message' not in event or 'text' not in event['message']:
                return Response({"status": "Event ignored"}, status=status.HTTP_200_OK)

            sender_id = event['sender']['id']
            message_text = event['message']['text']

            message = MessengerMessage.objects.create(
                sender_id=sender_id,
                message_text=message_text
            )

            serializer = MessengerMessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except (KeyError, IndexError):
            return Response(
                {"error": "Invalid payload"},
                status=status.HTTP_400_BAD_REQUEST
            )
