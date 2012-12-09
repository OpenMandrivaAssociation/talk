Summary:	Talk client for one-on-one Internet chatting
Name:		talk
Version:	0.17
Release:	%mkrel 21
License:	BSD
Group:		Networking/Chat  
Source0:	ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/netkit-ntalk-%{version}.tar.gz
Source1:	talk-xinetd
Source2:	ntalk-xinetd
Patch0:		netkit-ntalk-0.17-pre20000412-time.patch
Patch1:		netkit-ntalk-0.17-strip.patch
Patch2:		netkit-ntalk-0.17-sockopt.patch
Patch3:		netkit-ntalk-0.17-i18n.patch
Patch4:		netkit-ntalk-0.17-resize.patch
Patch5:		netkit-ntalk-0.17-fix-dos-condition.patch
Patch6:		netkit-ntalk-0.17-man-ln.patch
BuildRequires:	ncurses-devel
Obsoletes:	ntalk
Provides:	ntalk
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The talk package provides client and daemon programs for the Internet
talk protocol, which allows you to chat with other users on different
systems.  Talk is a communication program which copies lines from one
terminal to the terminal of another user.

Install talk if you'd like to use talk for chatting with users on
different systems.

%package	server
Group:		System/Servers
Summary:	Server for the talk program
Obsoletes:	ntalk
Requires:	xinetd

%description	server
The talk-server package provides daemon programs for the Internet talk
protocol, which allows you to chat with other users on different
machines.  Talk is a communication program which copies lines from one
terminal to the terminal of another user.

%prep
%setup -q -n netkit-ntalk-%{version}
%patch0 -p1 -b .time
%patch1 -p1 -b .strip
%patch2 -p1 -b .sockopt
%patch3 -p1 -b .i18n
%patch4 -p1 -b .resize
%patch5 -p1 -b .dos
%patch6 -p0 -b .man

cp %{SOURCE1} talk.xinetd
cp %{SOURCE2} ntalk.xinetd

%build
sh configure
perl -pi -e '
    s,^CC=.*$,CC=cc,;
    s,-O2,\$(RPM_OPT_FLAGS) -D_GNU_SOURCE,;
    s,^BINDIR=.*$,BINDIR=%{_bindir},;
    s,^MANDIR=.*$,MANDIR=%{_mandir},;
    s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
    ' MCONFIG

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/xinetd.d
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man8

make INSTALLROOT=%{buildroot} install MANDIR=%{_mandir}

install -m0644 talk.xinetd %{buildroot}%{_sysconfdir}/xinetd.d/talk
install -m0644 ntalk.xinetd %{buildroot}%{_sysconfdir}/xinetd.d/ntalk

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/talk
%{_mandir}/man1/talk.1*

%files server
%defattr(-,root,root)
%config (noreplace) %{_sysconfdir}/xinetd.d/*
%attr(0711,root,root)%{_sbindir}/in.ntalkd
%{_sbindir}/in.talkd
%{_mandir}/man8/in.ntalkd.8*
%{_mandir}/man8/in.talkd.8*
%{_mandir}/man8/ntalkd.8*
%{_mandir}/man8/talkd.8*


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.17-21mdv2011.0
+ Revision: 670663
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.17-20mdv2011.0
+ Revision: 607971
- rebuild

* Sat Jan 30 2010 Funda Wang <fwang@mandriva.org> 0.17-19mdv2010.1
+ Revision: 498424
- finally fix file list
- fix file list

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 0.17-18mdv2009.1
+ Revision: 318032
- rebuild
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

* Mon Apr 21 2008 Oden Eriksson <oeriksson@mandriva.com> 0.17-15mdv2009.0
+ Revision: 196210
- fix build
- sync with fc9

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.17-14mdv2008.1
+ Revision: 179621
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Aug 29 2007 Oden Eriksson <oeriksson@mandriva.com> 0.17-13mdv2008.0
+ Revision: 73369
- Import talk



* Mon Sep 18 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.17-13mdv2007.0
- Rebuild

* Wed Jun 07 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.17-12mdv2007.0
- rebuild

* Tue Jan 31 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.17-11mdk
- %%mkrel
- fix DoS condition in talkd (P4 from vdanen)
- from fedora:
	o patch to handle input in UTF-8 from Miloslav Trmac (#143818) (P3)

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.17-10mdk
- Rebuild

* Fri Dec 24 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.17-9mdk
- sync with fedora patches
- no .bz2 ending for man pages in %%files list
- fix summary-ended-with-dot
- cosmetics

* Sun Jun 15 2003 Stefan van der Eijk <stefan@eijk.nu> 0.17-8mdk
- BuildRequires

* Wed Apr  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.17-7mdk
- Rebuild to handle biarch struct utmp on hammer, though talkd doesn't
  use the ut_ fields that changed

* Fri Apr 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.17-6mdk
- Upgrade description.
- talk-server depend of xinetd.
- More glibc2.2 fix.
- Fix xinetd entry.
- Update to the last pre20000412 to get it works.

* Mon Mar 12 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.17-5mdk
- fix build on glibc 2.2.2 strict headers

* Thu Dec 28 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.17-4mdk
- stream for talk protocol.

* Sat Sep 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.17-3mdk
- Fix xinetd support.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.17-2mdk
- automatically added BuildRequires

* Tue Aug 01 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.17-1mdk
- new version

* Wed Jul 26 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.16-2mdk
- fix silly problem with xinetd files

* Sat Jul 22 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 0.16-1mdk
- much needed update to 0.16
- use sbindir macro (thierry sucks)
- make daemons -rwx--x--x (rawhide)
- xinetd move

* Fri Jul 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.11-5mdk
- macros, BM, _spechelper_

* Thu Mar 23 2000 Daouda Lo <daouda@mandrakesoft.com> 0.11-4mdk
- fix group for release 7.1

* Wed Nov 03 1999 Jerome Martin <jerome@mandrakesoft.com>
- Rebuild for new distribution
- Minor Specfile cleanup

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Fri Apr 09 1999 Jeff Johnson <jbj@redhat.com>
- update to multi-homed 0.11 version.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 14 1998 Erik Troan <ewt@redhat.com>
- built against new ncurses

* Tue Jul 15 1997 Erik Troan <ewt@redhat.com>
- initial build
