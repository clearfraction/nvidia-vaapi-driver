%define abi_package %{nil}
%global gitdate 20220719
%global commit 8e66a2fe429a57fda1bbd735842fe8fec87d1d7b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           nvidia-vaapi-driver
Version:        0.0.6
Release:        1.%{shortcommit}
Summary:        A VA-API implementation that uses NVDEC as a backend

License:        MIT
URL:            https://github.com/elFarto/nvidia-vaapi-driver/
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  libva-dev
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  mesa-dev
BuildRequires:  nv-codec-headers
BuildRequires:  gst-plugins-bad-dev
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(ffnvcodec)
BuildRequires:  pkgconfig(gstreamer-codecparsers-1.0)

Provides: %{name} = %{version}-%{release}

%description
This is a VA-API implementation that uses NVDEC as a backend.

%prep
%setup -n %{name}-%{commit}

%build
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export LDFLAGS="-Wl,-rpath=/opt/3rd-party/bundles/clearfraction/usr/lib64,-rpath=/usr/lib64"
export CFLAGS="$CFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "
export FCFLAGS="$FFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "
export FFLAGS="$FFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "
export CXXFLAGS="$CXXFLAGS -O3 -Ofast -falign-functions=32 -ffat-lto-objects -flto=auto -fno-semantic-interposition -mprefer-vector-width=256 "

CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" meson \
    --libdir=lib64 --prefix=/usr --buildtype=plain  builddir 

ninja -v -C builddir


%install
DESTDIR=%{buildroot} ninja -C builddir install

# Rename to nvdec to better describe the back-end used.
# Create a symbolic link keeping the name nvidia.
pushd %{buildroot}/usr/lib64/dri
mv nvidia_drv_video.so nvdec_drv_video.so
ln -s nvdec_drv_video.so nvidia_drv_video.so
popd


%files
%license COPYING
%doc README.md
%{_libdir}/dri/nvdec_drv_video.so
%{_libdir}/dri/nvidia_drv_video.so


%changelog
# based on https://github.com/clearfraction/gstreamer-libav

