# it's official and small so i'm using it
FROM python:3.9.0b5-alpine3.11

# first we need to copy everything
COPY . /drone-kubernetes-apply

# now we install all the python packages
RUN pip install -r /drone-kubernetes-apply/requirements.txt

# install kubectl, based on which DRONE_STAGE_ARCH is used with amd64 being the default if not otherwise stated as it's the most common one, can't use ADD as the internal logic also figures out the latest version of kubectl to use
ARG DRONE_STAGE_ARCH=amd64
RUN apk add --no-cache curl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/${DRONE_STAGE_ARCH}/kubectl
RUN mv ./kubectl /bin/kubectl
RUN chmod +x /bin/kubectl

# set the workdir to be the folder where all the data is so relative file names will work as expected
WORKDIR /drone-kubernetes-apply

# run the script that does the actual work when the container starts
CMD ["sh", "/drone-kubernetes-apply/drone_kubernetes_runner.sh"]
