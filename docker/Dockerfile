FROM ubuntu:24.04

RUN apt-get update && apt-get install -y apt-transport-https wget gpg git make python3 clang default-jdk

ADD https://storage.googleapis.com/dart-archive/channels/stable/release/2.19.6/linux_packages/dart_2.19.6-1_amd64.deb /
RUN dpkg -i /dart_2.19.6-1_amd64.deb

RUN useradd -m -s /bin/bash tester
USER tester
WORKDIR /home/tester

RUN git clone https://github.com/munificent/craftinginterpreters.git

WORKDIR /home/tester/craftinginterpreters

RUN make get && make
