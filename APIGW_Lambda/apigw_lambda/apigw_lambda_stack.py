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
            "LambdaBackend",
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(
                path=os.path.join(__file__, ""),
                bundling=BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_11.bundlingImage,
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t  /asset-output && rsync -au . /asset-output",
                    ],
                ),
            ),
        )
