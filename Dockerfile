###########################################################
# Dockerfile to build zUMIs container images
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu:18.04

# File Author / Maintainer
MAINTAINER Marta Benegas <mbenegas@biobam.com>

# Install compiler and perl stuff
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --yes \
 build-essential \
 gcc-multilib \
 apt-utils \
 python \
 wget \
 libncurses5-dev \
 libncursesw5-dev \
 libbz2-dev \
 liblzma-dev \
 zlib1g-dev \
 nano
 
# Install git
RUN apt-get install -y git

# Install java
RUN apt install -y default-jre default-jdk

#Install dependencies

RUN apt-get install --yes \
 gfortran \
 libhdf5-serial-dev \
 libcurl4-openssl-dev \
 libssl-dev \
 libxml2-dev \
 texlive-latex-extra \
 libcairo2-dev

##install R
ENV R_VERSION=R-3.6.0
WORKDIR /usr/local
RUN wget https://cran.r-project.org/src/base/R-3/$R_VERSION.tar.gz && \
        tar xvf $R_VERSION.tar.gz && \
        rm $R_VERSION.tar.gz && \
        cd $R_VERSION && \
	./configure --with-readline=no --with-x=no && make && make install
ENV PATH /usr/local/R-3.6.0/bin:$PATH

#basic R functionalities
RUN apt install -y r-cran-rgl \
 r-cran-rjags \
 r-cran-snow \
 r-cran-ggplot2 \
 r-cran-igraph \
 r-cran-lme4 \
 r-cran-rjava \
 r-cran-devtools \ 
 r-cran-rjava 

#R zUMIs dependencies
RUN Rscript -e 'cran_pcks <- c("inflection","yaml","shiny","shinythemes","shinyBS","ggplot2","mclust","dplyr","cowplot","Matrix","BiocManager","devtools","stringdist","data.table", "pbapply")' \
		-e 'install.packages(cran_pcks, repos="https://cloud.r-project.org/")'\ 
		-e 'bioc_pcks <- c("GenomicRanges","GenomicFeatures","GenomicAlignments","AnnotationDbi","Rsubread","plyranges")' \
		-e 'BiocManager::install(bioc_pcks)' \ 
		-e 'devtools::install_github("VPetukhov/ggrastr")' \
		-e 'devtools::install_github(repo = "mojaveazure/loomR", ref = "develop")'

##install samtools samtools-1.10
WORKDIR /usr/local/
RUN wget https://github.com/samtools/samtools/releases/download/1.10/samtools-1.10.tar.bz2
RUN tar -xjvf samtools-1.10.tar.bz2
RUN rm samtools-1.10.tar.bz2
WORKDIR /usr/local/samtools-1.10
RUN ./configure --prefix=/usr/local/samtools-1.10/
RUN make
RUN make install
ENV PATH /usr/local/samtools-1.10:$PATH


##install STAR 2.7.3a
ENV VERSION_STAR 2.7.3a
ENV URL_STAR "https://github.com/alexdobin/STAR/archive/${VERSION_STAR}.tar.gz"
RUN wget -q -O - $URL_STAR | tar -zxv && \
    cd STAR-${VERSION_STAR}/source && \
    make -j 4 && \
    cd .. && \
    cp ./bin/Linux_x86_64_static/STAR /usr/local/bin/ && \
    cd .. && \
    rm -rf ./STAR-${VERSION_STAR}


##install pigz
RUN apt-get install -y pigz 


#install zUMIs
WORKDIR /usr/local
RUN git clone https://github.com/sdparekh/zUMIs.git && \
 cd zUMIs && \
 mv zUMIs-master.sh zUMIs && \
 cd ..
ENV PATH /usr/local/zUMIs:$PATH


WORKDIR /usr/local
ENTRYPOINT ["tail", "-f", "/dev/null"]
