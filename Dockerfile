# Get an ubuntu base image and install xyce dependencies
FROM ubuntu:18.04 as xyce_deps
RUN apt-get update && apt-get install -yq gcc g++ gfortran make cmake bison flex libfl-dev libfftw3-dev libsuitesparse-dev libblas-dev liblapack-dev libtool automake autoconf openmpi-bin libopenmpi-dev && apt-get clean

# Install the trilinos dependence from git
FROM xyce_deps as trillinos_git
RUN apt-get install -yq git && apt-get clean
RUN \
    mkdir -p /opt/Xyce && \
    cd /opt/Xyce && \
    git clone https://github.com/trilinos/Trilinos.git && \
    cd Trilinos && \
    git checkout trilinos-release-12-12-branch

# Build the trillinos dependency
FROM trillinos_git as trillinos_build
COPY reconfig.sh /opt/Xyce/
RUN \
    cd /opt/Xyce && \
    mkdir build && \
    cd build && \
    bash ../reconfig.sh && \
    make && \
    make install && \
    cd .. && rm -rf Trilinos build

# Clone and build xyce- serial 
FROM trillinos_build as xyce
RUN \
    git clone --depth 1 --branch Release-7.4.0 https://github.com/Xyce/Xyce.git /opt/Xyce/Xyce-7.4 && \
    cd /opt/Xyce/Xyce-7.4 && \
    ./bootstrap && \
    mkdir build && \
    cd build && \
    ../configure CXXFLAGS="-O3" ARCHDIR="/opt/Xyce/XyceLibs/Serial" CPPFLAGS="-I/usr/include/suitesparse" && \
    make && \
    make install && \
    cd .. && \
    rm -rf build && \
    cd ..

# Install python3 
FROM xyce as python3
RUN apt-get update && apt-get install -y python3 python3-pip

# Install some python dependences
FROM python3 as python3_deps
COPY . /opt/app
RUN pip3 install cython
RUN pip3 install numpy

# Install some PACT dependences and run it
FROM python3_deps as pact
RUN pip3 install -r /opt/app/requirements.txt
WORKDIR /opt/app/src
ENTRYPOINT [ "python3","PACT.py" ]
# CMD ["python3", "PACT.py", "../Intel/Intel_ID1_lcf.csv", "../Intel/Intel.config", "../Intel/modelParams_Intel.config", "--gridSteadyFile", "Intel.grid.steady"]