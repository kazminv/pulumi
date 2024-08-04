import pulumi_aws as aws

# Fetch the latest Amazon Linux 2 AMI
ami_actual = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["amzn2-ami-hvm-*-x86_64-gp2"]
        ),
        aws.ec2.GetAmiFilterArgs(
            name="architecture",
            values=["x86_64"]
        ),
        aws.ec2.GetAmiFilterArgs(
            name="root-device-type",
            values=["ebs"]
        )
    ]
)


# Create a VPC
vpc = aws.ec2.Vpc("vpc-python",
                  cidr_block="10.0.0.0/16",
                  enable_dns_support=True,
                  enable_dns_hostnames=True,
                  tags={"Name": "pvc-python"})

# Create a subnet
subnet_1 = aws.ec2.Subnet("subnet-python-1",
                          vpc_id=vpc.id,
                          cidr_block="10.0.1.0/24",
                          map_public_ip_on_launch=True,
                          tags={"Name": "subnet-python-1"})

# Create a subnet
subnet_2 = aws.ec2.Subnet("subnet-python-2",
                          vpc_id=vpc.id,
                          cidr_block="10.0.2.0/24",
                          map_public_ip_on_launch=True,
                          tags={"Name": "subnet-python-2"})

# Create an internet gateway
igw = aws.ec2.InternetGateway("my-igw",
                              vpc_id=vpc.id,
                              tags={"Name": "igw-python"})

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
                                                  subnet_id=subnet_2.id,
                                                  route_table_id=route_table.id)

# Create a security group
security_group = aws.ec2.SecurityGroup("python-sg",
                                       vpc_id=vpc.id,
                                       description="Allow SSH, HTTPS and HTTP",
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
                                           aws.ec2.SecurityGroupIngressArgs( #ping
                                               protocol="tcp",
                                               from_port=25,
                                               to_port=25,
                                               cidr_blocks=["0.0.0.0/0"],
                                           ),
                                           aws.ec2.SecurityGroupIngressArgs(  # https
                                               protocol="tcp",
                                               from_port=443,
                                               to_port=443,
                                               cidr_blocks=["0.0.0.0/0"]
                                           ),
                                           aws.ec2.SecurityGroupIngressArgs(
                                               protocol="icmp",
                                               from_port=-1,  # from_port and to_port are ignored for ICMP
                                               to_port=-1,  # -1 allows all ICMP types and codes
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
                                       tags={"Name": "sg-python"})