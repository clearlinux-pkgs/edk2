%define ovmf_tag edk2-stable202011
%define target_arch X64
%define openssl_version 1.1.1i
%define openssl_dir CryptoPkg/Library/OpensslLib/openssl
%define brotli_version 1.0.7
%define brotli_compress_dir BaseTools/Source/C/BrotliCompress/brotli
%define brotli_decompress_dir MdeModulePkg/Library/BrotliCustomDecompressLib/brotli

Name     : edk2
Version  : 202011
Release  : 18
URL      : http://www.tianocore.org/edk2/
Source0  : https://github.com/tianocore/edk2/archive/edk2-stable202011.tar.gz
Source1  : https://www.openssl.org/source/openssl-1.1.1i.tar.gz
Source2  : https://github.com/google/brotli/archive/v1.0.7/brotli-1.0.7.tar.gz
Summary  : EFI Development Kit II
Group    : Applications/Emulators
License  : BSD-2-Clause
BuildRequires: acpica-unix2
BuildRequires: bc
BuildRequires: dosfstools
BuildRequires: gcc
BuildRequires: nasm
BuildRequires: python3
BuildRequires: util-linux-dev
Patch1: 0001-Remove-Werror-option-from-flags.patch

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
mkdir -p %{openssl_dir}
tar -C %{openssl_dir} --strip 1 -xf %{SOURCE1}
mkdir -p %{brotli_compress_dir}
tar -C %{brotli_compress_dir} --strip 1 -xf %{SOURCE2}
mkdir -p %{brotli_decompress_dir}
tar -C %{brotli_decompress_dir} --strip 1 -xf %{SOURCE2}

%build
export SOURCE_DATE_EPOCH=1526707454
cd OvmfPkg/
./build.sh -a %{target_arch} -D SECURE_BOOT_ENABLE -b RELEASE

%install
export SOURCE_DATE_EPOCH=1526707454
mkdir -p %{buildroot}/usr/share/qemu
cp Build/Ovmf%{target_arch}/RELEASE_GCC*/FV/OVMF.fd %{buildroot}/usr/share/qemu/OVMF.fd
cp Build/Ovmf%{target_arch}/RELEASE_GCC*/FV/OVMF_CODE.fd %{buildroot}/usr/share/qemu/OVMF_CODE.fd
cp Build/Ovmf%{target_arch}/RELEASE_GCC*/FV/OVMF_VARS.fd %{buildroot}/usr/share/qemu/OVMF_VARS.fd

%files
%defattr(-,root,root,-)
/usr/share/qemu/OVMF.fd
/usr/share/qemu/OVMF_CODE.fd
/usr/share/qemu/OVMF_VARS.fd
