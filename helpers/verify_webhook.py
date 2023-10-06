import os
from flask import jsonify
from dotenv import load_dotenv


def verify_webhook(request):
    """
    Verifies the webhook set up by returning hub.challenge if hub.verify_token matches VERIFY_TOKEN, error otherwise.
    """
    # Load environment variables from .env file
    load_dotenv()

    my_verify_token = os.environ.get('VERIFY_TOKEN')
    hub_mode = request.args.get("hub.mode")
    hub_verify_token = request.args.get("hub.verify_token")
    hub_challenge = request.args.get("hub.challenge")

    if hub_mode and hub_verify_token and hub_challenge:
        # If tokens match
        if hub_verify_token == my_verify_token:
            print("WEBHOOK SET UP OK.")
            return hub_challenge, 200

        print("INVALID TOKEN.")
        return jsonify({"success": False, "error": {"code": 403, "msg": "Invalid token."}}), 403

    print("MISSING PARAMETERS.")
    return jsonify({"success": False, "error": {"code": 400, "msg": "Missing parameter(s)."}}), 400
