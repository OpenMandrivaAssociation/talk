Summary:	Talk client for one-on-one Internet chatting
Name:		talk
Version:	0.17
Release:	%mkrel 15
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

