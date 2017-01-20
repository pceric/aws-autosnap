import os
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    client = ec2.meta.client
    results = client.describe_volumes(Filters=[{'Name': 'tag-key', 'Values': ['autosnap']},{'Name': 'status', 'Values': ['in-use']}])
    volumes = []
    for vol in results['Volumes']:
        print(vol['VolumeId'])
        volumes.append(vol['VolumeId'])
        snapshot = ec2.create_snapshot(VolumeId=vol['VolumeId'], Description='Lambda Auto Snapshot')
        snapshot.create_tags(Tags=[{'Key': 'Name', 'Value': vol['VolumeId'] + '-autosnap'}])
    results = client.describe_snapshots(Filters=[{'Name': 'tag:Name', 'Values': ['*-autosnap']}])
    for snap in results['Snapshots']:
        print(snap['SnapshotId'])
        if snap['StartTime'].date() <= (datetime.utcnow().date() - timedelta(int(os.getenv('RETENTION', '3')))):
            snapshot = ec2.Snapshot(snap['SnapshotId'])
            if snapshot.tags and 'locked' in map(lambda x: x['Key'], snapshot.tags):
                continue
            snapshot.delete()
    return True

