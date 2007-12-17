%define	_snapshot	-pre20000412

Summary:	Talk client for one-on-one Internet chatting
Name:		talk
Version:	0.17
Release:	%mkrel 13
License:	BSD
Group:		Networking/Chat  
BuildRequires:	ncurses-devel
Obsoletes:	ntalk
Provides:	ntalk

Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/chat/netkit-ntalk-%{version}%{_snapshot}.tar.bz2
Source1:	talk-xinetd
Source2:	ntalk-xinetd
Patch0:		netkit-ntalk-0.17-pre20000412-time.patch.bz2
Patch1:		netkit-ntalk-0.17-strip.patch.bz2
Patch2:		netkit-ntalk-0.17-sockopt.patch.bz2
Patch3:		netkit-ntalk-0.17-i18n.patch.bz2
Patch4:		netkit-ntalk-0.17-fix-dos-condition.patch.bz2

%package	server
Group:		System/Servers
Summary:	Server for the talk program
Obsoletes:	ntalk
Requires:	xinetd

%description
The talk package provides client and daemon programs for the Internet
talk protocol, which allows you to chat with other users on different
systems.  Talk is a communication program which copies lines from one
terminal to the terminal of another user.

Install talk if you'd like to use talk for chatting with users on
different systems.

%description	server
The talk-server package provides daemon programs for the Internet talk
protocol, which allows you to chat with other users on different
machines.  Talk is a communication program which copies lines from one
terminal to the terminal of another user.

%prep
%setup -q -n netkit-ntalk-%{version}%{_snapshot}
%patch0 -p1 -b .glibc22
%patch1 -p1 -b .strip
%patch2 -p1 -b .sockopt
%patch3 -p1 -b .i18n
%patch4 -p1 -b .dos

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
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}}

make INSTALLROOT=$RPM_BUILD_ROOT install MANDIR=%{_mandir}

install -m644 %{SOURCE1} -D $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/talk
install -m644 %{SOURCE2} -D $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/ntalk

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/talk
%{_mandir}/man1/talk.1*

%files server
%defattr(-,root,root)
%attr(0711,root,root)%{_sbindir}/in.ntalkd
%{_sbindir}/in.talkd
%{_mandir}/man8/in.ntalkd.8*
%{_mandir}/man8/in.talkd.8*
%{_mandir}/man8/ntalkd.8*
%{_mandir}/man8/talkd.8*
%config (noreplace) %{_sysconfdir}/xinetd.d/*
