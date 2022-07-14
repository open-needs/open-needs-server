"""
Provides a special AWS lambda handler to start the Open-Needs server.

Ideas from https://www.deadbear.io/simple-serverless-fastapi-with-aws-lambda/
"""
from mangum import Mangum

from open_needs_server.main import ons_app


handler = Mangum(ons_app)
