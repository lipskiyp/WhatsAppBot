# WhatsApp API Bot (In Progress)

WhatsApp API Bot with a Flask server, launched using ngrok.

### The server can currently handle:

* Initial webhook configuration and token verification with Meta.
* Incoming messages - server marks the incoming message as "read" and responds with a default greeting text message.
* Prints status updates for the outhoing messages (e.g. "delivered", "read" etc.)

### The app requires the following variables to be stored inside the environment for it to work:

* WHATSAPP_TOKEN - (temporary) Meta access token (can be found inside the "API Set Up" section on the Meta for Developers website).
* VERIFY_TOKEN - your own verification token to be used for the webhook configuration (can be any string).
* GRAPH_BASE_API - base graph API url (currently version 17 is used - https://graph.facebook.com/v17.0/).
* PHONE_NUMBER_ID - your sender WhatsApp phone number id.

## main.py

Flask main app with all of the server endpoints.

## /helpers/verify_webhook.py

Handles the initial webhook set up and token verification logic for GET requests to /mywebhook endpoint.

## /helpers/handle_webhook.py

Handles logic for the webhook notifications.

## /helpers/handle_text_message.py

Handles logic for text messages.
