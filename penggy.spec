%define name penggy
%define version 0.2.1
%define release %mkrel 5

Summary:	UNIX client for AOL
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Networking/Remote access
License:	GPL
URL:		http://peng.apinc.org
Source:		http://download.penggy.org/sources/%{name}-%{version}.tar.bz2
Patch0:		penggy-modem.patch.bz2
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	guile-devel

%description
Penggy is a free UNIX client for AOL. It allows UNIX users to connect
to the Internet using AOL, through an IP tunneling system.

%prep
rm -rf $RPM_BUILD_ROOT
%setup

%patch0 -p1

%build
%configure --target="" --enable-dsl --enable-flap --enable-cable

%make

%install
%makeinstall
%find_lang %{name}

%post
# script for launch of tun. Important, tun is available as module with mdk9.0
# launch tun if it is'nt still
if ! (lsmod | grep -q tun) then
  echo "Launching tun."; modprobe tun; result=$?
  if [ "$result" ]; then
    echo "Error launching tun !"
  fi
else
  echo "Tun module is still running."
fi
# initialise launching of tun at boot time
if ! (grep -q tun -r /etc/modules) then
  echo "Adding tun in /etc/modules ."
  echo tun >> /etc/modules
else
  echo "Tun already in /etc/modules, nothing to do."
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%{_sbindir}/%{name}
%{_datadir}/%{name}/chat/*
%defattr(-,root,root,0755)
%doc COPYING DISCLAIMER INSTALL README TODO
%config(noreplace) %{_sysconfdir}/%{name}/*

