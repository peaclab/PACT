FROM ubuntu:focal as xyce_build

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y git cmake build-essential gcc g++ ninja-build gfortran make bison flex libfl-dev libfftw3-dev libsuitesparse-dev libblas-dev liblapack-dev libtool autoconf automake libopenmpi-dev openmpi-bin

RUN git clone --branch Release-7.4.0   --depth 1 https://github.com/Xyce/Xyce.git

RUN git clone --branch trilinos-release-12-12-1 --depth 1 https://github.com/trilinos/Trilinos.git

WORKDIR /Trilinos

RUN mkdir build && cd build && cmake -GNinja -DCMAKE_C_COMPILER=mpicc \
-DCMAKE_CXX_COMPILER=mpic++ \
-DCMAKE_Fortran_COMPILER=mpif77 \
-DCMAKE_CXX_FLAGS="-O3 -fPIC" \
-DCMAKE_C_FLAGS="-O3 -fPIC" \
-DCMAKE_Fortran_FLAGS="-O3 -fPIC" \
-DCMAKE_MAKE_PROGRAM="ninja" \
-DCMAKE_INSTALL_PREFIX="/opt/trilinos_parallel" \
-DTrilinos_ENABLE_NOX=ON \
-DNOX_ENABLE_LOCA=ON \
-DTrilinos_ENABLE_EpetraExt=ON \
-DEpetraExt_BUILD_BTF=ON \
-DEpetraExt_BUILD_EXPERIMENTAL=ON \
-DEpetraExt_BUILD_GRAPH_REORDERINGS=ON \
-DTrilinos_ENABLE_TrilinosCouplings=ON \
-DTrilinos_ENABLE_Ifpack=ON \
-DTrilinos_ENABLE_Isorropia=ON \
-DTrilinos_ENABLE_AztecOO=ON \
-DTrilinos_ENABLE_Belos=ON \
-DTrilinos_ENABLE_Teuchos=ON \
-DTrilinos_ENABLE_COMPLEX_DOUBLE=ON \
-DTrilinos_ENABLE_Amesos=ON \
-DAmesos_ENABLE_KLU=ON \
-DTrilinos_ENABLE_Amesos2=ON \
-DAmesos2_ENABLE_KLU2=ON \
-DAmesos2_ENABLE_Basker=ON \
-DTrilinos_ENABLE_Sacado=ON \
-DTrilinos_ENABLE_Stokhos=ON \
-DTrilinos_ENABLE_Kokkos=ON \
-DTrilinos_ENABLE_Zoltan=ON \
-DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES=OFF \
-DTrilinos_ENABLE_CXX11=ON \
-DTPL_ENABLE_AMD=ON \
-DAMD_LIBRARY_DIRS="/usr/lib" \
-DTPL_AMD_INCLUDE_DIRS="/usr/include/suitesparse" \
-DTPL_ENABLE_BLAS=ON \
-DTPL_ENABLE_LAPACK=ON \
-DTPL_ENABLE_MPI=ON ..

RUN cd build && cmake --build . && ninja install

WORKDIR /Xyce

RUN ./bootstrap && mkdir build && cd build && \
 ../configure CXXFLAGS="-O3" ARCHDIR="/opt/trilinos_parallel" CPPFLAGS="-I/usr/include/suitesparse" -enable-mpi \
CXX=mpicxx \
CC=mpicc \
F77=mpif77 \
--enable-stokhos \
--enable-amesos2 \
--prefix=/opt/XyceInstall/Parallel && \ 
make -j $(nproc) && make install

FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y nano vim python-is-python3 python3-pip gfortran bison flex libfl-dev libfftw3-dev libsuitesparse-dev libblas-dev liblapack-dev libtool libopenmpi-dev openmpi-bin
WORKDIR /
COPY --from=xyce_build /opt /opt

ENV PATH /opt/XyceInstall/Parallel/bin:$PATH

RUN useradd -ms /bin/bash pact

WORKDIR /home/pact

COPY ./requirements.txt requirements.txt

USER pact

RUN pip3 install -r requirements.txt

COPY --chown=pact:pact . ./

CMD ["/bin/bash"]