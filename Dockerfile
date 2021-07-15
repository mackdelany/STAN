FROM python:3.8

RUN mkdir -p /stan

WORKDIR /stan

COPY . /stan

RUN chmod +x ./shell/redisinstall.sh && \
    chmod +x ./shell/celeryrun.sh && \
    chmod +x ./shell/integration_tests.sh && \
    chmod +x ./shell/launchprodapp.sh && \
    chmod +x ./shell/launchprodcompose.sh && \
    chmod +x ./shell/api_test.sh

RUN addgroup stan && \
    adduser --disabled-password --gecos "" --ingroup stan stan && \
    chown stan:stan -R /stan/

USER stan

ENV PATH="/home/stan/.local/bin:${PATH}"

RUN pip install --user --no-cache-dir  -r requirements.txt 

RUN ./shell/redisinstall.sh

EXPOSE 80
