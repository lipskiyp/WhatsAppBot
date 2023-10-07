import os
import requests

def set_text_message_status(message_id, status="", sender_number_id="", verification_token=""):
    # Set status to "read" by default
    if not status:
        status = "read"
    # Uses the environment variables PHONE_NUMBER_ID for sender_number_id and WHATSAPP_TOKEN for verification_token if none provided.
    if not sender_number_id:
        sender_number_id = os.environ.get('PHONE_NUMBER_ID')
    if not verification_token:
        verification_token = os.environ.get('WHATSAPP_TOKEN')

    headers = {
        'Authorization': f'Bearer {verification_token}',
    }

    json_data = {
        'messaging_product': 'whatsapp',
        'status': status,
        "message_id": message_id,
    }

    endpoint = os.environ.get('GRAPH_BASE_API') + f"{sender_number_id}/messages"
    response = requests.post(endpoint, headers=headers, json=json_data)
    # Raise error if failed
    response.raise_for_status()

def send_text_message(message, recipient_number, sender_number_id="", verification_token=""):
    """
    Sends a WhatsApp text message: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages
    """
    # Uses the environment variables PHONE_NUMBER_ID for sender_number_id and WHATSAPP_TOKEN for verification_token if none provided.
    if not sender_number_id:
        sender_number_id = os.environ.get('PHONE_NUMBER_ID')
    if not verification_token:
        verification_token = os.environ.get('WHATSAPP_TOKEN')

    headers = {
        'Authorization': f'Bearer {verification_token}',
    }

    json_data = {
        'messaging_product': 'whatsapp',
        'to': str(recipient_number),
        'type': 'text',
        "text": {
            "body": str(message)
        }
    }

    endpoint = os.environ.get('GRAPH_BASE_API') + f"{sender_number_id}/messages"
    response = requests.post(endpoint, headers=headers, json=json_data)
    # Raise error if failed
    response.raise_for_status()

def handle_status_notifications(body):
    """
    Handles status notifications.
    """
    recipient_id = body.get("entry")[0].get("changes")[0].get("value").get("statuses")[0].get("recipient_id")
    message_status = body.get("entry")[0].get("changes")[0].get("value").get("statuses")[0].get("status")
    print(f"MESSAGE TO {recipient_id} STATUS UPDATE: {message_status}")

def handle_text_message(body):
    """
    Handles the incoming text-messages.
    """
    message = body.get("entry")[0].get("changes")[0].get("value").get("messages")[0].get("text").get("body")
    message_id = body.get("entry")[0].get("changes")[0].get("value").get("messages")[0].get("id")
    recipient_name = body.get("entry")[0].get("changes")[0].get("value").get("contacts")[0].get("profile").get("name")
    recipient_number = body.get("entry")[0].get("changes")[0].get("value").get("messages")[0].get("from")
    print(f'INCOMING TEXT MESSAGE: "{message}" FROM: "{recipient_number}"')

    # Set message status to "read".
    set_text_message_status(message_id=message_id, status="read")

    # Respond to the message
    send_text_message(
        message=f"Hey, {recipient_name}!",
        recipient_number=recipient_number
        )

def handle_messages(body):
    """
    Handles incoming messages notifications.
    """
    # Handle status notification
    if body.get("entry")[0].get("changes")[0].get("value").get("statuses"):
        handle_status_notifications(body)
        return

    message_type = body.get("entry")[0].get("changes")[0].get("value").get("messages")[0].get("type")
    # Handle text messages
    if message_type == "text":
        handle_text_message(body)
