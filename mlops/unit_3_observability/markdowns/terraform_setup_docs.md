## Terraform setup

> If you cloned Mage’s [MLOps repository](https://github.com/mage-ai/mlops), 
> skip this section and go to the **Customize Terraform configurations** section.


Install and setup Terraform on your local machine.
Follow the guide here or the detailed guide in the 
[Mage arcane library aka developer documentation](https://docs.mage.ai/production/deploying-to-cloud/using-terraform).

<br />

---

<br />


### Customize Terraform configurations

Open the file `mage-ops/mlops/terraform/aws/variables.tf` and update the following variables:

```hcl
variable "docker_image" {
  description = "Docker image url used in ECS task."
  default     = "mageai/mageai:alpha"
}

variable "app_name" {
  type        = string
  description = "Application Name"
  default     = "mlops"
}

variable "aws_region" {
  type        = string
  description = "AWS Region"
  default     = "us-west-2"
}

variable "availability_zones" {
  description = "List of availability zones"
  default     = ["us-west-2a", "us-west-2b"]
}
```

Open the file `mage-ops/mlops/terraform/aws/env_vars.json` and update 1 variable
if your project name isn’t `mlops`:

```json
[
  {
    "name": "MAGE_PRESENTERS_DIRECTORY",
    "value": "[change to your project name]/presenters"
  }
]
```

<br />

---

<br />

#### Run the following commands to deploy the application to AWS:

Run the command after changing directories into: `mage-ops/mlops/terraform/aws`

```bash
terraform init
terraform apply
```

Here are detailed instructions on how to
[deploy Mage to AWS using Terraform](https://docs.mage.ai/production/deploying-to-cloud/aws/setup).