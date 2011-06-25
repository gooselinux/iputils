Summary: Network monitoring tools including ping
Name: iputils
Version: 20071127
Release: 13%{?dist}
License: BSD with advertising and GPLv2+ and Rdisc
URL: http://www.skbuff.net/iputils
Group: System Environment/Daemons

Source0: http://www.skbuff.net/iputils/%{name}-s%{version}.tar.bz2
Source1: ifenslave.tar.gz
Source3: rdisc.initd

Patch0: iputils-20020927-rh.patch
Patch1: iputils-20020124-countermeasures.patch
Patch2: iputils-20020927-addrcache.patch
Patch3: iputils-20020927-ping-subint.patch
Patch4: iputils-ping_cleanup.patch
Patch5: iputils-ifenslave.patch
Patch6: iputils-20020927-arping-infiniband.patch
Patch7: iputils-20070202-idn.patch
Patch8: iputils-20070202-open-max.patch
Patch9: iputils-20070202-traffic_class.patch
Patch10: iputils-20070202-arping_timeout.patch
Patch11: iputils-20071127-output.patch
Patch12: iputils-20070202-ia64_align.patch
Patch13: iputils-20071127-warnings.patch
Patch14: iputils-20071127-typing_bug.patch
Patch15: iputils-20071127-corr_type.patch
Patch16: iputils-20071127-timeout.patch
Patch17: iputils-20071127-flowlabel.patch
Patch18: iputils-20071127-dosping.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: docbook-utils perl-SGMLSpm
BuildRequires: glibc-kernheaders >= 2.4-8.19
BuildRequires: libidn-devel
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

%description
The iputils package contains basic utilities for monitoring a network,
including ping. The ping command sends a series of ICMP protocol
ECHO_REQUEST packets to a specified network host to discover whether
the target machine is alive and receiving network traffic.

%prep
%setup -q -a 1 -n %{name}-s%{version}

%patch0 -p1 -b .rh
%patch1 -p1 -b .countermeasures
%patch2 -p1 -b .addrcache
%patch3 -p1 -b .ping-subint
%patch4 -p1 -b .cleanup
%patch5 -p1 -b .addr
%patch6 -p1 -b .infiniband
%patch7 -p1 -b .idn
%patch8 -p1 -b .open-max
%patch9 -p1 -b .traffic_class
%patch10 -p1 -b .arping_timeout
%patch11 -p1 -b .output
%patch12 -p1 -b .ia64_align
%patch13 -p1 -b .warnings
%patch14 -p1 -b .typing_bug
%patch15 -p1 -b .corr_type
%patch16 -p1 -b .timeout
%patch17 -p1 -b .flowlabel
%patch18 -p1 -b .dosping

%build
%ifarch s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIE -Werror"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -Werror"
%endif
export LDFLAGS="-pie"
make %{?_smp_mflags} arping clockdiff ping ping6 rdisc tracepath tracepath6
gcc -Wall $RPM_OPT_FLAGS ifenslave.c -o ifenslave
make -C doc man

