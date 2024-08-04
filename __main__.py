import pulumi
from instance import ec2_instance
from instance import bucket
from vpc import vpc
from vpc import ami_actual

# Export the IDs of the created resources
pulumi.export("instance_id", ec2_instance.id)
pulumi.export("bucket_name", bucket.id)
pulumi.export("vpc_id", vpc.id)
pulumi.export("private_ip", ec2_instance.private_ip)
pulumi.export("public_ip", ec2_instance.public_ip)
pulumi.export("ami_id", ami_actual.id)
