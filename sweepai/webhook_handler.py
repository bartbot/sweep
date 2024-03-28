import logging

from flask import Flask, request

from sweepai.utils.gitlab_utils import (GitLabAPIError, get_gitlab_client,
                                        get_mr_comments, get_mr_details,
                                        post_mr_comment)

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.json
    logging.info("Received data: %s", data)
    # Process GitLab webhook events
    if 'object_kind' in data and data['object_kind'] == 'merge_request':
        project_id = data['project']['id']
        mr_id = data['object_attributes']['id']
        token = 'your_private_token_here'  # This should be securely retrieved from environment variables or configuration
        comment = 'Thank you for your merge request!'
        try:
            post_mr_comment(project_id, mr_id, comment, token)
            logging.info("Posted comment on MR #%d", mr_id)
        except GitLabAPIError as e:
            logging.error("Failed to post comment on MR: %s", e)
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