%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}/{bin,sbin}
install -c clockdiff		${RPM_BUILD_ROOT}%{_sbindir}/
install -cp arping		${RPM_BUILD_ROOT}/sbin/
ln -s /sbin/arping		${RPM_BUILD_ROOT}%{_sbindir}/arping
install -cp ping		${RPM_BUILD_ROOT}/bin/
install -cp ifenslave		${RPM_BUILD_ROOT}/sbin/
install -cp rdisc		${RPM_BUILD_ROOT}/sbin/
install -cp ping6		${RPM_BUILD_ROOT}/bin/
install -cp tracepath		${RPM_BUILD_ROOT}/bin/
install -cp tracepath6		${RPM_BUILD_ROOT}/bin/

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
ln -sf /bin/ping6 ${RPM_BUILD_ROOT}%{_sbindir}
ln -sf /bin/tracepath ${RPM_BUILD_ROOT}%{_sbindir}
ln -sf /bin/tracepath6 ${RPM_BUILD_ROOT}%{_sbindir}

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
install -cp doc/clockdiff.8	${RPM_BUILD_ROOT}%{_mandir}/man8/
install -cp doc/arping.8	${RPM_BUILD_ROOT}%{_mandir}/man8/
install -cp doc/ping.8		${RPM_BUILD_ROOT}%{_mandir}/man8/
install -cp doc/rdisc.8		${RPM_BUILD_ROOT}%{_mandir}/man8/
install -cp doc/tracepath.8	${RPM_BUILD_ROOT}%{_mandir}/man8/
install -cp ifenslave.8		${RPM_BUILD_ROOT}%{_mandir}/man8/
ln -s ping.8.gz ${RPM_BUILD_ROOT}%{_mandir}/man8/ping6.8.gz
ln -s tracepath.8.gz ${RPM_BUILD_ROOT}%{_mandir}/man8/tracepath6.8.gz

install -dp ${RPM_BUILD_ROOT}%{_sysconfdir}/rc.d/init.d
install -m 755 -p %SOURCE3 ${RPM_BUILD_ROOT}%{_sysconfdir}/rc.d/init.d/rdisc

iconv -f ISO88591 -t UTF8 RELNOTES -o RELNOTES.tmp
touch -r RELNOTES RELNOTES.tmp
mv -f RELNOTES.tmp RELNOTES

%post
/sbin/chkconfig --add rdisc

%preun
if [ $1 = 0 ]; then
	service rdisc stop >/dev/null 2>&1
	/sbin/chkconfig --del rdisc
fi 

%postun
if [ "$1" -ge "1" ]; then
	service rdisc status 2>&1 > /dev/null
	if [ $? -eq 0 ]; then
		service rdisc restart >/dev/null 2>&1 || :
	fi
