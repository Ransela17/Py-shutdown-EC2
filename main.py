import sys
import time

import boto3
from botocore.exceptions import ClientError

# Getting tags from txt file at s3 bucket
s3 = boto3.resource('s3')
obj = s3.Object('ranselabucket', 'List_Tags.txt')
body = obj.get()['Body'].read().decode("utf-8")
list_of_tags = body.split(" ")

Stop_ec2 =[]

# checkTags boolean function that get instance and check are tags to protect
def checkTags(instance):
    for i in list_of_tags:
        if i in [tag['Key'] for tag in instance['Tags']]:  # third loop
            return True
    return False

# create ami image function for instances before shutting down
def createAMI(ec2instance):
    create_ami = ec2instance.create_image()
    create_ami.wait_until_exists(Filters=[{'Name': 'state', 'Values': ['available']}])

#
def stopInstance(Stop_ec2):
    try:
        for ec2instance in Stop_ec2:
            createAMI(ec2instance)
            ec2Client.stop_instances(InstanceIds=[ec2instance], DryRun=False)
            print('instance' + ec2instance + 'stop')
    except ClientError as e:
        print(e)


if __name__ == '__main__':
    print('My First ec2 Client')

    ec2Client = boto3.client( # Connect AWS Data
        'ec2',
        aws_access_key_id="AKIARJ3HHC6PNW2LGBPZ",
        aws_secret_access_key="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"
    )

    print('Import start')
    ec2Instances = ec2Client.describe_instances() # get all data about instances

    for reservation in ec2Instances['Reservations']: # first loop
        for instance in reservation['Instances']: # second loop
            if not checkTags(instance):
                Stop_ec2.append(instance['InstanceId'])  # insert to ec2 stopped list
                print('instace' + instance['InstanceId'] + 'add to list')
            else:
                print('instance' + instance['InstanceId'] + 'keep running' )
    stopInstance(Stop_ec2)


