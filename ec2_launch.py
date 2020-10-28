import argparse
import boto3
import yaml
import json

from ec2.ec2_instance import Ec2Instance
from ec2.ec2_logins import EC2Logins
from ec2.security_groups import SecurityGroups
from ec2.vpc import VPC
from log import get_logger

SSH_SECURITY_GROUP = "ssh_group"


def load_launch_config():
    """ Read YML config """
    logger.info("Loading EC2 launch YML config ....")
    with open(args.config_file, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    logger.info("EC2 config:\n " + json.dumps(config['server'], indent=4))
    return config['server']


def print_ssh_commands(ec2_public_ips, ec2_logins):
    """ Print SSH command for end user for login purpose"""
    ssh_cmd = ''
    for ec2_public_ip in ec2_public_ips:
        for login, ec2_login in ec2_logins.get_logins().items():
            ssh_cmd += "\n\t\tssh -oStrictHostKeyChecking=no -l " + login + " -i " + ec2_login.ssh_keys_dir + "/id_rsa  " + ec2_public_ip
    logger.info("************    EC2 SSH Login Info    ******************\n{0}\n".format(ssh_cmd))

def launch_ec2():
    """ Main Launch method """
    aws_session = boto3.Session(
        region_name=args.aws_region,
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key
    )
    ec2_client = aws_session.client('ec2')
    ec2_resource = aws_session.resource('ec2')
    ec2_launch_config = load_launch_config()
    ec2_logins = EC2Logins()
    ec2_logins.populate_users_from_config(ec2_launch_config['users'])

    logger.info("Creating pre-requisites to launch EC2 instances")
    vpc_id = VPC(ec2_client).get_default_vpc()
    security_group_id = SecurityGroups(ec2_client).create_security_group(vpc_id, SSH_SECURITY_GROUP)
    ec2 = Ec2Instance(ec2_resource, ec2_client)
    logger.info("Done with pre-requisites to launch EC2 instances")

    ec2_public_ips = ec2.launch_instances(
        ec2_launch_config=ec2_launch_config,
        security_group_id=security_group_id,
        ec2_logins=ec2_logins
    )

    print_ssh_commands(ec2_public_ips, ec2_logins)


if __name__ == '__main__':
    logger = get_logger(__name__)
    parser = argparse.ArgumentParser(description='AWS EC2 Launch')
    parser.add_argument('--config_file', default='ec2_lunch_config.yml', help='YAML config_file')
    parser.add_argument('--aws_region', default='us-west-1', help='aws region to use')
    parser.add_argument('--aws_access_key_id', required=True, help='use aws access_key_id')
    parser.add_argument('--aws_secret_access_key', required=True, help='use aws_secret_access_key for key')
    args = parser.parse_args()

    launch_ec2()
