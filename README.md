# LaunchEC2Instances
Launch EC2 Instances with specified configuration in YAML
- *Create EC2 instances*
- *Create required EBS volumes and mount them*
- *Create OS users*
- *Able to do SSH to EC2 instances by enabling Security group for igress port 22 ie ssh_group* 
___
#### Pre-Requirements:

- Python 3.8
- pip3 
- git 

#### Installation and Launch EC2 instances:

```
$ git clone git@github.com:baipaneni/LaunchEC2Instances.git
$ cd LaunchEC2Instances
$ pip3 install pipenv
$ pipenv install 
## Please replace <<aws_access_key_id>> and <<aws_secret_access_key>>  with your own AWS aws_access_key_id and aws_secret_access_key
$ python ec2_launch.py --aws_access_key_id <<aws_access_key_id>> --aws_secret_access_key <<aws_secret_access_key>>
```
#### Once the EC2 instances are up
```
NOTE: Normally Launch EC2 instances takes 1-2 minutes before EC2 instances for use


```




