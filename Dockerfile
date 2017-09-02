# http://container-solutions.com/6-dockerfile-tips-official-images/
FROM ubuntu:16.04
MAINTAINER 'donger' 272045117@qq.com
WORKDIR /app

# install deps
# 阿里源[无奈脸]
COPY conf/sources.list /etc/apt/sources.list
RUN deps='ca-certificates python cron supervisor'; buildDeps='python-pip wget vim ipython'; \
    set -x \
    && apt-get update && apt-get install -y $deps $buildDeps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 豆瓣源
COPY conf/pip.conf /root/.pip/pip.conf
RUN set -x \
    && pip install setuptools \
    && pip install -U pip

# 安装TA-Lib
RUN buildDeps='python-dev gcc make'; \
    set -x \
    && apt-get update && apt-get install -y $buildDeps --no-install-recommends \
    && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O ta-lib.tar.gz \
    && tar -zxf ta-lib.tar.gz \
    && cd ta-lib \
    && ./configure --prefix=/usr \
    && make && make install \
    && cd .. \
    && pip install numpy TA-Lib \
    && rm -rf ta-lib.tar.gz ta-lib/ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove $buildDeps

# pip install -r requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN crontab conf/crontab
RUN ln -s /app/conf/supervisor.conf /etc/supervisor/conf.d/supervisor.conf

RUN chmod u+x ./run.sh ./src/*
CMD ["./run.sh"]
