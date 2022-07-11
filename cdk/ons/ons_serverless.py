import os
import subprocess
import shutil

from aws_cdk import (
    BundlingOptions,
    Stack,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_lambda_python_alpha as pylambda,
    aws_lambda as _lambda
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
        self.create_sources()

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda_python_alpha/PythonFunction.html
        pylambda.PythonFunction(
            self,
            "ONS_Start",
            filesystem=_lambda.FileSystem.from_efs_access_point(access_point, '/mnt/ons'),
            vpc=vpc,
            runtime=_lambda.Runtime.PYTHON_3_7,  # required
            entry=".build/src/",
            index="open_needs_server/aws.py",
            handler="handler",
            layers=[
                self.create_dependencies_layer(self.stack_name, entrypoint_name)
            ]
        )

    def clean_build_folder(self):
        print('Cleaning .build')
        shutil.rmtree('.build', ignore_errors=True)

    def create_sources(self) -> str:
        print('Copying sources')
        source_path = 'open_needs_server'
        config_path = 'settings.toml'

        target_folder = 'open_needs_server'
        target_path = '.build/src/'

        target_final = f'{target_path}/{target_folder}'
        shutil.copytree(source_path, target_final, dirs_exist_ok=True)
        print(f'  {target_path}')

        print('Copying config')
        shutil.copy(config_path, target_path)

        return target_path

    def create_dependencies_layer(self, project_name, function_name: str) -> pylambda.PythonLayerVersion:
        """
        https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/LayerVersion.html

        :param project_name:
        :param function_name:
        :return:
        """
        print('Copying dependencies')
        requirements_files = [
            'requirements/server.txt',
            'requirements/aws.txt'
        ]
        output_dir = f'.build/deps/'
        output_req = f'.build/deps/requirements.txt'
        os.makedirs(output_dir, exist_ok=True)

        # if not os.environ.get('SKIP_PIP'):
        #     subprocess.check_call(
        #         f'pip install -r {" -r".join(requirements_files)} -t {output_dir}/python'.split()
        #     )

        with open(output_req, 'w') as req_output:
            for req_file in requirements_files:
                with open(req_file) as req_input:
                    req_output.write(req_input.read())
                    req_output.write('\n')

        layer_id = f'{project_name}-{function_name}-dependencies'
        # layer_code = lambda_.Code.from_asset(output_dir)

        # Uses docker to build deps
        layer = pylambda.PythonLayerVersion(self, layer_id,
                                            entry=output_dir)

        print(f' {output_dir}')
        return layer
