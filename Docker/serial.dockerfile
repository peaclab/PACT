FROM ubuntu:focal as xyce_build

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y gcc g++ build-essential ninja-build gfortran make cmake bison flex libfl-dev libfftw3-dev libsuitesparse-dev libblas-dev liblapack-dev libtool automake autoconf

RUN git clone --branch Release-7.4.0   --depth 1 https://github.com/Xyce/Xyce.git

RUN git clone --branch trilinos-release-12-12-1 --depth 1 https://github.com/trilinos/Trilinos.git

WORKDIR /Trilinos

ARG FLAGS="-O3 -fPIC"

RUN mkdir build && cd build && cmake -GNinja \
-DCMAKE_C_COMPILER=gcc \
-DCMAKE_CXX_COMPILER=g++ \
-DCMAKE_Fortran_COMPILER=gfortran \
-DCMAKE_CXX_FLAGS="$FLAGS" \
-DCMAKE_C_FLAGS="$FLAGS" \
-DCMAKE_Fortran_FLAGS="$FLAGS" \
-DCMAKE_INSTALL_PREFIX="/opt/trilinos_serial" \
-DCMAKE_MAKE_PROGRAM="ninja" \
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
  -DTeuchos_ENABLE_COMPLEX=ON \
-DTrilinos_ENABLE_Amesos=ON \
  -DAmesos_ENABLE_KLU=ON \
-DTrilinos_ENABLE_Sacado=ON \
-DTrilinos_ENABLE_Kokkos=OFF \
-DTrilinos_ENABLE_ALL_OPTIONAL_PACKAGES=OFF \
-DTrilinos_ENABLE_CXX11=OFF \
-DTPL_ENABLE_AMD=ON \
-DAMD_LIBRARY_DIRS="/usr/lib" \
-DTPL_AMD_INCLUDE_DIRS="/usr/include/suitesparse" \
-DTPL_ENABLE_BLAS=ON \
-DTPL_ENABLE_LAPACK=ON ..

RUN cd build && cmake --build . && ninja install

WORKDIR /Xyce

RUN ./bootstrap && mkdir build && cd build && \
 ../configure CXXFLAGS="-O3" ARCHDIR="/opt/trilinos_serial" CPPFLAGS="-I/usr/include/suitesparse" \
--prefix=/opt/XyceInstall/Serial && \ 
make -j $(nproc) && make install

FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y nano vim python-is-python3 python3-pip gfortran bison flex libfl-dev libfftw3-dev libsuitesparse-dev libblas-dev liblapack-dev libtool
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