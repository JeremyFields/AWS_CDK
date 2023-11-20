from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    BundlingOptions,
)
from constructs import Construct
import os


class ApigwLambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        backend = _lambda.Function(
            self,
            "lambda_backend",
            handler="index.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset(
                path="lambda",
                bundling=BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_11.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t  /asset-output && rsync -r . /asset-output",
                    ],
                ),
            ),
        )

        api = apigw.RestApi(self, "rest_api")