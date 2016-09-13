%define debug_package %{nil}
%define product_family DeskOS Linux
%define release_name Core
%define base_release_version 7
%define full_release_version 7
%define dist_release_version 7
%define upstream_rel 7.2
%define centos_rel 2.1511
%define deskos_rel 2.1609
%define dist .el%{dist_release_version}.deskos

Name:           deskos-release
Version:        %{base_release_version}
Release:        %{deskos_rel}.0.1
Summary:        %{product_family} release file
Group:          System Environment/Base
URL:            https://deskosproject.org
License:        GPLv2
Provides:       centos-release = %{version}
Provides:       centos-release(upstream) = %{upstream_rel}
Provides:       redhat-release = %{upstream_rel}
Provides:       system-release = %{upstream_rel}
Provides:       system-release(releasever) = %{base_release_version}
Obsoletes:      centos-release

Source0:        https://dl.deskosproject.org/sources/deskos-release/deskos-release-%{base_release_version}-%{deskos_rel}.tar.gz
Source1:        85-display-manager.preset
Source2:        90-default.preset
Source3:        80-deskos.preset
Source4:        DeskOS.repo
Source5:        RPM-GPG-KEY-DeskOS-7

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
echo "%{product_family} release %{full_release_version}.%{deskos_rel} (%{release_name}) " > %{buildroot}/etc/centos-release
echo "Derived from Red Hat Enterprise Linux %{upstream_rel} (Source)" > %{buildroot}/etc/centos-release-upstream
echo "Derived from CentOS Linux %{full_release_version}.%{centos_rel}" > %{buildroot}/etc/deskos-release-upstream
ln -s centos-release %{buildroot}/etc/system-release
ln -s centos-release %{buildroot}/etc/redhat-release
ln -s centos-release %{buildroot}/etc/deskos-release

# create /etc/os-release
cat << EOF >>%{buildroot}/etc/os-release
NAME="%{product_family}"
VERSION="%{full_release_version} (%{release_name})"
ID="deskos"
ID_LIKE="centos rhel fedora"
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

# DeskOS Repo
install -m 644 %{SOURCE4} %{buildroot}/etc/yum.repos.d

# DeskOS GPG Key
install -m 644 %{SOURCE5} %{buildroot}/etc/pki/rpm-gpg

mkdir -p -m 755 %{buildroot}/etc/yum/vars
install -m 0644 yum-vars-infra %{buildroot}/etc/yum/vars/infra

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%deskos_ver %{base_release_version}
%%deskos %{base_release_version}
%%centos_ver %{base_release_version}
%%centos %{base_release_version}
%%rhel %{base_release_version}
%%dist %dist
%%el%{base_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/centos-release
ln -s centos-release %{buildroot}/%{_datadir}/redhat-release
ln -s centos-release %{buildroot}/%{_datadir}/deskos-release
install -m 644 EULA %{buildroot}/%{_datadir}/centos-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/centos-release
ln -s centos-release %{buildroot}/%{_docdir}/redhat-release
ln -s centos-release %{buildroot}/%{_docdir}/deskos-release
install -m 644 GPL %{buildroot}/%{_docdir}/centos-release
install -m 644 Contributors %{buildroot}/%{_docdir}/centos-release

# copy systemd presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE3} %{buildroot}%{_prefix}/lib/systemd/system-preset/


%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/deskos-release
/etc/system-release
/etc/centos-release
/etc/deskos-release-upstream
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
%{_docdir}/deskos-release
%{_docdir}/centos-release/*
%{_datadir}/redhat-release
%{_datadir}/deskos-release
%{_datadir}/centos-release/*
%{_prefix}/lib/systemd/system-preset/*

%changelog
* Thu Sep 1 2016 Ricardo Arguello <rarguello@deskosproject.org>
- Changed the release number and added /etc/deskos-release

* Wed Aug 24 2016 Ricardo Arguello <rarguello@deskosproject.org>
- Added deskos-testing repo

* Thu May 12 2016 Ricardo Arguello <rarguello@deskosproject.org>
- GPG Key added

* Mon Mar 21 2016 Ricardo Arguello <rarguello@deskosproject.org>
- Initial setup for DeskOS
