# aws-autosnap
Creates automatic EBS snapshots with Lambda and CloudWatch events. Uses
volume tags to choose what to snapshot. Will automatically clean up old
snapshots with a configureable window.

## Quick start
There are two ways to install this lambda, manually or with the supplied
script. Both ways require you to first configure a Lambda IAM role that has access to
create EC2 snapshots.

For automatic mode you must have a working copy of both the awscli
(with permission to install Lambdas and CloudWatch events) and jq. Copy your
lambda role arn string then execute:
```
$ ./deploy.sh "arn:aws:iam::1234567890:role/SOMEROLE"
```
You're done!

To manually install, create a new Lambda function configured for Python and install
the `autosnap.py` script.  Next add a trigger that is based on a CloudWatch event.
Works best as a daily cron like `cron(0 0 * * ? *)`. See deploy.sh for hints.

## How to use and configure
The script will look for any EBS volumes with a tag name of `autosnap`. Once found
it will auto create a snapshot with a `-autosnap` suffix. It will then look for
snapshots with that suffix and delete any that are older than 3 days by default.
You can change how long it saves snapshots by setting the `RETENTION` environment
variable in your Lambda function (or go crazy and edit the script).

