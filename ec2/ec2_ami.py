from log import get_logger

logger = get_logger(__name__)


class EC2AMI:

    def __init__(self, ec2_client):
        self.ec2_client = ec2_client

    def get_latest_ami_id(self, ami_type, architecture, virtualization_type, root_device_type, root_device_name):
        """Getting latest AMI id"""
        images = self.ec2_client.describe_images(
            Filters=[
                {
                    'Name': 'architecture',
                    'Values': [
                        architecture,
                    ]
                },
                {
                    'Name': 'virtualization-type',
                    'Values': [
                        virtualization_type
                    ]
                },
                {
                    'Name': 'root-device-type',
                    'Values': [
                        root_device_type
                    ]
                },
                {
                    'Name': 'block-device-mapping.device-name',
                    'Values': [
                        root_device_name
                    ]
                },
                {
                    'Name': 'state',
                    'Values': [
                        'available'
                    ]
                },
                {
                    'Name': 'name',
                    'Values': [
                        ami_type + '-ami-' + virtualization_type + '*-' + root_device_type
                    ]
                }
            ],
            Owners=['amazon'],

        )
        available_images = [(i['ImageId'], i['CreationDate']) for i in images['Images'] if i['State'] == 'available']
        available_images.sort(key=lambda tup: tup[1], reverse=True)
        logger.info("Latest AMI Found : " + available_images[0][0])

        return available_images[0][0]
