from aws_cdk import (
    Stack,
    Duration
)

from aws_cdk.aws_lambda import (
    DockerImageFunction,
    DockerImageCode
)

from constructs import Construct


class AwsLambdaThumbnailizerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda
        self.convert = DockerImageFunction(
            code=DockerImageCode.from_image_asset(
                directory='lambdas/thumbnailizer',),
            id='thumbnailizer-lambda',
            function_name='thumbnailizer-lambda',
            memory_size=1024,
            scope=self,
            timeout=Duration.seconds(300),
        )
