#!/usr/bin/env python3
import os

from aws_cdk import App, Environment

from iac.aws_lambda_thumbnailizer_stack import AwsLambdaThumbnailizerStack


app = App()
AwsLambdaThumbnailizerStack(app,
                            "AwsLambdaThumbnailizerStack",
                            env=Environment(
                                account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                region=os.getenv('CDK_DEFAULT_REGION')
                            ),
                            )

app.synth()
