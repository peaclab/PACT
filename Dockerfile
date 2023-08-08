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

# Build the trillinos-serial dependency
FROM trillinos_git as trillinos_serial_build
COPY reconfig.sh /opt/Xyce/
RUN \
    cd /opt/Xyce && \
    mkdir build_serial && \
    cd build_serial && \
    bash ../reconfig.sh && \
    make && \
    make install && \
    cd .. && rm -rf build_serial

# Clone and build xyce- serial 
FROM trillinos_serial_build as xyce_serial
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

# Build the trillinos-serial dependency
FROM xyce_serial as trillinos_parallel_build
COPY reconfig_parallel.sh /opt/Xyce/
RUN \
    cd /opt/Xyce && \
    mkdir build_parallel && \
    cd build_parallel && \
    bash ../reconfig_parallel.sh && \
    make && \
    make install && \
    cd .. && rm -rf Trilinos build_parallel

# Clone and build xyce- parallel 
FROM trillinos_parallel_build as xyce_parallel
RUN \
    cd /opt/Xyce/Xyce-7.4 && \
    mkdir build_parallel && \
    cd build_parallel && \
    ../configure CXXFLAGS="-O3" ARCHDIR="/opt/Xyce/XyceLibs/Parallel" CPPFLAGS="-I/usr/include/suitesparse" --enable-mpi \
    CXX=mpicxx \
    CC=mpicc \
    F77=mpif77 \
    --enable-stokhos \
    --enable-amesos2 && \
    make && \
    make install && \
    cd .. && \
    rm -rf build_parallel && \
    cd ..

# Install python3 
FROM xyce_parallel as python3
RUN apt-get update && apt-get install -y python3 python3-pip

# Install some python dependences
FROM python3 as python3_deps
COPY requirements.txt .
RUN pip3 install cython
RUN pip3 install numpy
RUN pip3 install -r requirements.txt

# Install some PACT dependences and run it
FROM python3_deps as pact
COPY . /opt/app

# Add a new user "pactuser" with user id 8877
RUN useradd -u 8877 pactuser
# Set permissions for /opt/app directory
RUN chown -R pactuser:pactuser /opt/app
RUN chmod -R 777 /opt/app

WORKDIR /opt/app/src

# Change to non-root privilege
USER pactuser
ENTRYPOINT [ "python3","PACT.py" ]
