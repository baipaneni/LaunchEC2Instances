from ec2.ec2_ssh_keys import SSHKeys
from log import get_logger

logger = get_logger(__name__)

GLOBAL_SSH_KEY_DIR = "/tmp/aws_ssh_keys"


class EC2Login:
    """Class for EC2 OS login info"""
    def __init__(self, login, ssh_public_key):
        self.login = login
        self.ssh_public_key = ssh_public_key
        self.ssh_keys_dir = "<<Login " + login + " private Key path>>"
        self._verify_and_create_public_key()

    def _verify_and_create_public_key(self):
        """ Checking provided public key valid or not, if not create it"""
        if self.ssh_public_key.startswith('--'):
            logger.info("SSH public key in input YAML for {login} is invalid , creating new ones".
                        format(login=self.login))
            self.ssh_keys_dir = GLOBAL_SSH_KEY_DIR + "/" + self.login
            self.ssh_public_key = SSHKeys.gen_ssh_public_key(self.login, self.ssh_keys_dir )
        else:
            logger.info("Provided SSH public is valid for " + self.login)