from flask import Flask, jsonify, request
import boto3
from botocore.exceptions import ClientError
from functools import lru_cache
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"

dynamodb = boto3.resource("dynamodb")

print(os.getenv("AWS_ACCESS_KEY_ID"))
print(os.getenv("AWS_SECRET_ACCESS_KEY"))
table = dynamodb.Table("ESD-VideoMetaData")

# it is important to note here that the √ideo id equals to the match id.


# Cache size depends on your needs; here, we cache the latest 128 requests
@lru_cache(maxsize=128)
def get_video_path(video_id):
    try:
        # The video id here refers to the match id.
        response = table.get_item(Key={"video_id": video_id})
        # Corrected the print statement to properly format the dictionary as a string
        print("response:", response)
    except ClientError as e:
        # Print the error message from the exception
        print(e.response["Error"]["Message"])
        return None
    else:
        # Check if 'Item' key exists and then attempt to get 'video_url' from it
        item = response.get("Item")
        if item is not None:
            return item.get("video_url")
        else:
            # If 'Item' key does not exist, log it and return None
            print(f"No item found with video_id: {video_id}")
            return None


# Create video asset with video_id
@app.route("/ ", methods=["POST"])
def create_video_asset():
    video_id = request.json.get("id")
    video_url = request.json.get("url")

    if not video_id or not video_url:
        return jsonify({"error": "Missing fields, video id and url are required"}), 400
    video_urlink = video_url  # Use the provided video_url

    # Setting a default URL for all matches - can comment the one below ocne this works!
    video_urlink = "https://bchewy.s3.ap-southeast-1.amazonaws.com/Old+Trafford+Thriller+Manchester+United+vs+Liverpool.mp4"  # set as default

    # video_url = request.json.get("url")
    if not video_id or not video_urlink:
        return jsonify({"error": "Missing video id or url"}), 400
    try:
        table.put_item(Item={"video_id": video_id, "video_url": video_urlink})
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return jsonify({"error": "Failed to create video asset"}), 500
    else:
        return jsonify({"message": "Video asset created successfully"}), 201


@app.route("/video", methods=["GET"])
def get_video():
    video_id = request.args.get("id")
    print("video_id: " + str(video_id))
    if not video_id:
        return jsonify({"error": "Missing video id"}), 400

    video_path = get_video_path(video_id)
    print("video path: " + str(video_path))
    if video_path:
        return jsonify(video_path)
    else:
        return jsonify({"error": "Video not found"}), 404


if __name__ == "__main__":
    app.run(port=9005, debug=True, host="0.0.0.0")
