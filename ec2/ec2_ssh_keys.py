import logging
import os
from log import get_logger

logger = get_logger(__name__)


class SSHKeys:

    @staticmethod
    def create_ssh_keys(ssh_key_dir: str, user: str) -> None:
        """ Create SSH keys for users"""
        logger.info("creating ssh keys for {user}".format(user=user))
        cmd = "rm -rf {ssh_key_dir} \
            && mkdir -p {ssh_key_dir} \
            && ssh-keygen -t rsa  -q -N '' -C {user}@localhost -f {ssh_key_dir}/id_rsa" \
            .format(user=user, ssh_key_dir=ssh_key_dir)
        os.system(cmd)
        logger.info("created ssh keys for {user} in directory {ssh_key_dir}".
                    format(user=user, ssh_key_dir=ssh_key_dir))

    @staticmethod
    def gen_ssh_public_key(user: str, ssh_key_dir):
        """
        Generate SSH keys if not exists
        """
        ssh_public_key_file = ssh_key_dir + "/id_rsa.pub"

        if not os.path.exists(ssh_public_key_file):
            SSHKeys.create_ssh_keys(ssh_key_dir, user)
        else:
            logger.info("Using exiting keys for {user} in {ssh_public_key_file} ".
                        format(user=user,
                               ssh_public_key_file=ssh_public_key_file))

        with open(ssh_public_key_file, 'r') as file:
            ssh_public_key = file.read()

        return ssh_public_key
