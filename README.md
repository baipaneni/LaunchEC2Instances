# LaunchEC2Instances
Launch EC2 Instances with specified configuration in YAML
- *Create EC2 instances*
- *Create required EBS volumes and mount them*
- *Create OS users*
- *Able to do SSH to EC2 instances by enabling Security group for igress port 22 ie ssh_group* 
___
#### Pre-Requisites:

- Python 3.8
- pip3 
- git 
- Valid AWS credentials aws_access_key_id and aws_secret_access_key which have IAM admin access.

#### Installation and Launch EC2 instances:

```
$ git clone git@github.com:baipaneni/LaunchEC2Instances.git
$ cd LaunchEC2Instances
$ sudo pip3 install pipenv
$ pipenv install

# To Run ec2_launch.py command, Please replace <<aws_access_key_id>> and <<aws_secret_access_key>> 
# with your own AWS aws_access_key_id and aws_secret_access_key
$ pipenv run python ec2_launch.py --aws_access_key_id <<aws_access_key_id>> --aws_secret_access_key <<aws_secret_access_key>>

```
#### Once the EC2 instances are up
*NOTE: Normally Launch EC2 instances takes 1-2 minutes before EC2 instances for use*

- At the end of ec2_launch.py Example output

```

 ssh -oStrictHostKeyChecking=no -l user1 -i /tmp/aws_ssh_keys/user1/id_rsa  18.132.48.229
 ssh -oStrictHostKeyChecking=no -l user2 -i /tmp/aws_ssh_keys/user2/id_rsa  18.132.48.229

```
- Run SSH commands which you received from terminal .
- Both users has sudo permissions.


#### Help for ec2_launch.py

```
$ python ec2_launch.py -h
usage: ec2_launch.py [-h] [--config_file CONFIG_FILE] [--aws_region AWS_REGION] --aws_access_key_id AWS_ACCESS_KEY_ID --aws_secret_access_key AWS_SECRET_ACCESS_KEY

AWS EC2 Launch

optional arguments:
  -h, --help            show this help message and exit
  --config_file CONFIG_FILE
                        YAML config_file
  --aws_region AWS_REGION
                        aws region to use
  --aws_access_key_id AWS_ACCESS_KEY_ID
                        use aws access_key_id
  --aws_secret_access_key AWS_SECRET_ACCESS_KEY
                        use aws_secret_access_key for key
```

