%global forgeurl https://github.com/facebook/fb303/
# take the date fbthrift is tagged
# and use the last fb303 commit prior to that date
%global commit 2b3b110f2b8c27f70ba0fe1e81b0213cae62bc0a
%global date 20201130

# add -i for outputting more info
%forgemeta

# need to figure out how to get the Python bindings to build later
%bcond_with python

## Depends on fizz, which has linking issues on some platforms:
# https://bugzilla.redhat.com/show_bug.cgi?id=1893332
%ifarch i686 x86_64
%bcond_without static
%else
%bcond_with static
%endif

%global _static_builddir static_build

Name:           fb303
Version:        0
Release:        0.1%{?dist}
Summary:        Base Thrift service and a common set of functionality

License:        ASL 2.0
URL:            %{forgeurl}
Source0:        %{forgesource}
Patch0:         %{name}-explicit_glog.patch

# Folly is known not to work on big-endian CPUs
ExcludeArch:    s390x

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  fbthrift-devel
BuildRequires:  fizz-devel
BuildRequires:  folly-devel
BuildRequires:  gflags-devel
BuildRequires:  glog-devel
%if %{with python}
BuildRequires:  python3-devel
BuildRequires:  python3-fbthrift-devel
%endif
BuildRequires:  wangle-devel
#Requires:

%description
fb303 is a base Thrift service and a common set of functionality for querying
stats, options, and other information from a service.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake-filesystem

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%if %{with static}
%package        static
Summary:        Static development libraries for %{name}
BuildRequires:  fbthrift-static
BuildRequires:  fizz-static
BuildRequires:  folly-static
BuildRequires:  wangle-static
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    static
The %{name}-static package contains static libraries for
developing applications that use %{name}.
%endif


%prep
# forgesetup doesn't take patches
%autosetup -n %{name}-%{commit} -p1


%build
%if %{with static}
# static build
mkdir %{_static_builddir}
pushd %{_static_builddir}
%cmake .. \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name}-static \
  -DFBTHRIFT_ROOT=%{_libdir}/cmake/fbthrift-static \
  -DFIZZ_ROOT=%{_libdir}/cmake/fizz-static \
  -DFOLLY_ROOT=%{_libdir}/cmake/folly-static \
  -DWANGLE_ROOT=%{_libdir}/cmake/wangle-static \
  -DPYTHON_EXTENSIONS=OFF
%cmake_build
popd

%endif
%cmake \
  -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DPACKAGE_VERSION=0.%{date} \
%if %{with python}
  -DPYTHON_EXTENSIONS=ON
%else
  -DPYTHON_EXTENSIONS=OFF
%endif
%cmake_build


%install
%if %{with static}
# static build
pushd %{_static_builddir}
%cmake_install
popd
%endif

%cmake_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%files
%license LICENSE
%doc README.md
%{_libdir}/*.so.*

%files devel
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/%{name}/

%if %{with static}
%files static
%{_libdir}/*.a
%{_libdir}/cmake/%{name}-static
%endif


%changelog
* Mon Nov 30 14:54:10 PST 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 0-0.1.20201130git2b3b110
- Update to snapshot from 20201130

* Mon Nov 23 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 0-0.1.20201123git94cac88
- Initial package