fi


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc RELNOTES README.bonding
%{_sbindir}/clockdiff
/sbin/arping
%{_sbindir}/arping
%attr(4755,root,root) /bin/ping
/sbin/ifenslave
/sbin/rdisc
%attr(4755,root,root) /bin/ping6
/bin/tracepath
/bin/tracepath6
%{_sbindir}/ping6
%{_sbindir}/tracepath
%{_sbindir}/tracepath6
%attr(644,root,root) %{_mandir}/man8/*
%{_sysconfdir}/rc.d/init.d/rdisc

%changelog
* Tue Jul 27 2010 Ondrej Vasik <ovasik@redhat.com> - 20071127-13
- Resolves: CVE-2010-2529 - prevent DoS vulnerability in ping
  
* Wed May 12 2010 Jiri Skala <jskala@redhat.com> - 20071127-12
- Resolves: #586114 - ping6 does not support -F flowlabel and nexthop option

* Tue Mar 16 2010 Jiri Skala <jskala@redhat.com> - 20071127-11
- Resolves: #574036 - arping ignores the deadline option

* Wed Jan 06 2010 Jiri Skala <jskala@redhat.com> - 20071127-10
- Related: rhbz#543948
- fixed license

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 20071127-9.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071127-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Jiri Skala <jskala@redhat.com> - 20071127-8
- remake type conversions to gcc4.4 requirements

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071127-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 26 2008 Jiri Skala <jskala@redhat.com> - 20071127-6
- #455713 not accepted - suid is back

* Fri Aug 15 2008 Jiri Skala <jskala@redhat.com> - 20071127-5
- removed a dependency on libsysfs library in arping

* Wed Aug 06 2008 Jiri Skala <jskala@redhat.com> - 20071127-4
- Resolves: #455713 remove suid from ping
- corrected typing error in man

* Tue Jun 03 2008 Martin Nagy <mnagy@redhat.com> - 20071127-3
- major patch cleanup so it will be easier to get patches upstream
- fix for #68212, previous fix actually didn't work for ping6
- renewed the ia64 align patches
- update README.bonding
- clear up the code from warnings
- spec file cleanup

* Tue Mar 25 2008 Martin Nagy <mnagy@redhat.com> - 20071127-2
- fix inconsistent behaviour of ping (#360881)

* Mon Feb 25 2008 Martin Nagy <mnagy@redhat.com> - 20071127-1
- update to new upstream version

* Mon Feb 18 2008 Martin Nagy <mnagy@redhat.com> - 20070202-9
- rebuild

* Mon Feb 18 2008 Martin Nagy <mnagy@redhat.com> - 20070202-8
- correctly fix the -w option and return code of arping (#387881)

* Fri Feb 01 2008 Martin Nagy <mnagy@redhat.com> - 20070202-7
- fix -Q option of ping6 (#213544)

* Mon Jan 14 2008 Martin Nagy <mnagy@redhat.com> - 20070202-6
- fix absolute symlinks and character encoding for RELNOTES (#225909)
- preserve file timestamps (#225909)
- use %%{?_smp_mflags} (#225909)
- fix service rdisc stop removing of lock file

* Fri Sep 14 2007 Martin Bacovsky <mbacovsk@redhat.com> - 20070202-5
- rebuild

* Fri Aug  3 2007 Martin Bacovsky <mbacovsk@redhat.com> - 20070202-4
- resolves: #236725: ping does not work for subsecond intervals for ordinary user
- resolves: #243197: RFE: Please sync ifenslave with current kernel
- resolves: #246954: Initscript Review
- resolves: #251124: can't build rdisc - OPEN_MAX undeclared

* Fri Apr  6 2007 Martin Bacovsky <mbacovsk@redhat.com> - 20070202-3
- resolves: #235374: Update of iputils starts rdisc, breaking connectivity 

* Tue Mar 27 2007 Martin Bacovsky <mbacovsk@redhat.com> - 20070202-2
- Resolves: #234060: [PATCH] IDN (umlaut domains) support for ping and ping6
  patch provided by Robert Scheck <redhat@linuxnetz.de>

* Thu Mar 15 2007 Martin Bacovsky <mbacovsk@redhat.com> - 20070202-1
- upgarde to new upstream iputils-s20070202
- Resolves: #229995
- Resolves: #225909 - Merge Review: iputils
- patches revision

* Thu Feb 22 2007 Martin Bacovsky <mbacovsk@redhat.com>- 20020927-42
- Resolves: #218706 - now defines the destination address along RFC3484
- Resolves: #229630 - ifenslave(8) man page added
- Resolves: #213716 - arping doesn't work on InfiniBand ipoib interfaces
 
* Wed Sep 13 2006 Radek Vokal <rvokal@redhat.com> - 20020927-41
- new ifenslave/bonding documentation

* Mon Aug 21 2006 Martin Bacovsky <mbacovsk@redhat.com> - 20020927-40 
- tracepath doesn't continue past destination host (#174032) 
  previous patch replaced by new one provided by <mildew@gmail.com>
  option -c added

* Mon Jul 17 2006 Radek Vokal <rvokal@redhat.com> - 20020927-39
- rebuilt

* Mon Jul 10 2006 Radek Vokal <rvokal@redhat.com> - 20020927-38
- tracepath doesn't continue past destination host (#174032) <mildew@gmail.com>

* Wed Mar 29 2006 Radek Vokál <rvokal@redhat.com> - 20020927-37
- fix ifenslave, shows interface addresses
- add RPM_OPT_FLAGS to ifenslave
 
* Sun Mar 12 2006 Radek Vokál <rvokal@redhat.com> - 20020927-36
- fix ifenslave man page (#185223)

* Fri Feb 24 2006 Radek Vokál <rvokal@redhat.com> - 20020927-35
- add PreReq: chkconfig (#182799,#182798)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 20020927-34.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 20020927-34.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Radek Vokál <rvokal@redhat.com> 20020927-34
- ping clean-up, added new ICMP warning messages

* Wed Jan 25 2006 Radek Vokál <rvokal@redhat.com> 20020927-33
- gcc patch, warnings cleaned-up

* Tue Dec 13 2005 Radek Vokal <rvokal@redhat.com> 20020927-32
- fix HOPLIMIT option for setsockopt() (#175471)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec 02 2005 Radek Vokal <rvokal@redhat.com> 20020927-31
- ifenslave.8 from debian.org
- separate ifenslave to its own tarball

* Tue Nov 08 2005 Radek Vokal <rvokal@redhat.com> 20020927-30
- don't ship traceroute6, now part of traceroute package

* Wed Oct 05 2005 Radek Vokal <rvokal@redhat.com> 20020927-29
- add ping6 and tracepath6 manpages, fix attributes. 

* Fri Sep 30 2005 Radek Vokal <rvokal@redhat.com> 20020927-28
- memset structure before using it (#168166)

* Mon Sep 26 2005 Radek Vokal <rvokal@redhat.com> 20020927-27
- fixed ping -f, flooding works again (#134859,#169141)

* Thu Sep 08 2005 Radek Vokal <rvokal@redhat.com> 20020927-26
- tracepath6 and tracepath fix, use getaddrinfo instead of gethostbyname(2) 
  (#100778,#167735)

* Fri Aug 12 2005 Radek Vokal <rvokal@redhat.com> 20020927-25
- fixed arping timeout (#165715)

* Mon Jul 18 2005 Radek Vokal <rvokal@redhat.com> 20020927-24
- fixed arping buffer overflow (#163383)

* Fri May 27 2005 Radek Vokal <rvokal@redhat.com> 20020927-23
- fixed un-initialized "device" (#158914)

* Thu Apr 07 2005 Radek Vokal <rvokal@redhat.com> 20020927-22
- don't start rdisc as default (#154075)

* Tue Apr 05 2005 Radek Vokal <rvokal@redhat.com> 20020927-21
- rdisc init script added (#151614)

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 20020927-20
- arping fix for infiniband (#150156)

* Tue Dec 07 2004 Radek Vokal <rvokal@redhat.com> 20020927-19
- return values fixed - patch from suse.de

* Mon Oct 18 2004 Radek Vokal <rvokal@redhat.com>
- ifenslave.c and README.bonding updated from kernel-2.6.8-1.521 (#136059)

* Mon Oct 11 2004 Radek Vokal <rvokal@redhat.com>
- spec file updated, source fixed (#135193)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 12 2004 Phil Knirsch <pknirsch@redhat.com> 20020927-15
- Updated rh patch to enable PIE build of binaries.

* Thu Apr 22 2004 Phil Knirsch <pknirsch@redhat.com> 20020927-14
- Fixed bug with wrong return code check of inet_pton() in traceroute6 (#100684)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Oct 02 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-12
- Fixed unaligned access problem on ia64 (#101417)

* Wed Sep 10 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-11
- Don't use own headers, use glibc and kernheaders.

* Thu Sep 04 2003 Bill Nottingham <notting@redhat.com> 20020927-10
- fix build with new glibc-kernheaders

* Wed Sep 03 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-9.1
- rebuilt

* Wed Sep 03 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-9
- Start icmp_seq from 0 instead of 1 (Conform with debian and Solaris #100609).

* Thu Jul 31 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-8
- One more update to ifenslave.c

* Mon Jun 16 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-7
- Updated ifenslave.c and README.bonding to latest version.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 15 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-5
- Bumped release and rebuilt

* Thu May 15 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-4
- Fixed DNS lookup problems (#68212).
- Added warning if binding problem failed on subinterface (#81640).

* Tue May 13 2003 Phil Knirsch <pknirsch@redhat.com> 20020927-3
- Removed bonding tarball and replaced it with ifenslave.c and README
- FHS compliance for all tools, now to be found in /bin with compat symlinks to
  old places.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 20020927-2
- rebuilt

* Fri Nov 29 2002 Phil Knirsch <pknirsch@redhat.com> 20020927-1
- Updated to latest upstream version.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 20020124-8
- automated rebuild

* Tue Jun 18 2002 Phil Knirsch <pknirsch@redhat.com> 20020124-7
- Added new BuildPreReqs for docbook-utils and perl-SGMLSpm (#66661)
- Fixed ipv6 error printing problem (#66659).

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Phil Knirsch <pknirsch@redhat.com>
- Added a patch to activate the rdisc server (#64270).
- Display the countermeasures warning only in verbose (#55236)

* Thu Apr 18 2002 Bill Nottingham <notting@redhat.com>
- quit trying to build HTML versions of the man pages

* Thu Mar 14 2002 Phil Knirsch <pknirsch@redhat.com>
- Added fix by Tom "spot" Callaway to fix buffer overflow problems in stats.

* Wed Feb 27 2002 Phil Knirsch <pknirsch@redhat.com>
- Update to iputils-ss020124.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Aug 27 2001 Philipp Knirsch <pknirsch@redhat.de> 20001110-6
- Fixed buffer overflow problem in traceroute6.c (#51135)

* Mon Jul 01 2001 Philipp Knirsch <pknirsch@redhat.de>
- Made ping6 and traceroute6 setuid (safe as they drop it VERY early) (#46769)

* Thu Jun 28 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed ping statistics overflow bug (#43801)

* Tue Jun 26 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed a bunch of compiler warnings (#37131)
- Fixed wrong exit code for no packets and deadline (#40323)
- Moved arping to /sbin from /usr/sbin due to ifup call (#45785). Symlink from
  /usr/sbin/ provided for backwards compatibility.

* Mon Apr 30 2001 Preston Brown <pbrown@redhat.com>
- install in.rdisc.8c as rdisc.8

* Tue Jan 16 2001 Jeff Johnson <jbj@redhat.com>
- update to ss001110
- doco fixes (#23844).

* Sun Oct  8 2000 Jeff Johnson <jbj@redhat.com>
- update to ss001007.

* Tue Aug  8 2000 Tim Waugh <twaugh@redhat.com>
- fix spelling mistake (#15714).

* Tue Aug  8 2000 Tim Waugh <twaugh@redhat.com>
- turn on -U on machines without TSC (#15223).

* Tue Aug  1 2000 Jeff Johnson <jbj@redhat.com>
- better doco patch (#15050).

* Tue Jul 25 2000 Jakub Jelinek <jakub@redhat.com>
- fix include-glibc/ to work with new glibc 2.2 resolver headers

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to ss000418.
- perform reverse DNS lookup only once for same input.

* Sun Mar  5 2000 Jeff Johnson <jbj@redhat.com>
- include README.ifenslave doco.
- "ping -i N" was broke for N >= 3 (#9929).
- update to ss000121:
-- clockdiff: preserve raw socket errno.
-- ping: change error exit code to 1 (used to be 92,93, ...)
-- ping,ping6: if -w specified, transmit until -c limit is reached.
-- ping,ping6: exit code non-zero if some packets not received within deadline.

* Tue Feb 22 2000 Jeff Johnson <jbj@redhat.com>
- man page corrections (#9690).

* Wed Feb  9 2000 Jeff Johnson <jbj@jbj.org>
- add ifenslave.

* Thu Feb  3 2000 Elliot Lee <sopwith@redhat.com>
- List /usr/sbin/rdisc in %%files list.

* Thu Jan 27 2000 Jeff Johnson <jbj@redhat.com>
- add remaining binaries.
- casts to remove compilation warnings.
- terminate if -w deadline is reached exactly (#8724).

* Fri Dec 24 1999 Jeff Johnson <jbj@redhat.com>
- create (only ping for now, traceroute et al soon).
