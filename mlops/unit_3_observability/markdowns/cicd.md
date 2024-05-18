## Continuous Integration and Continuous Deployment (CI/CD)

This allows developers to automate the process of testing and deploying code.
In this section, we will create a CI/CD pipeline that will build and
deploy our application to AWS Elastic Container Service (ECS).

<br />

---

<br />

### GitHub Actions YAML configurations

If you deployed Mage using the Terraform templates provided by Mage,
a GitHub Action workflow YAML file will already be created. 
Skip this section and go to the **Create IAM policy** section to continue.

If you don’t have the GitHub Actions workflow YAML,
follow this [detailed guide](https://docs.mage.ai/production/ci-cd/local-cloud/github-actions)
to create a CI/CD pipeline for your application.

> Note: After running `terraform apply`, a GitHub Actions workflow YAML file should be created
> in the `mage-ops/.github/workflows` directory.
> This file will contain the CI/CD pipeline configuration.

Enter the following environment variables in the GitHub Actions YAML file that match your
infrastructure:

```yaml
env:
  AWS_REGION: us-west-2
  ECR_REPOSITORY: ...
  ECS_CLUSTER: ...
  ECS_SERVICE: ...
  ECS_TASK_DEFINITION: ...
  CONTAINER_NAME: ...
```

<br />

---

<br />

### Create IAM policy

1. Policy name: **ContinuousIntegrationContinuousDeployment**

1. Permissions using the JSON editor:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:CompleteLayerUpload",
        "ecr:GetAuthorizationToken",
        "ecr:InitiateLayerUpload",
        "ecr:PutImage",
        "ecr:UploadLayerPart",
        "ecs:DeregisterTaskDefinition",
        "ecs:DescribeClusters",
        "ecs:DescribeServices",
        "ecs:DescribeTaskDefinition",
        "ecs:RegisterTaskDefinition",
        "ecs:UpdateService",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

<br />

---

<br />

### Create IAM user

1. User name: **MageContinuousIntegrationDeployer**

1. Attach policies directly:
   - **ContinuousIntegrationContinuousDeployment**

1. After creating the user, create an access key and secret key.

1. Use case: **Third-party service**
