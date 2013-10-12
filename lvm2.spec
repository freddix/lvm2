Summary:	The new version of Logical Volume Manager for Linux
Name:		lvm2
Version:	2.02.103
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/lvm2/LVM2.%{version}.tgz
# Source0-md5:	e427e3494aaf86da2d363f344deb3837
URL:		http://sources.redhat.com/lvm2/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	readline-devel
Requires:	device-mapper >= %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	'.*libdevmapper-event-lvm2.so.*'

%description
This package includes a number of utilities for creating, checking,
and repairing logical volumes.

%package -n device-mapper
Summary:	Userspace support for the device-mapper
Group:		Base

%description -n device-mapper
The goal of this driver is to support volume management. The driver
enables the definition of new block devices composed of ranges of
sectors of existing devices. This can be used to define disk
partitions - or logical volumes. This light-weight kernel component
can support user-space tools for logical volume management.

%package -n device-mapper-devel
Summary:	Header files and development documentation for %{name}
Group:		Development/Libraries
Requires:	device-mapper = %{version}-%{release}

%description -n device-mapper-devel
Header files and development documentation for %{name}.

%prep
%setup -qn LVM2.%{version}

%build
export CC="%{__cc}"
%configure \
	--disable-selinux		\
	--enable-applib			\
	--enable-cmdlib			\
	--enable-dmeventd		\
	--enable-fsadm			\
	--enable-pkgconfig		\
	--enable-readline		\
	--with-cluster=internal		\
	--with-group=			\
	--with-interface=ioctl		\
	--with-lvm1=internal		\
	--with-mirrors=internal		\
	--with-optimisation="%{rpmcflags}"	\
	--with-pool=internal		\
	--with-snapshots=internal	\
	--with-user=			\
	--with-usrlibdir=%{_libdir}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/lvm,/%{_lib}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	OWNER="" \
	GROUP=""

touch $RPM_BUILD_ROOT%{_sysconfdir}/lvm/lvm.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post   -n device-mapper -p /usr/sbin/ldconfig
%postun -n device-mapper -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README WHATS_NEW doc/*
%attr(755,root,root) %{_sbindir}/*
%exclude %{_sbindir}/dmeventd
%exclude %{_sbindir}/dmsetup
%{_mandir}/man?/*
%exclude %{_mandir}/man8/dmsetup.8*
%attr(750,root,root) %dir %{_sysconfdir}/lvm
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/lvm.conf

%files -n device-mapper
%defattr(644,root,root,755)
%doc *_DM
%attr(755,root,root) %{_sbindir}/dmeventd
%attr(755,root,root) %{_sbindir}/dmsetup
%attr(755,root,root) %{_libdir}/libdevmapper*.so.*.*
%attr(755,root,root) %{_libdir}/liblvm2app.so.*.*
%attr(755,root,root) %{_libdir}/liblvm2cmd.so.*.*
%dir %{_libdir}/device-mapper
%attr(755,root,root) %{_libdir}/device-mapper/*.so
%{_mandir}/man8/dmsetup.8*

%files -n device-mapper-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdevmapper*.so
%attr(755,root,root) %{_libdir}/liblvm2app.so
%attr(755,root,root) %{_libdir}/liblvm2cmd.so
%{_includedir}/libdevmapper*.h
%{_includedir}/lvm2app.h
%{_includedir}/lvm2cmd.h
%{_pkgconfigdir}/*.pc

