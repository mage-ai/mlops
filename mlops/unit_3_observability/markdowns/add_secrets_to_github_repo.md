## Add secrets to GitHub repository

Follow [this guide](https://docs.mage.ai/production/ci-cd/local-cloud/github-actions#github-actions-setup) 
to add the newly created access key and secret to your GitHub project.

Get the access key and secret by running on your host machine (e.g. local computer):

```sh
cat ~/.aws/credentials
```

You should see something like this:

```bash
[MageDeployer]
aws_access_key_id = XXXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
[MageContinuousIntegrationDeployer]
aws_access_key_id = XXXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```