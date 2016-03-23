%define debug_package %{nil}
%define product_family DeskOS Linux
%define variant_titlecase Server
%define variant_lowercase server
%define release_name Core
%define base_release_version 7
%define full_release_version 7
%define dist_release_version 7
%define upstream_rel 7.2
%define centos_rel 2.1511
#define beta Beta
%define dist .el%{dist_release_version}.centos

Name:           deskos-release
Version:        %{base_release_version}
Release:        %{centos_rel}%{?dist}.2.10
Summary:        %{product_family} release file
Group:          System Environment/Base
URL:            https://deskosproject.org
License:        GPLv2
Provides:       centos-release = %{version}-%{release}
Provides:       centos-release(upstream) = %{upstream_rel}
Provides:       redhat-release = %{upstream_rel}
Provides:       system-release = %{upstream_rel}
Provides:       system-release(releasever) = %{base_release_version}
Obsoletes:      centos-release

Source0:        http://deskosproject.org/sources/deskos-release/deskos-release-%{base_release_version}-%{centos_rel}.tar.gz
Source1:        85-display-manager.preset
Source2:        90-default.preset

%description
%{product_family} release files

%prep
%setup -q -n deskos-release-%{base_release_version}

%build
echo OK

%install
rm -rf %{buildroot}

# create /etc
mkdir -p %{buildroot}/etc

# create /etc/system-release and /etc/redhat-release
echo "%{product_family} release %{full_release_version}.%{centos_rel} (%{release_name}) " > %{buildroot}/etc/centos-release
echo "Derived from Red Hat Enterprise Linux %{upstream_rel} (Source)" > %{buildroot}/etc/centos-release-upstream
ln -s centos-release %{buildroot}/etc/system-release
ln -s centos-release %{buildroot}/etc/redhat-release

# create /etc/os-release
cat << EOF >>%{buildroot}/etc/os-release
NAME="%{product_family}"
VERSION="%{full_release_version} (%{release_name})"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="%{full_release_version}"
PRETTY_NAME="%{product_family} %{full_release_version} (%{release_name})"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:deskosproject:deskos:7"
HOME_URL="https://deskosproject.org/"

EOF
# write cpe to /etc/system/release-cpe
echo "cpe:/o:deskosproject:deskos:7" > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file %{buildroot}/etc/pki/rpm-gpg
done

# copy yum repos
mkdir -p -m 755 %{buildroot}/etc/yum.repos.d
for file in CentOS-*.repo; do 
    install -m 644 $file %{buildroot}/etc/yum.repos.d
done

mkdir -p -m 755 %{buildroot}/etc/yum/vars
install -m 0644 yum-vars-infra %{buildroot}/etc/yum/vars/infra

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%centos_ver %{base_release_version}
%%centos %{base_release_version}
%%rhel %{base_release_version}
%%dist %dist
%%el%{base_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/centos-release
ln -s centos-release %{buildroot}/%{_datadir}/redhat-release
install -m 644 EULA %{buildroot}/%{_datadir}/centos-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/centos-release
ln -s centos-release %{buildroot}/%{_docdir}/redhat-release
install -m 644 GPL %{buildroot}/%{_docdir}/centos-release
install -m 644 Contributors %{buildroot}/%{_docdir}/centos-release

# copy systemd presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/systemd/system-preset/


%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/system-release
/etc/centos-release
/etc/centos-release-upstream
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/pki/rpm-gpg/
%config(noreplace) /etc/yum.repos.d/*
%config(noreplace) /etc/yum/vars/*
/etc/rpm/macros.dist
%{_docdir}/redhat-release
%{_docdir}/centos-release/*
%{_datadir}/redhat-release
%{_datadir}/centos-release/*
%{_prefix}/lib/systemd/system-preset/*

%changelog
* Mon Mar 21 2016 Ricardo Arguello <rarguello@deskosproject.org>
- Initial setup for DeskOS

* Tue Dec  1 2015 Johnny Hughes <johnny@centos.org>
- Bump Release for 1511
- Add CentOS-Media.repo and put CentOS-CR.repo in the
  tarball, then removed patch1000 

* Tue Mar 31 2015 Karanbir Singh <kbsingh@centos.org>
- rework upstream communication
- re-establish redhat-release as a symlink from centos-release

* Fri Mar 27 2015 Karanbir Singh <kbsingh@centos.org>
- dont auto enable the initial-setup tui mode

* Thu Mar 19 2015 Karanbir Singh <kbsingh@centos.org>
- Bump Release for 1503 
- add ABRT specific content to os-release
- split redhat-release from centos-release

* Tue Feb 17 2015 Karanbir Singh <kbsingh@centos.org>
- Include the CR repo for upcoming 7.1 release ( and beyond )

* Thu Aug 21 2014 Karanbir Singh <kbsingh@centos.org>
- add a yum var to route mirrorlist accurately
- add CentOS-fastrack repo
- Trim the CentOS-Debug-7 key
- rename the Debug repo to base-debug so yum-utils can consume easier

* Tue Jul 15 2014 Karanbir Singh <kbsingh@centos.org>
- add CentOS-7 Debug rpm key

* Fri Jul 4 2014 Karanbir Singh <kbsingh@centos.org>
- Roll in the final name change conversation results
- Stage for release content
- Add yum repos
- Add distro keys ( incomplete )

* Mon Jun 30 2014 Karanbir Singh <kbsingh@centos.org>
- add a macro to macros.dist to indicate just centos as well 

* Tue Jun 24 2014 Karanbir Singh <kbsingh@centos.org> 
- Trial run for CentOS DateStamp release
- Add stubs for the yum repos
- fix os-release to only have one ID_LIKE ( Avij #7171)
- make the yum repo definitions be config noreplace ( Trevor )

* Tue Jun 17 2014 Karanbir Singh <kbsingh@centos.org> 7.0.el7.0.140617.3
- rebuild for 2014-06-17 pub qa release
- ensure we get the right cpe info
- ensure centos-release is trackable

* Sat Jun 14 2014 Karanbir Singh <kbsingh@centos.org> 7.0.el7.0.140614.2
- prep for public QA release tag as broken

* Fri Jun 13 2014 Karanbir Singh <kbsingh@centos.org> 7-0.el7
- initial setup for centos-rc