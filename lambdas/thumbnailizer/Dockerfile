FROM --platform=linux/amd64 amazonlinux:2 AS libreoffice-builder

ARG LIBREOFFICE_VERSION=7.3.2.2
ARG DOWNLOAD_PATH=https://github.com/LibreOffice/core/archive/libreoffice-${LIBREOFFICE_VERSION}.tar.gz

# Install build dependencies
RUN yum install -y yum-utils \
    && yum-config-manager --enable epel \
    && yum install -y \
    autoconf \
    ccache \
    expat-devel \
    fontconfig-devel \
    git \
    gmp-devel \
    google-crosextra-caladea-fonts \
    google-crosextra-carlito-fonts \
    icu \
    libcurl-devel \
    liberation-sans-fonts \
    liberation-serif-fonts \
    libffi-devel \
    libICE-devel \
    libicu-devel \
    libmpc-devel \
    libpng-devel \
    libSM-devel \
    libX11-devel \
    libXext-devel \
    libXrender-devel \
    libxslt-devel \
    mesa-libGL-devel \
    mesa-libGLU-devel \
    mpfr-devel \
    nasm \
    nspr-devel \
    nss-devel \
    openssl-devel \
    perl-Digest-MD5 \
    python3-devel \
    which
RUN yum groupinstall -y "Development Tools"

# The Amazon Linux 2 core repository is not kept up-to-date
# Some packages need to be installed from CentOS' repositories
RUN yum install -y \
    https://vault.centos.org/centos/8/AppStream/x86_64/os/Packages/liblangtag-0.6.2-8.el8.x86_64.rpm \
    https://vault.centos.org/centos/8/AppStream/x86_64/os/Packages/liblangtag-data-0.6.2-8.el8.noarch.rpm \
    https://vault.centos.org/centos/8/PowerTools/x86_64/os/Packages/gperf-3.1-5.el8.x86_64.rpm \ 
    https://vault.centos.org/centos/8/AppStream/x86_64/os/Packages/flex-2.6.1-9.el8.x86_64.rpm

# LibreOffice should not be installed as root
RUN groupadd -g 9999 libreoffice \ 
    && useradd -r -u 9999 -g libreoffice libreoffice

USER libreoffice

# Download LibreOffice source file
RUN cd /tmp \
    && curl -L ${DOWNLOAD_PATH} | tar -xz \
    && mv core-libreoffice-${LIBREOFFICE_VERSION} libreoffice

WORKDIR /tmp/libreoffice

# Prepare installation
ARG LC_CTYPE=en_US.UTF-8
ARG LC_ALL=en_US.UTF-8
RUN echo "lo_sources_ver=${LIBREOFFICE_VERSION}" >> sources.ver
RUN ./autogen.sh \
    --disable-avahi \
    --disable-cairo-canvas \
    --disable-coinmp \
    --disable-cups \
    --disable-cve-tests \
    --disable-dbus \
    --disable-dconf \
    --disable-dependency-tracking \
    --disable-evolution2 \
    --disable-dbgutil \
    --disable-extension-integration \
    --disable-extension-update \
    --disable-firebird-sdbc \
    --disable-gio \
    --disable-gstreamer-1-0 \
    --disable-gtk3 \
    --disable-introspection \
    --disable-largefile \
    --disable-lotuswordpro \
    --disable-lpsolve \
    --disable-odk \
    --disable-ooenv \
    --disable-pch \
    --disable-postgresql-sdbc \
    --disable-python \
    --disable-randr \
    --disable-report-builder \
    --disable-scripting-beanshell \
    --disable-scripting-javascript \
    --disable-sdremote \
    --disable-sdremote-bluetooth \
    --enable-mergelibs \
    --with-galleries="no" \
    --with-system-curl \
    --with-system-expat \
    --with-system-libxml \
    --with-system-nss \
    --with-system-openssl \
    --with-theme="no" \
    --without-export-validation \
    --without-fonts \
    --without-helppack-integration \
    --without-java \
    --without-junit \
    --without-krb5 \
    --without-myspell-dicts \
    --without-system-dicts

RUN make

# Strip symbols from object files
RUN strip ./instdir/**/* || true

# Not needed to run LibreOffice in --headless mode
RUN rm -rf /tmp/libreoffice/instdir/share/gallery \
    ./instdir/share/config/images_*.zip \
    ./instdir/readmes 

FROM --platform=linux/amd64 amazonlinux:2 AS ffmpeg-builder

ARG DOWNLOAD_PATH=https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

WORKDIR /tmp/ffmpeg

RUN yum install -y tar xz

RUN curl -L ${DOWNLOAD_PATH} | tar -xJ

WORKDIR /opt/ffmpeg

RUN mv /tmp/ffmpeg/*/ffmpeg /tmp/ffmpeg/*/ffprobe .

FROM --platform=linux/amd64 amazonlinux:2 AS imagemagick-builder

ARG IMAGE_MAGICK_VERSION=7.1.1-17
ARG DOWNLOAD_PATH=https://github.com/ImageMagick/ImageMagick/archive/refs/tags/${IMAGE_MAGICK_VERSION}.tar.gz

WORKDIR /tmp/image-magick

RUN yum install -y tar gzip libpng-devel libjpeg-devel libtiff-devel

RUN yum groupinstall -y "Development Tools"

RUN curl -L ${DOWNLOAD_PATH} | tar -xz

WORKDIR /tmp/image-magick/ImageMagick-${IMAGE_MAGICK_VERSION} 

RUN ./configure --prefix=/opt/imagemagick --enable-shared=no --enable-static=yes

RUN make

RUN make install

RUN strip /opt/imagemagick/**/* || true
RUN rm -drf /opt/imagemagick/include /opt/imagemagick/lib /opt/imagemagick/share

# Copy only the necessary files from the build image
FROM public.ecr.aws/lambda/python:3.11

# LibreOffice
COPY --from=libreoffice-builder /tmp/libreoffice/instdir /opt/libreoffice

# ffmpeg
COPY --from=ffmpeg-builder /opt/ffmpeg /opt/ffmpeg/

# ImageMagick
COPY --from=imagemagick-builder /opt/imagemagick/ /opt/imagemagick/

RUN yum install -y liberation-serif-fonts liberation-sans-fonts google-crosextra-caladea-fonts google-crosextra-carlito-fonts \
    libX11 libxslt libXrender libXext libICE libSM libtiff libgomp

# Copy function code
COPY src/ ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}

ENV LIBREOFFICE_PATH=/opt/libreoffice/program/soffice.bin
ENV PATH="$PATH:/opt/libreoffice/program:/opt/ffmpeg:/opt/imagemagick/bin"

# Install the specified packages
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_app.lambda_handler" ]