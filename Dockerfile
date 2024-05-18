FROM mageai/mageai:alpha

ARG PROJECT_NAME=mlops
ARG MAGE_CODE_PATH=/home/mage_code
ARG USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

WORKDIR ${MAGE_CODE_PATH}

# Replace [project_name] with the name of your project (e.g. demo_project)
COPY ${PROJECT_NAME} ${PROJECT_NAME}

# Set the USER_CODE_PATH variable to the path of user project.
# The project path needs to contain project name.
# Replace [project_name] with the name of your project (e.g. demo_project)
ENV USER_CODE_PATH=${USER_CODE_PATH}

# RUN apt-get update && apt-get install graphviz

# Install custom Python libraries
RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}/${PROJECT_NAME}"

# Installing necessary utilities and Terraform
RUN apt-get update && \
  apt-get install -y wget unzip && \
  wget https://releases.hashicorp.com/terraform/1.8.3/terraform_1.8.3_linux_amd64.zip && \
  unzip terraform_1.8.3_linux_amd64.zip -d /usr/local/bin/ && \
  rm terraform_1.8.3_linux_amd64.zip

CMD ["/bin/sh", "-c", "/app/run_app.sh"]
