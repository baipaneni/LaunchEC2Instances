import time
from typing import Dict

from ec2.ec2_user_data import EC2UserData
from ec2.ec2_logins import EC2Logins
from ec2.ec2_volumes import EC2Volumes
from ec2.ec2_ami import EC2AMI
from log import get_logger

logger = get_logger(__name__)


class Ec2Instance:
    def __init__(self, ec2_resource, ec2_client):
        self.ec2_resource = ec2_resource
        self.ec2_client = ec2_client

    def _get_public_ips(self, ec2_ids):
        """ Get Public IPs for EC2 Instances"""
        public_ips = []

        for ec2_id in ec2_ids:
            while True:
                response = self.ec2_client.describe_instances(InstanceIds=[ec2_id])
                ec2_info = response['Reservations'][0]['Instances'][0]
                logger.info(ec2_info)
                if ec2_info['PublicIpAddress']:
                    logger.info("Public IP for EC2 instance " + ec2_id + ":  " + ec2_info['PublicIpAddress'])
                    public_ips.append(ec2_info['PublicIpAddress'])
                    break
                else:
                    logger.info("Still waiting for Public IP to be configured for " + ec2_id)
                    time.sleep(10)

        return public_ips

    def launch_instances(self, ec2_launch_config: Dict, security_group_id: str, ec2_logins: EC2Logins):
        """ Launch EC2 instances based on config """
        ec2_ids = []
        ec2_volumes = EC2Volumes(ec2_launch_config['volumes'], ec2_launch_config['root_device_type'])
        user_data = EC2UserData(ec2_logins, ec2_volumes).get_user_data()
        ami_id = EC2AMI(self.ec2_client).get_latest_ami_id(
            ami_type=ec2_launch_config['ami_type'],
            architecture=ec2_launch_config['architecture'],
            virtualization_type=ec2_launch_config['virtualization_type'],
            root_device_type=ec2_volumes.root_device_type,
            root_device_name=ec2_volumes.root_device_name
        )

        ec2_instances = self.ec2_resource.create_instances(
            ImageId=ami_id,
            MinCount=ec2_launch_config['min_count'],
            MaxCount=ec2_launch_config['max_count'],
            InstanceType=ec2_launch_config['instance_type'],
            SecurityGroupIds=[security_group_id],
            UserData=user_data,
            BlockDeviceMappings=ec2_volumes.get_block_device_mappings()

        )

        for ec2 in ec2_instances:
            ec2.wait_until_running()
            ec2_ids.append(ec2.instance_id)

        return self._get_public_ips(ec2_ids)
