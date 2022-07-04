from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_lambda as lambda_
)
from constructs import Construct


class OnsServerless(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, 'ONS-VPC')
        filesystem = efs.FileSystem(self, 'ONS-Efs', vpc=vpc)

        access_point = filesystem.add_access_point(
            'AccessPoint',
            path='/export/lambda',
            create_acl={
                'owner_uid': '1001',
                'owner_gid': '1001',
                'permissions': '750'
            },
            posix_user={
                'uid': '1001',
                'gid': '1001'
            })

        lambda_.Function(
            self,
            "ONS_Start",
            filesystem=lambda_.FileSystem.from_efs_access_point(access_point, '/mnt/ons'),
            vpc=vpc,
            runtime=lambda_.Runtime.PYTHON_3_8,  # required
            code=lambda_.Code.from_asset('open_needs_server'),
            handler="my_exported_func"
        )
