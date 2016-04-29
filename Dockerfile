FROM debian:8
MAINTAINER Tong Da <tongda@outlook.com>

RUN apt-get update && apt-get install -y  \
    autoconf \
    automake \
    bzip2 \
    g++ \
    git \
    libatlas3-base \
    libtool-bin \
    make \
    python2.7 \
    python-pip \
    python-yaml \
    python-simplejson \
    python-gi \
    subversion \
    wget \
    zlib1g-dev && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    pip install ws4py==0.3.2 && \
    pip install tornado && \    
    ln -s /usr/bin/python2.7 /usr/bin/python ; ln -s -f bash /bin/sh

#RUN cd /opt && wget http://www.digip.org/jansson/releases/jansson-2.7.tar.bz2 && \
#    bunzip2 -c jansson-2.7.tar.bz2 | tar xf -  && \
#    cd jansson-2.7 && \
#    ./configure && make && make check &&  make install && \
#    echo "/usr/local/lib" >> /etc/ld.so.conf.d/jansson.conf && ldconfig && \
#    rm /opt/jansson-2.7.tar.bz2 && rm -rf /opt/jansson-2.7

RUN cd /opt && \
    git clone https://github.com/ThoughtWorksInc/kaldi && \
    cd /opt/kaldi/tools && \
    make && \
    ./install_portaudio.sh && \
    cd /opt/kaldi/src && ./configure --shared && \
    sed -i '/-g # -O0 -DKALDI_PARANOID/c\-O3 -DNDEBUG' kaldi.mk && \
    make depend && make && \
    cd /opt/kaldi/src/online && make depend && make && \
#    cd /opt/kaldi/src/gst-plugin && make depend && make && \
    cd /opt && \
#    git clone https://github.com/alumae/gst-kaldi-nnet2-online.git && \
#    cd /opt/gst-kaldi-nnet2-online/src && \
#    sed -i '/KALDI_ROOT?=\/home\/tanel\/tools\/kaldi-trunk/c\KALDI_ROOT?=\/opt\/kaldi' Makefile && \
#    make depend && make && \
#    rm -rf /opt/gst-kaldi-nnet2-online/.git/ && \
#    find /opt/gst-kaldi-nnet2-online/src/ -type f -not -name '*.so' -delete && \
#    rm -rf /opt/kaldi/.git && \
#    rm -rf /opt/kaldi/egs/ /opt/kaldi/windows/ /opt/kaldi/misc/ && \
    rm -rf /opt/kaldi/windows/ /opt/kaldi/misc/
#    find /opt/kaldi/src/ -type f -not -name '*.so' -delete && \
#    find /opt/kaldi/tools/ -type f \( -not -name '*.so' -and -not -name '*.so*' \) -delete && \
#    cd /opt && git clone https://github.com/alumae/kaldi-gstreamer-server.git && \
#    rm -rf /opt/kaldi-gstreamer-server/.git/ && \
#    rm -rf /opt/kaldi-gstreamer-server/test/

RUN apt-get install -y \
    python3.4 \
    python3-pip \
    nginx && \
    pip3 install tornado && \
    rm -f /etc/nginx/sites-available/default

ENV KALDI_SCRIPT_DIR=/opt/kaldi/egs/twasr-thchs30/s5

COPY asr asr-demo/asr/
COPY main.py asr-demo/
COPY conf/nginx/test-asr.conf /etc/nginx/conf.d/
COPY conf/*.pem /etc/nginx/certs/
COPY index.html /usr/share/nginx/asr-demo/
COPY model/final.mdl /opt/kaldi/egs/twasr-thchs30/s5/exp/mono/
COPY model/HCLG.fst /opt/kaldi/egs/twasr-thchs30/s5/exp/mono/graph/
COPY model/words.txt /opt/kaldi/egs/twasr-thchs30/s5/exp/mono/graph/

EXPOSE 8080 8443

CMD nginx && python3.4 asr-demo/main.py
