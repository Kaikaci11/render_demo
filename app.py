from flask import Flask, send_file
import datetime
from basic_utils import read_file, read_json, update_tracking_ids_json_file, get_mime_type
import urllib.request
from io import BytesIO

app = Flask(__name__)


# Serve a default page. This function is not required.
@app.route('/')
def my_function():
    return "PhantomConnect"


@app.route('/store_image/<account_login>/<tracking_id>/<path:image_url>')
def store_image(account_login,tracking_id,image_url):

    update_tracking_ids_json_file(
        account_login,
        {tracking_id:image_url}
    )
    return "Image saved."


@app.route('/image/<account_login>/<tracking_id>')
def display_image(account_login,tracking_id):

    # Get the image path
    image_url = read_json(account_login).get(tracking_id,None)
    mime_type = get_mime_type(image_url)

    # Replace with your User-Agent string
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'

    headers = {'User-Agent': user_agent}

    req = urllib.request.Request(image_url, headers=headers)
    with urllib.request.urlopen(req) as response:
        image_data = response.read()

    if response.status_code == 200:

        # Get the current time of request and format time into readable format.
        current_time = datetime.datetime.now()
        timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")

        log_entry = f"{tracking_id},{timestamp}\n"

        # Write log to hardcoded path. Must be an absolute path to the log file.
        with open(f'{account_login}.txt', 'a') as f:
            f.write(log_entry)

        # Return the image data as a response without saving it locally
        return send_file(BytesIO(image_data), content_type=mime_type)

    else:
        # Handle the case where the external image could not be fetched
        return "Image not found", 404


@app.route('/log/<account_login>')
def email_logs(account_login):
    logs_path = f'{account_login}.txt'
    logs: str = read_file(logs_path)

    return logs

if __name__ == '__main__':
    app.run()