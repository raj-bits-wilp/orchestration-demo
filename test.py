import boto3

# Specify the profile name
profile_name = 'LabRole'

# Create a session using the specified profile
session = boto3.Session(profile_name=profile_name)

# Create an S3 client using the session
s3 = session.client('s3')


# List objects in the specified bucket
response = s3.list_objects(Bucket='orchestration-demo')

# Print object keys
for obj in response.get('Contents', []):
    print(obj['Key'])
