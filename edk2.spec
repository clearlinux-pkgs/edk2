%define ovmf_tag vUDK2017
%define target_arch X64
%define openssl_version 1.1.0f

Name:       edk2
Version:    2
Release:    1
Summary:    EFI Development Kit II

Group:      Applications/Emulators
License:    BSD-2-Clause
URL:        http://www.tianocore.org/edk2/
Source0:    https://github.com/tianocore/edk2/archive/%{ovmf_tag}.tar.gz
Source1:    https://www.openssl.org/source/openssl-%{openssl_version}.tar.gz
Patch1:     0001-disabling-features-to-reduce-OVMF.fd-boot-time.patch

BuildRequires:  python
BuildRequires:  util-linux-dev
BuildRequires:  gcc
BuildRequires:  acpica-unix2
BuildRequires:  nasm
BuildRequires:  dosfstools

%description
EFI Development Kit II
AARCH64 UEFI Firmware

%prep
%setup -q -n %{name}-%{ovmf_tag}
%patch1 -p1
tar -C CryptoPkg/Library/OpensslLib -xf %{SOURCE1}
(cd CryptoPkg/Library/OpensslLib;
 mv openssl-* openssl)

%build
export SOURCE_DATE_EPOCH=1500666186
cd OvmfPkg/
./build.sh -a %{target_arch} -D SECURE_BOOT_ENABLE

%install
export SOURCE_DATE_EPOCH=1500666186
mkdir -p %{buildroot}/usr/share/qemu
cp Build/Ovmf%{target_arch}/DEBUG_GCC*/FV/OVMF.fd %{buildroot}/usr/share/qemu/OVMF.fd

%files
%defattr(-,root,root,-)
/usr/share/qemu/OVMF.fd
