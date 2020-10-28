
class EC2Volumes:
    def __init__(self, volumes, root_device_type):
        self.volumes = volumes
        self.root_device_type = root_device_type
        self.root_device_name = self.get_root_device_name(volumes)

    def get_root_device_name(self, volumes):
        for volume_info in volumes:
            if volume_info['mount'] == '/':
                return volume_info['device']

    def get_block_device_mappings(self):
        block_device_mappings = []

        for volume_info in self.volumes:
            block_device_mappings.append(
                {
                    "DeviceName": volume_info['device'],
                    "Ebs":
                        {"VolumeSize": volume_info['size_gb']}
                }
            )

        return block_device_mappings

    def get_volumes(self):
        return self.volumes