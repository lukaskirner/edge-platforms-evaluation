FROM ubuntu:20.04

RUN mkdir -p /home/coral
WORKDIR /home/coral

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
        python3-pycoral

RUN git clone https://github.com/google-coral/pycoral.git \
    && cd pycoral \
    && bash examples/install_requirements.sh classify_image.py

WORKDIR /home/coral/pycoral
ENTRYPOINT python3 ./examples/classify_image.py \
--model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
--labels test_data/inat_bird_labels.txt \
--input test_data/parrot.jpg