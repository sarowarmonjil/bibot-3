# http://container-solutions.com/6-dockerfile-tips-official-images/
FROM ubuntu:16.04
MAINTAINER 'donger' 272045117@qq.com
WORKDIR /app

# install deps
# 阿里源[无奈脸]
COPY conf/sources.list /etc/apt/sources.list
RUN deps='ca-certificates python cron'; buildDeps='python-pip wget vim ipython'; \
    set -x \
    && apt-get update && apt-get install -y $deps $buildDeps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# pip install -r requirements.txt
# 豆瓣源
COPY conf/pip.conf /root/.pip/pip.conf
COPY requirements.txt .
RUN set -x \
    && pip install setuptools \
    && pip install -r requirements.txt

COPY . .

RUN crontab conf/crontab

RUN chmod u+x ./run.sh ./src/*
CMD ["./run.sh"]
