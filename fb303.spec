%global forgeurl https://github.com/facebook/fb303/
# take the date fbthrift is tagged
# and use the first "Updating submodules" commit from that day
%global commit bd92ca817da526f9b57faa6b0f70445c80a6318f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211220

# need to figure out how to get the Python bindings to build later
%bcond_with python

## Depends on fizz, which has linking issues on some platforms:
# https://bugzilla.redhat.com/show_bug.cgi?id=1893332
%ifarch %ix86 x86_64
%bcond_without static
%else
%bcond_with static
%endif

# No tests were found!!!
%bcond_with tests

%global _static_builddir static_build

Name:           fb303
Version:        0
Release:        0.7.%{date}git%{shortcommit}%{?dist}
Summary:        Base Thrift service and a common set of functionality

License:        ASL 2.0
URL:            %{forgeurl}
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

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

%global _description %{expand:
fb303 is a base Thrift service and a common set of functionality for querying
stats, options, and other information from a service.}

%description %{_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake-filesystem

%description    devel %{_description}

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

%description    static %{_description}

The %{name}-static package contains static libraries for
developing applications that use %{name}.
%endif


%prep
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


%if %{with tests}
%check
%ctest
%endif


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
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.7.20211220gitbd92ca8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

%autochangelog
