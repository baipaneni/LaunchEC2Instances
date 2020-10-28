
from botocore.exceptions import ClientError

from log import get_logger

logger = get_logger(__name__)


class SecurityGroups:

    def __init__(self, ec2_client):
        self.ec2_client = ec2_client

    def get_security_group(self, vpc_id, group_name):
        """ Get Security group with in VPC """
        response = self.ec2_client.describe_security_groups(
            Filters=[
                {
                    'Name': 'group-name',
                    'Values': [
                        group_name,
                    ]
                },
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id,
                    ]
                },
            ]
        )

        if response.get('SecurityGroups'):
            return response.get('SecurityGroups', [{}])[0].get('GroupId', '')
        else:
            return None

    def create_security_group(self, vpc_id, group_name) -> str:
        """ Create Security group"""
        security_group_id = self.get_security_group(vpc_id, group_name)
        if security_group_id:
            return security_group_id

        try:
            response = self.ec2_client.create_security_group(GroupName=group_name,
                                                             Description='allow ssh users',
                                                             VpcId=vpc_id)
            security_group_id = response['GroupId']
            logger.info("Security Group Created {security_group_id} in vpc {vpc_id}.".format(
                security_group_id=security_group_id,
                vpc_id=vpc_id))

            self.ec2_client.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                     'FromPort': 22,
                     'ToPort': 22,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
            return security_group_id

        except ClientError as e:
            raise e
