Summary:	The new version of Logical Volume Manager for Linux
Name:		lvm2
Version:	2.02.117
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/lvm2/LVM2.%{version}.tgz
# Source0-md5:	ab5889dae7924b44ed2444161058a419
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
	--enable-lvmetad		\
	--enable-pkgconfig		\
	--enable-readline		\
	--enable-udev-systemd-background-jobs	\
	--with-cache=internal		\
	--with-default-dm-run-dir=/run	\
	--with-default-locking-dir=/run/lock/lvm    \
	--with-default-pid-dir=/run	\
	--with-default-run-dir=/run/lvm	\
	--with-group=			\
	--with-interface=ioctl		\
	--with-lvm1=internal		\
	--with-mirrors=internal		\
	--with-optimisation="%{rpmcflags}"	\
	--with-pool=internal		\
	--with-snapshots=internal	\
	--with-thin=internal		\
	--with-user=			\
	--with-usrlibdir=%{_libdir}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/lvm \
    $RPM_BUILD_ROOT%{systemdunitdir}/sockets.target.wants

%{__make} install install_system_dirs install_systemd_units \
	DESTDIR=$RPM_BUILD_ROOT \
	OWNER="" \
	GROUP=""

ln -sf ../dm-event.socket \
    $RPM_BUILD_ROOT%{systemdunitdir}/sockets.target.wants/dm-event.socket

touch $RPM_BUILD_ROOT%{_sysconfdir}/lvm/lvm.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post   -n device-mapper -p /usr/sbin/ldconfig
%postun -n device-mapper -p /usr/sbin/ldconfig

%if 0
%endif

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/lvmlocal.conf
%attr(750,root,root) %dir %{_sysconfdir}/lvm/profile
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/profile/*.profile
%{systemdunitdir}/blk-availability.service
%{systemdunitdir}/lvm2-lvmetad.service
%{systemdunitdir}/lvm2-lvmetad.socket
%{systemdunitdir}/lvm2-monitor.service
%{systemdunitdir}/lvm2-pvscan@.service

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
%{systemdunitdir}/dm-event.service
%{systemdunitdir}/dm-event.socket
%{systemdunitdir}/sockets.target.wants/dm-event.socket
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

