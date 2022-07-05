import os
import subprocess
import shutil

from aws_cdk import (
    BundlingOptions,
    Stack,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_lambda as lambda_
)
from constructs import Construct


class OnsServerless(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.clean_build_folder()

        vpc = ec2.Vpc(self, 'ONS-VPC', nat_gateways=0)
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

        entrypoint_name = 'ons_layer'

        lambda_.Function(
            self,
            "ONS_Start",
            filesystem=lambda_.FileSystem.from_efs_access_point(access_point, '/mnt/ons'),
            vpc=vpc,
            runtime=lambda_.Runtime.PYTHON_3_9,  # required
            code=lambda_.Code.from_asset(self.create_sources()),
            handler="open_needs_server.aws.handler",
            layers=[
                self.create_dependencies_layer(self.stack_name, entrypoint_name)
            ]
        )

    def clean_build_folder(self):
        print('Cleaning .build')
        shutil.rmtree('.build')

    def create_sources(self):
        print('Copying sources')
        source_path = 'open_needs_server'
        target_folder = 'open_needs_server'
        target_path = '.build/src/'

        target_final = f'{target_path}/{target_folder}'
        shutil.copytree(source_path, target_final, dirs_exist_ok=True)
        print(f'  {target_path}')
        return target_path

    def create_dependencies_layer(self, project_name, function_name: str) -> lambda_.LayerVersion:
        print('Copying dependencies')
        requirements_files = [
            'requirements/server.txt',
            'requirements/aws.txt'
        ]
        output_dir = f'.build/deps'

        if not os.environ.get('SKIP_PIP'):
            subprocess.check_call(
                f'pip install -r {" -r".join(requirements_files)} -t {output_dir}/python'.split()
            )

        layer_id = f'{project_name}-{function_name}-dependencies'
        layer_code = lambda_.Code.from_asset(output_dir)

        print(f' {output_dir}')
        return lambda_.LayerVersion(self, layer_id, code=layer_code)
