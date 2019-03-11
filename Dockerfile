FROM python:3-slim

USER root

RUN apt-get update \
    && apt-get -y install tesseract-ocr tesseract-ocr-chi-sim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir stagesep2==0.1.4 \
    && mkdir /root/stagesep2

WORKDIR /root/stagesep2
CMD ["bash"]
