import hashlib
import os
from mailchimp_marketing import Client
import mailchimp
from mailchimp_marketing.api_client import ApiClientError
import mailchimp_transactional
from dotenv import load_dotenv
from mailchimp_transactional.api_client import ApiClientError

load_dotenv()

def mark_user_as_subscribed_in_mailchimp(email):
    # Initialize the Mailchimp client
    client = Client()
    client.set_config({'api_key': os.environ.get('MAILCHIMP_API_KEY'), 'server': os.environ.get('MAILCHIMP_SERVER')})
    subscriber_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    list_id = os.environ.get('MAILCHIMP_AUDIENCE_ID')

    body = {
        'email_address': email,
        'status': 'subscribed',
        'merge_fields': {
            'ADDRESS': {
                'addr1': '123 Main St',
                'city': 'Anytown',
                'state': 'CA',
                'zip': '12345',
                'country': 'United States'
            }
        }
    }

    try:
        response = client.lists.set_list_member(list_id, subscriber_hash, body)
        
        print("User marked as verified in Mailchimp.", response)
    except ApiClientError as error:
        print("Mailchimp API error:", error)
    
def send_email_using_mailchimp(to_email,username, url):
    mailchimp = mailchimp_transactional.Client(os.environ.get('MAILCHIMP_API_KEY'))

    # Define the message parameters
    ##### NOTE: I have commented the mail sending attributes which are not required for me
    message = {
        "html": "<p>Hello, this is the HTML content of your email.</p>",
        "text": f"Hi {username}\n Use the link below to verify your email \n{url}",
        "subject": "Email Verification",
        "from_email": "ishika.shah@mindinventory.com",
        # "from_name": "Ishika Shah",
        "to": [
            {
                "email": to_email,
                # "name": 'Ishika Shah',
                "type": "to"
            }
        ],
        "headers": {
            "Reply-To": "reply-to@example.com"
        },
        # "important": False,
        # "track_opens": True,
        # "track_clicks": True,
        # "auto_text": True,
        # "auto_html": False,
        # "inline_css": True,
        # "url_strip_qs": False,
        # "preserve_recipients": True,
        # "view_content_link": True,
        # "bcc_address": "bcc@example.com",
        # "tracking_domain": "tracking.example.com",
        # "signing_domain": "example.com",
        # "return_path_domain": "returnpath.example.com",
        # "merge": True,
        # "merge_language": "handlebars",
        # "global_merge_vars": [
        #     {
        #         "name": "global_var1",
        #         "content": "Global Variable 1 Content"
        #     }
        # ],
        # "merge_vars": [
        #     {
        #         "rcpt": "recipient@example.com",
        #         "vars": [
        #             {
        #                 "name": "merge_var1",
        #                 "content": "Recipient 1 Merge Variable 1 Content"
        #             }
        #         ]
        #     }
        # ],
        # "tags": ["tag1", "tag2"],
        # "subaccount": "subaccount_id",
        # "google_analytics_domains": ["example.com"],
        # "google_analytics_campaign": "your_campaign",
        # "metadata": {
        #     "website": "example.com"
        # },
        # "recipient_metadata": [
        #     {
        #         "rcpt": "recipient@example.com",
        #         "values": {
        #             "user_id": 12345
        #         }
        #     }
        # ],
        # "attachments": [
        #     {
        #         "type": "text/plain",
        #         "name": "myfile.txt",
        #         "content": "SGVsbG8gV29ybGQh\n"
        #     }
        # ],
        # "images": [
        #     {
        #         "type": "image/png",
        #         "name": "IMAGECID",
        #         "content": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAF8SURBVHjadJPfS5NhFMd/21FVE1IbJJDVqQ2qQ5kUXYFCoKkUcPQRpugRZkFETFp5W8D+//+uUupLr7Kz4XoEJmwklp5UUVQuHgJvfb6/G+HUikoNaToJLf65vt+8X0M7A6rZ8rxgmXAC9AeZ/H2+NmNdDgCTeZr4M5kAEk/R3gZ8ANngQfgBvAHTAfAByADVnj7YFie2j/GL8F6IXeCN3AGlZtdK8WrgD8cjnKu4rAI5/PJdQZlllVmXbADp6atz+6kc9FkMikJv4TJdBJuJ+5ZT3EVhr9VsFtoAxu8L4gtPwLeBXkBSVOc1VwD+qTt8bR8KfWTnAHIKdT0AAAAASUVORK5CYII=\n"
        #     }
        # ]
    }

    try:
        # Send the transactional message
        response = mailchimp.messages.send({"message": message})
        print(response)
    except ApiClientError as error:
        print(f"An exception occurred: {error.text}")