import boto3
import configparser
import os

AWS_CONFIG_PATH = os.path.expanduser("~/.aws/config")

def get_profiles():
    config = configparser.ConfigParser()
    config.read(AWS_CONFIG_PATH)
    profiles = []
    for section in config.sections():
        if section.startswith("profile "):
            profiles.append(section.replace("profile ", ""))
    return profiles

def list_ec2_instances(profile):
    session = boto3.Session(profile_name=profile)
    ec2 = session.client('ec2')
    regions = [r['RegionName'] for r in ec2.describe_regions()['Regions']]
    for region in regions:
        ec2_regional = session.client('ec2', region_name=region)
        resp = ec2_regional.describe_instances()
        for reservation in resp['Reservations']:
            for instance in reservation['Instances']:
                print(f"Profile: {profile}, Region: {region}")
                print(f"  InstanceId: {instance.get('InstanceId')}")
                print(f"  InstanceType: {instance.get('InstanceType')}")
                print(f"  State: {instance.get('State', {}).get('Name')}")
                print(f"  Private IP: {instance.get('PrivateIpAddress')}")
                print(f"  Public IP: {instance.get('PublicIpAddress')}")
                print(f"  Tags: {instance.get('Tags')}")
                print("-" * 40)

if __name__ == "__main__":
    profiles = get_profiles()
    for profile in profiles:
        try:
            list_ec2_instances(profile)
        except Exception as e:
            print(f"Error with profile {profile}: {e}")