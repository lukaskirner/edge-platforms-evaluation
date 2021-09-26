FROM ubuntu:20.04

RUN mkdir -p /home/data
WORKDIR /home

RUN apt-get update && \
    apt-get install -y git \
        curl \
        gnupg2 \
        zlib1g-dev \
        libjpeg-dev \
        libpng-dev

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -y libedgetpu1-std \
        python3-pycoral \
        python3-pip

RUN curl -L -o ./data/labels.txt https://github.com/google-coral/test_data/raw/master/inat_bird_labels.txt \
    && curl -L -o ./data/model.tflite https://github.com/google-coral/test_data/raw/master/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite 

COPY . .
RUN pip install -r requirements.txt


ENTRYPOINT [ "python3", "./detector.py" ]