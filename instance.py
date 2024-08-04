import pulumi_aws as aws
from vpc import ami_actual
from vpc import security_group
from vpc import subnet_2

# Create an EC2 instance
ec2_instance = aws.ec2.Instance("python-python",
                                instance_type="t2.micro",
                                vpc_security_group_ids=[security_group.id],
                                subnet_id=subnet_2.id,
                                ami=ami_actual.id,  # Amazon Linux 2 AMI
                                private_ip="10.0.2.55",
                                tags={"Name": "instance-python"})

# Create an S3 bucket
bucket = aws.s3.Bucket("bucket-python")