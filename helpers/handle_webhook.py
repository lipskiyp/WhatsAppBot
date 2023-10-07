from flask import jsonify

from .handle_messages import handle_messages


NOTIFICATION_OBJECT = "whatsapp_business_account"

def handle_webhook(request):
    """
    Handles webhook notifications (e.g. messages).
    """
    body = request.get_json()
    try:
        # Check payload structure matches: https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
        if(
            body.get("entry"),
            body.get("object") == NOTIFICATION_OBJECT,
        ):
            # Handle messages.
            if body.get("entry")[0].get("changes")[0].get("field") == "messages":
                handle_messages(body)
            else:
                print("UNKNOWN FIELD - PASS.")
            return jsonify({"success": True, "status": "ok", "msg": "Notification handled ok."}), 200
        else:
            print("INVALID NOTIFICATION FORMAT.")
            return jsonify({"success": False, "error": {"code": 404, "msg": "Invalid notification format."}}), 404

    except Exception as e:
        print(f"UNKNOWN SERVER ERROR: {e}.")
        return jsonify({"success": False, "error": {"code": 500, "msg": str(e)}}), 500
