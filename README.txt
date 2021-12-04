# Python Script - Shut down all the ec2 instances with no protect tag
Can be used for dev environment

the steps:
1. Connect AWS Data
2. Getting tags from txt file at s3 bucket
3. Checking Tags - get instance and check if there are tags for protect or not
4. For all instance with no protect tag - reate ami image before shutting down
5. Stop instances