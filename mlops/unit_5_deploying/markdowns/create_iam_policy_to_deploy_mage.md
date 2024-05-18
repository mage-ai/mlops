## Setup AWS permissions for deploying

Run the next block to set all of this up automtically.

### Create IAM policy to deploy Mage

1. Add these
   [permissions](https://docs.mage.ai/production/deploying-to-cloud/aws/terraform-apply-policy)
   using the JSON editor.

1. Policy name: **TerraformApplyDeployMage**

> In order to perform the above action, you need the following permissions:

```json
iam:CreatePolicy
```

```sh
aws iam create-policy --policy-name TerraformApplyDeployMage --policy-document \
  "$(curl -s https://raw.githubusercontent.com/mage-ai/mage-ai-terraform-templates/master/aws/policies/TerraformApplyDeployMage.json)"
```

<br />

---

<br />

### Create AWS policies to delete resources

1. Add these
   [permissions](https://docs.mage.ai/production/deploying-to-cloud/aws/terraform-destroy-policy)
   using the JSON editor.

1. Policy name: **TerraformDestroyDeleteResources**

> In order to perform the above action, you need the following permissions:

```json
iam:CreatePolicy
```

```sh
aws iam create-policy --policy-name TerraformDestroyDeleteResources --policy-document \
  "$(curl -s https://raw.githubusercontent.com/mage-ai/mage-ai-terraform-templates/master/aws/policies/TerraformDestroyDeleteResources.json)"
```

<br />

---

<br />

### Create IAM user

1. User name: **MageDeployer**

1. Attach policies directly:

- **TerraformApplyDeployMage**
- **TerraformDestroyDeleteResources**

1. After creating the user, create an access key and secret key.

1. Use case: **Command Line Interface (CLI)**

##### Create IAM User

**Creating the IAM User (MageDeployer):**

> In order to perform the above action, you need the following permissions:

```json
iam:CreateUser
```

```sh
aws iam create-user --user-name MageDeployer
```

##### Attach Policies to User

> In order to perform the above action, you need the following permissions:

```json
iam:ListPolicies
```

**Attach TerraformApplyDeployMage Policy:**

_First, find the Policy ARN by listing the policies.
\_Then, attach the policy to the user using the ARN obtained:_

```sh
aws iam attach-user-policy \
  --policy-arn $(aws iam list-policies \
  --query "Policies[?PolicyName==\`TerraformApplyDeployMage\`].Arn" \
  --output text) \
  --user-name MageDeployer
```

**Attach TerraformDestroyDeleteResources Policy:**

_Find the Policy ARN. \_Attach the policy to the user:_

```sh
aws iam attach-user-policy \
  --policy-arn $(aws iam list-policies \
  --query "Policies[?PolicyName==\`TerraformDestroyDeleteResources\`].Arn" \
  --output text) \
  --user-name MageDeployer
```

##### Create Access Key for the User

```sh
aws iam create-access-key \
  --user-name MageDeployer \
  --output json | jq -r '"[mage-deployer]\naws_access_key_id = \(.AccessKey.AccessKeyId)\naws_secret_access_key = \(.AccessKey.SecretAccessKey)"' >> ~/.aws/credentials
export AWS_PROFILE="mage-deployer"
```
