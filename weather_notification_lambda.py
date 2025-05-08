
import json
import urllib.request
import boto3

def lambda_handler(event, context):
    city = "New York"
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        message = f"Weather Update for {city}:
Condition: {weather}\nTemperature: {temp}°C\nHumidity: {humidity}%."

        sns = boto3.client("sns")
        sns.publish(
            TopicArn="arn:aws:sns:YOUR_REGION:YOUR_ACCOUNT_ID:YOUR_TOPIC_NAME",  # Replace with your SNS topic ARN
            Message=message,
            Subject="Daily Weather Update"
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Weather notification sent successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
