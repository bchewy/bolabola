from flask import Flask, jsonify, request
import boto3
from botocore.exceptions import ClientError
from functools import lru_cache
from dotenv import load_dotenv
import os
import json
import requests

app = Flask(__name__)
load_dotenv()

os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
os.environ["AWS_DEFAULT_REGION"] = "ap-southeast-1"
# os.environ["12LAB_KEY"] = os.getenv("12LAB_KEY")

print("AWS_ACCESS_KEY_ID: " + os.getenv("AWS_ACCESS_KEY_ID"))
print("AWS_SECRET_ACCESS_KEY: " + os.getenv("AWS_SECRET_ACCESS_KEY"))
# print("12LAB_KEY: " + os.getenv("12LAB_KEY"))

# DynamoDB credentials from environment variables
dynamodb_credentials = {
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "region_name": os.getenv("AWS_DEFAULT_REGION"),
}
dynamodb = boto3.resource("dynamodb", **dynamodb_credentials)
table = dynamodb.Table("ESD-VideoMetaData")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION"),
)
bucket_name = "esd-videometadata-assets"

# Create the S3 bucket if it does not exist
try:
    s3.head_bucket(Bucket=bucket_name)
except ClientError:
    # The bucket does not exist or you have no access.
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            "LocationConstraint": os.getenv("AWS_DEFAULT_REGION")
        },
    )
    # Set the new bucket to have public read access
    s3.put_bucket_acl(Bucket=bucket_name, ACL="public-read")
    print(f"Bucket {bucket_name} created and set to public read access.")
else:
    print(f"Bucket {bucket_name} already exists and is accessible.")


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
    video_url = request.json.get("video_url")
    match_id = request.json.get("match_id")
    if not video_url:
        return jsonify({"error": "No video URL provided"}), 400

    try:
        # Send video_url to 12labs API and get video_id as response
        response = requests.post(
            "https://api.12labs.com/upload",
            json={"video_url": video_url},
            headers={"Authorization": "Bearer tlk_0A7K1FP1A5EK902T611D205A8D51"},
        )
        response_data = response.json()
        if response.status_code == 200:
            video_id_12labs = response_data["video_id"]
            table.put_item(
                Item={
                    "match_id": match_id,
                    "video_url": video_url,
                    "video_id_12labs": video_id_12labs,
                }
            )
        else:
            return (
                jsonify({"error": "Failed to process video with 12labs"}),
                response.status_code,
            )
    except ClientError as e:
        print(e.response["Error"]["Message"])
        return jsonify({"error": "Failed to create video asset"}), 500
    except requests.exceptions.RequestException as e:
        print(e)
        return jsonify({"error": "Failed to communicate with 12labs API"}), 500
    else:
        return (
            jsonify(
                {
                    "message": "Video asset created successfully",
                    "video_id_12labs": video_id_12labs,
                    "video_url": video_url,
                }
            ),
            201,
        )


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
