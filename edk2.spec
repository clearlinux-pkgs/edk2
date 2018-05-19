%define ovmf_tag vUDK2018
%define target_arch X64
%define openssl_version 1.1.0h
%define openssl_dir CryptoPkg/Library/OpensslLib/openssl

Name:       edk2
Version:    2
Release:    8
Summary:    EFI Development Kit II

Group:      Applications/Emulators
License:    BSD-2-Clause
URL:        http://www.tianocore.org/edk2/
Source0:    https://github.com/tianocore/edk2/archive/vUDK2018.tar.gz
Source1:    https://www.openssl.org/source/openssl-1.1.0h.tar.gz
Patch1:     0001-disabling-features-to-reduce-OVMF.fd-boot-time.patch
Patch2:     0002-Remove-Werror-option-from-flags.patch

BuildRequires:  python
BuildRequires:  util-linux-dev
BuildRequires:  gcc
BuildRequires:  acpica-unix2
BuildRequires:  nasm
BuildRequires:  dosfstools

Provides: clr-ovmf-bin
Obsoletes: clr-ovmf-bin
Provides: clr-ovmf-bin-data
Obsoletes: clr-ovmf-bin-data

%description
EFI Development Kit II
UEFI Firmware

%prep
%setup -q -n %{name}-%{ovmf_tag}
%patch1 -p1
%patch2 -p1
mkdir -p %{openssl_dir}
tar -C %{openssl_dir} --strip 1 -xf %{SOURCE1}

%build
export SOURCE_DATE_EPOCH=1526707454
cd OvmfPkg/
./build.sh -a %{target_arch} -D SECURE_BOOT_ENABLE

%install
export SOURCE_DATE_EPOCH=1526707454
mkdir -p %{buildroot}/usr/share/qemu
cp Build/Ovmf%{target_arch}/DEBUG_GCC*/FV/OVMF.fd %{buildroot}/usr/share/qemu/OVMF.fd
cp Build/Ovmf%{target_arch}/DEBUG_GCC*/FV/OVMF_CODE.fd %{buildroot}/usr/share/qemu/OVMF_CODE.fd
cp Build/Ovmf%{target_arch}/DEBUG_GCC*/FV/OVMF_VARS.fd %{buildroot}/usr/share/qemu/OVMF_VARS.fd

%files
%defattr(-,root,root,-)
/usr/share/qemu/OVMF.fd
/usr/share/qemu/OVMF_CODE.fd
/usr/share/qemu/OVMF_VARS.fd
