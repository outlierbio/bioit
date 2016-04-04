FROM centos:7.0.1406
MAINTAINER Jake Feala <jake@outlierbio.com>

# Yum and pip packages
RUN yum update -y && yum install -y bzip2 gcc gcc-c++ make tar wget
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && \
    python get-pip.py 
RUN pip install --upgrade pip && pip install awscli boto3 click ipython

# Add shared utilities
ADD . /bio-it/
RUN cd /bio-it && pip install .

# Add minimal credentials for application user
ADD ./secrets/aws/* /root/.aws/
ENV AWS_PROFILE bioit

