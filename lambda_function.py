import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import boto3


def get_sendgrid_api_key():
    """Fetch SendGrid API key from AWS Secrets Manager."""
    secret_name = "email-credentials"  
    region_name = "us-east-1"

    # Create a Secrets Manager client
    client = boto3.client(service_name="secretsmanager", region_name=region_name)

    try:
        # Retrieve the secret value
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        return secret
    except Exception as e:
        print(f"Error retrieving the secret: {str(e)}")
        raise e

def parse_sns_message(event):
    """Parse the SNS message to extract the email and first_name."""
    for record in event['Records']:
        sns_message = record['Sns']['Message']
    sns_message_json = json.loads(sns_message)
    email = sns_message_json.get("email")
    first_name = sns_message_json.get("first_name")
    token = sns_message_json.get("token")
    return email, first_name, token

def generate_verification_link(email,token):
    secrets = get_sendgrid_api_key()
    """Generate a unique verification link."""
    domain_url = secrets["DOMAIN_NAME"]
    # verification_link = f"http://127.0.0.1:8000/verify?user={email}&token={token}"
    verification_link = f"https://{domain_url}/verify?user={email}&token={token}"
    return verification_link


def send_verification_email(email, first_name, verification_link):
    """Send a verification email to the user."""
    secrets = get_sendgrid_api_key()
    body = f"""
    Hi {first_name},
 
    Please verify your email address by clicking the given link below:
 
    {verification_link}
 
    This link will expire in 2 minutes.
    """

    message = Mail(
        from_email=f'noreply@{secrets["DOMAIN_NAME"]}',
        to_emails=email,
        subject='Verify email address for Webapp',
        html_content=body
    )

    try:
        sg = SendGridAPIClient(secrets['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(f"Email sent to {email}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise e


def lambda_handler(event, context):
    """Main Lambda handler function."""
    try:
        # Parse SNS message
        email, first_name, token = parse_sns_message(event)

        # Generate verification link
        verification_link = generate_verification_link(email, token)

        # Send verification email
        send_verification_email(email, first_name, verification_link)

        return {
            'statusCode': 200,
            'body': 'User emailed with verification link successfully'
        }

    except Exception as e:
        print(f"Error in Lambda execution: {str(e)}")
        return {
            'statusCode': 503,
            'body': f'Error: {str(e)}'
        }
