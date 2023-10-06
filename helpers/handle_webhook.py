from dotenv import load_dotenv
from flask import jsonify

from .handle_text_message import handle_text_message


TEXT_MESSAGE_OBJECT = "whatsapp_business_account"

def handle_webhook(request):
    """
    Handles webhook notifications (e.g. messages).
    """
    # Load environment variables from .env file
    load_dotenv()

    notification_body = request.get_json()
    try:
        if notification_body.get("entry") and notification_body.get("object") == TEXT_MESSAGE_OBJECT:
            # Handle text message notifications.
            if notification_body.get("entry")[0].get("changes")[0].get("value").get("messages")[0].get("type") == "text":
                print("TEXT MESSAGE.")
                handle_text_message(request)
            else:
                print("UNKNOWN NOTIFICATION.")
            return jsonify({"success": True, "status": "ok", "msg": "Notification handled Ok."}), 200
        else:
            print("INVALID NOTIFICATION FORMAT.")
            return jsonify({"success": False, "error": {"code": 404, "Invalid notification format.": f"{e}"}}), 404
    except Exception as e:
        print(f"UNKNOWN SERVER ERROR: {e}.")
        return jsonify({"success": False, "error": {"code": 500, "msg": str(e)}}), 500
