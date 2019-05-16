Name:           gluu-docs
Version:        0.1
Release:        1%{?dist}
Summary:        Gluu Documentation
License:        GPLv2 
URL:            http://www.gluu.org 
Source0:        %{name}-%{version}.tar.gz
BuildArch: 	noarch
BuildRequires:  python27
Requires:       httpd

%description


%prep
%setup -q


%build
/usr/bin/virtualenv env
env/bin/pip install -r requirements.txt
env/bin/mkdocs build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_defaultdocdir}/gluu-docs
cp -r site/* %{buildroot}/%{_defaultdocdir}/gluu-docs/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_defaultdocdir}/gluu-docs/*


%changelog
* Tue Apr 28 2015 Adrian Alves <adrian@gluu.org> - 0.1-1
- Initial build
