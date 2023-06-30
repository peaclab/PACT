# This file will target linux systems; i looked for a centos 
# image that with python on docker hub
FROM centos/python-38-centos7

# Switch to root user
USER root

#Install required system packages as specified https://xyce.sandia.gov/documentation-tutorials/building-guide/#osxPreReq
RUN yum install -y epel-release \
    && yum update -y \
    && yum install -y \
        gcc \
        g++ \
        gfortran\
        git \
        make \
        cmake \
        fftw-devel \
        fftw \
        blas-devel \
        blas \
        lapack-devel \
        lapack\
        bison \
        flex \
        suitesparse-devel \
        suitesparse \
        autoconf \
        automake \
        libtool \
        openmpi-3.1.4 \
        openmpi-devel
 
# Install Trilinos
RUN git clone https://github.com/trilinos/Trilinos.git /trilinos \
    && cd /trilinos \
    && git checkout tags/trilinos-release-12-12-1

RUN mkdir -p $HOME/XyceLibs/Serial

 # Copy the script into the container
COPY reconfigure.sh /reconfigure.sh

# Serial build
# # Make the script executable
RUN chmod +x /reconfigure.sh \
    && cd $HOME/XyceLibs/Serial \
    && /bin/sh /reconfigure.sh\
    && make \
    && make install

# # # Parallel build
# # RUN mkdir /trilinos/build-parallel \
# #     && cd /trilinos/build-parallel \
# #     && /bin/sh /reconfigure.sh

  # Install XYCE from github 
RUN cd $HOME \
    && git clone https://github.com/Xyce/Xyce.git /Xyce \
    && cd /Xyce \
    && git checkout tags/Release-7.2.0 \
    && ./bootstrap \
    && yum install -y file 

# #  # Configure Xyce for the serial build directory
RUN mkdir -p $HOME/XyceInstall/Serial 

RUN cd $HOME/XyceInstall/Serial \
      &&  /Xyce/configure \
      CXXFLAGS="-O3" \
      ARCHDIR="$HOME/XyceLibs/Serial" \
      CPPFLAGS="-I/usr/include/suitesparse" \
      CFLAGS="-O3" \
    --enable-stokhos \
    --enable-amesos2 \
    --prefix=/XyceInstall/Serial

# # # Build and install Xyce
# RUN make \
#     && make install

# # Configure Xyce for the Parellel build directory
# # RUN /Xyce/configure \
# #     CXXFLAGS="-O3" \
# #     ARCHDIR="/XyceLibs/Serial" \
# #     CPPFLAGS="-I/usr/include/suitesparse" \
# #     --enable-mpi \
# #     CXX=mpicxx \
# #     CC=mpicc \
# #     F77=mpif77 \
# #     --enable-stokhos \
# #     --enable-amesos2 \
# #     --prefix=/XyceInstall/Parellel



# # Switch back to non-root user
# USER default

# # Set environment variables for Xyce and OpenMPI
# ENV PATH="/usr/local/Xyce-7.2.0/bin:${PATH}"
# ENV LD_LIBRARY_PATH="/usr/local/Xyce-7.2.0/lib:${LD_LIBRARY_PATH}"
# ENV LD_RUN_PATH="/usr/local/Xyce-7.2.0/lib:${LD_RUN_PATH}"
# ENV OMPI_MCA_btl_vader_single_copy_mechanism=none


# # Set the working directory
# WORKDIR /app

# # Copy your application files
# COPY . .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the example configuration files!!! 
# # COPY Example/ /app/Example/

# # Load modules
# #RUN source /etc/profile.d/modules.sh \
# #   && module load openmpi/3.1.4_gnu-10.2.0 \
# #   && module load xyce/7.4

# CMD ["python3", "/src/PACT.py", "/Intel/Intel_ID1_lcf.csv", "/Intel/Intel.config", "/Intel/modelParams_Intel.config", "--gridSteadyFile", "Intel.grid.steady"]

# # python3 VisualPACT.py ../Intel/Intel.cir.csv --fps 20 --overlay Example_overlay_images/Inteli7.PNG --dpi 100 