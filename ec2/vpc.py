from log import get_logger

logger = get_logger(__name__)


class VPC:
    def __init__(self, ec2_client):
        self.ec2_client = ec2_client

    def get_default_vpc(self) -> str:
        """ Get default VPC or create default VPC if not exists"""
        default_vpc_id = None
        response = self.ec2_client.describe_vpcs()
        for vpc_info in response.get('Vpcs', [{}]):
            if vpc_info['IsDefault']:
                logger.info("Default VPC :" + vpc_info['VpcId'])
                default_vpc_id = vpc_info['VpcId']

        if not default_vpc_id:
            response = self.ec2_client.create_default_vpc()
            default_vpc_id = response['Vpc']['VpcId']

        return default_vpc_id
