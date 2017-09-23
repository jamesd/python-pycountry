# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?__python2: %global __python2 %__python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global prjname pycountry
%global prjown  flyingcircus
%global shortcommit0 658386a36300

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{prjname}
Version:        17.9.23
Release:        1%{?dist}
Summary:        ISO databases for the standards

License:        LGPLv2
URL:            https://pypi.python.org/pypi/%{prjname}/
Source0:        https://bitbucket.org/%{prjown}/%{prjname}/get/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
%if %{with python3}
BuildRequires:  python3-devel
%endif # with python3

%description
pycountry provides the ISO databases for the standards:

639
    Languages
3166
    Countries
3166-3
    Deleted countries
3166-2
    Subdivisions of countries
4217
    Currencies
15924
    Scripts

The package includes a copy from Debian’s pkg-isocodes and makes the
data accessible through a Python API.

Translation files for the various strings are included as well.

%if %{with python3}
%package -n python3-%{prjname}
Summary:       %{summary} 

%description -n python3-%{prjname}
%{summary}

%endif # with python3


%prep
%autosetup -c -n %{prjown}-%{prjname}-%{shortcommit0}
ls
mv %{prjown}-%{prjname}-%{shortcommit0} python2

%if %{with python3}
cp -a python2 python3
%endif # with python3


%build
pushd python2
%{__python2} setup.py build
popd

%if %{with python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with python3


%install
rm -rf $RPM_BUILD_ROOT
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with python3

pushd python2
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd


%check
pushd python2
%{__python2} setup.py test
popd

%if %{with python3}
pushd python3
%{__python3} setup.py test
popd
%endif


%files
%license python2/LICENSE.txt
%doc python2/README python2/TODO.txt python2/HISTORY.txt
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-%{prjname}
%license python3/LICENSE.txt
%doc python3/README python3/TODO.txt python3/HISTORY.txt
%{python3_sitelib}/*
%endif # with python3


%changelog
* Sat Sep 23 2017 James Davidson <james@greycastle.net> - 17.9.23-1
- Update to upstream release 17.9.23
- Fix rpmlint issues

* Sun Aug 28 2016 James Davidson <james@greycastle.net>
- Initial packaging
