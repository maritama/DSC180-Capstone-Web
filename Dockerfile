FROM maven:3-jdk-11 as maven_builder

WORKDIR /app
ADD web-development .
RUN ["/usr/local/bin/mvn-entrypoint.sh", "mvn", "clean", "package"]


FROM tomcat:9-jdk11

COPY --from=maven_builder /app/target/python.war $CATALINA_HOME/webapps/

RUN apt-get update -y
RUN apt-get install -y htop gcc ant
# RUN apt-get install g++ -y
# RUN DEBIAN_FRONTEND='noninteractive' apt-get install openjdk-8-jdk -y
# RUN DEBIAN_FRONTEND='noninteractive' apt-get install curl -y
# RUN DEBIAN_FRONTEND='noninteractive' apt-get install cmake -y 


RUN wget -q \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

ENV PATH /opt/conda/bin:$PATH

RUN conda install pandas matplotlib seaborn scikit-learn

WORKDIR /app
ADD phrase-mining /app/phrase-mining

RUN cd /app/phrase-mining && \
    rm -rf AutoPhrase && \
    git clone https://github.com/shangjingbo1226/AutoPhrase.git && \
    cd AutoPhrase %% \
    git checkout 36312ae
