import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("vpc-python",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={"Name": "pvc-python"})

# Create a subnet
subnet = aws.ec2.Subnet("subnet-python",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
    tags={"Name": "subnet-python"})

# Create an internet gateway
igw = aws.ec2.InternetGateway("my-igw",
    vpc_id=vpc.id,
    tags={"Name": "my-igw"})

# Create a route table
route_table = aws.ec2.RouteTable("my-route-table",
    vpc_id=vpc.id,
    routes=[aws.ec2.RouteTableRouteArgs(
        cidr_block="0.0.0.0/0",
        gateway_id=igw.id,
    )],
    tags={"Name": "my-route-table"})

# Associate route table with subnet
route_table_assoc = aws.ec2.RouteTableAssociation("my-route-table-assoc",
    subnet_id=subnet.id,
    route_table_id=route_table.id)

# Create a security group
security_group = aws.ec2.SecurityGroup("my-sg",
    vpc_id=vpc.id,
    description="Allow SSH and HTTP",
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        )
    ],
    tags={"Name": "my-sg"})

# Create an EC2 instance
ec2_instance = aws.ec2.Instance("instance-python",
    instance_type="t2.micro",
    vpc_security_group_ids=[security_group.id],
    subnet_id=subnet.id,
    ami="ami-070b7c2988d4e2c89",  # Amazon Linux 2 AMI
    tags={"Name": "my-instance"})

# Create an S3 bucket
bucket = aws.s3.Bucket("my-bucket")

# Export the IDs of the created resources
pulumi.export("instance_id", ec2_instance.id)
pulumi.export("bucket_name", bucket.id)
pulumi.export("vpc_id", vpc.id)