import boto3
import sys
import time
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_invalidation(distribution_id, paths, aws_access_key, aws_secret_key, region_name):
    """
    Create an invalidation request for a specific CloudFront distribution.
    
    :param distribution_id: The ID of the CloudFront distribution.
    :param paths: List of paths to invalidate. Example: ['/*']
    :param aws_access_key: Your AWS access key.
    :param aws_secret_key: Your AWS secret key.
    :param region_name: The AWS region.
    :return: The invalidation ID.
    """
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )

    client = session.client('cloudfront')

    try:
        response = client.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(paths),
                    'Items': paths
                },
                'CallerReference': str(distribution_id) + '-' + str(int(time.time()))
            }
        )

        invalidation_id = response['Invalidation']['Id']
        print(f"Invalidation created for distribution {distribution_id}. Invalidation ID: {invalidation_id}")
        return invalidation_id

    except NoCredentialsError:
        print("Error: AWS credentials not found.")
        sys.exit(1)
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def main():
    # Load AWS credentials and region from environment variables
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region_name = os.getenv('AWS_DEFAULT_REGION')

    # Load CloudFront distribution IDs and corresponding site names/URLs from environment variables
    distribution_ids = {
        '1': {'id': os.getenv('DISTRIBUTION_ID_1'), 'name': 'https://stg.company.com'},
        '2': {'id': os.getenv('DISTRIBUTION_ID_2'), 'name': 'https://stg.admin.com'} # Add more distributions as needed
    }

    # Prompt the user to select distributions
    print("Select the CloudFront distributions to invalidate (e.g., 1,2,3):")
    for key, value in distribution_ids.items():
        print(f"{key}: {value['name']}")

    choices = input("Enter your choices (comma-separated): ").strip().split(',')

    selected_distributions = [distribution_ids[choice.strip()] for choice in choices if choice.strip() in distribution_ids]

    if not selected_distributions:
        print("Invalid choice(s). Please enter valid numbers corresponding to the distributions.")
        sys.exit(1)

    # Paths to invalidate
    paths_to_invalidate = ['/*']  # You can customize the paths here

    # Invalidate the selected distributions
    for distribution in selected_distributions:
        print(f"Invalidating {distribution['name']}...")
        create_invalidation(distribution['id'], paths_to_invalidate, aws_access_key, aws_secret_key, region_name)

if __name__ == "__main__":
    main()
