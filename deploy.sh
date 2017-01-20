#!/bin/bash
if ! [ -x "$(command -v jq)" ]; then
    echo "jq is not installed"
    exit 1
fi
if [[ $# -lt 1 ]]; then
    echo "Please supply a valid IAM role with EC2 access"
    exit 1
fi
zip autosnap.zip autosnap.py
aws lambda create-function --function-name autosnap --runtime "python2.7" --role "${1}" --handler lambda_handler --description "EBS autosnap" --timeout 10 --zip-file fileb://autosnap.zip
aws events put-rule --name autosnap-cron --schedule-expression "cron(0 0 * * ? *)" --state ENABLED --description "Autosnap Lambda"
ARN=$(aws lambda list-functions --query 'Functions[?FunctionName==`autosnap`]' | jq -r .[0].FunctionArn)
aws events put-targets --rule autosnap-cron --targets "Id=autosnap,Arn=${ARN}"
