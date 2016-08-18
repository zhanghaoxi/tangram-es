Name:       tangram-es
Summary:    Tangram-ES Map Library
Version:    0.0.1
Release:    1
Group:      Framework/maps
License:    MIT
Source0:    %{name}-%{version}.tar.gz
Source1:    deps.tar.gz

#Requires(post): eglibc
#Requires(postun): eglibc

BuildRequires:  cmake
#BuildRequires:  pkgconfig(glib-2.0)
#BuildRequires:  pkgconfig(gmodule-2.0)
# BuildRequires: libicu-devel
BuildRequires:  pkgconfig(dlog)
BuildRequires: 	pkgconfig(libcurl)
BuildRequires: 	pkgconfig(icu-uc)
BuildRequires: 	pkgconfig(freetype2)
BuildRequires: 	pkgconfig(harfbuzz)
BuildRequires: 	pkgconfig(evas)
BuildRequires: 	pkgconfig(fontconfig)

#BuildRequires:  pkgconfig(capi-network-connection)
#BuildRequires: 	pkgconfig(capi-maps-service)
#BuildRequires:  capi-maps-service-plugin-devel
#BuildRequires:  pkgconfig(json-glib-1.0)
Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

# Requires: libicu = 54.1

%ifarch %{arm}
%define ARCH arm
%else
%define ARCH i586
%endif

%description
Tangram-ES Map Library.

%prep
# %setup -q
%setup -q

rmdir external/alfons
rmdir external/geojson-vt-cpp
rmdir external/yaml-cpp
rmdir core/include/glm
rmdir core/include/variant
rmdir core/include/isect2d
rmdir core/include/earcut.hpp
rmdir external/duktape

%setup -q -T -D -a 1


%build
%if 0%{?tizen_build_binary_release_type_eng}
export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE -g"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE -g"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
#echo "-------------------------------->>"
#find .
#echo "--------------------------------<<"
cmake .  -DCMAKE_BUILD_TYPE=Debug -DPLATFORM_TARGET=tizen-lib -DCMAKE_INSTALL_PREFIX=%{_prefix} -DMAJORVER=${MAJORVER} -DFULLVER=%{version}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}
# cp external/yaml-cpp/LICENSE %{buildroot}/usr/share/license/%{name}-yaml-cpp
# ... or embed the other licenses in LICENSE

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest tangram-es.manifest
%defattr(-,root,root,-)
%{_libdir}/libtangram.so
/usr/share/license/tangram-es

# %package devel
# Summary:    Tizen MapsQuest Maps Plug-in Library (Development)
# Group:      Framework/maps
# Requires:   %{name} = %{version}-%{release}
#
# %description devel
# Tangram-ES. (Development)
#
# %post devel
# /sbin/ldconfig
#
# %postun devel
# /sbin/ldconfig
#
# %files devel
# %defattr(-,root,root,-)
# %{_includedir}/mapquest-plugin/*.h
# %{_libdir}/pkgconfig/maps-plugin-mapquest.pc
# %{_libdir}/maps/plugins/libmaps-plugin-mapquest.so

# %package test
# Summary:    Tizen MapQuest Maps Plug-in Library (Internal Dev)
# Group:      Framework/maps
# Requires:   capi-maps-service = %{version}-%{release}

# %description test
# This packages provides Plugin APIs capsulating MapQuest Maps Open APIs for Maps Service Library. (Internal Dev)

