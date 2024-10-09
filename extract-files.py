#
# Copyright (C) 2024 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

from typing import List

from extract_utils.main import ExtractUtilsModule

from extract_utils.fixups_blob import (
    blob_fixups_user_type,
    blob_fixup,
)

from extract_utils.fixups_lib import (
    lib_fixups_user_type,
    lib_fixup_vendorcompat,
    libs_proto_3_9_1,
)

namespace_imports = [
    'hardware/qcom-caf/sm8550',
    'hardware/qcom-caf/wlan',
    'hardware/sony',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
    'vendor/sony/pdx234',
]


libs_add_vendor_suffix = (
    'vendor.qti.hardware.fm@1.0',
    'vendor.qti.hardware.data.cne.internal.api@1.0',
    'vendor.qti.hardware.data.cne.internal.constants@1.0',
    'vendor.qti.hardware.data.cne.internal.server@1.0',
    'vendor.qti.hardware.data.connection@1.0',
    'vendor.qti.hardware.data.connection@1.1',
    'vendor.qti.hardware.data.dynamicdds@1.0',
    'vendor.qti.hardware.data.iwlan@1.0',
    'vendor.qti.hardware.data.qmi@1.0',
    'com.qualcomm.qti.dpm.api@1.0',
    'vendor.qti.hardware.dpmservice@1.0',
    'vendor.qti.diaghal@1.0',
    'vendor.qti.imsrtpservice@3.0',
    'vendor.qti.imsrtpservice@3.1',
    'vendor.qti.hardware.qccsyshal@1.0',
    'vendor.qti.hardware.qccsyshal@1.1',
    'vendor.qti.hardware.qccsyshal@1.2',
    'vendor.qti.hardware.qccvndhal@1.0',
    'vendor.qti.hardware.wifidisplaysession@1.0',
)

libs_remove = (
    'libwpa_client',
    'libwfdaac_vendor',
    'libagmclient',
    'libpalclient',
    'libc++abi',
)


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    if partition != 'vendor':
        return None

    return f'{lib}_{partition}'


def lib_fixup_remove(lib: str, partition: str, *args, **kwargs):
    return ''


lib_fixups: lib_fixups_user_type = {
    libs_proto_3_9_1: lib_fixup_vendorcompat,
    libs_add_vendor_suffix: lib_fixup_vendor_suffix,
    libs_remove: lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/bin/hw/android.hardware.security.keymint-service-qti',
        'vendor/bin/hw/vendor.semc.hardware.secd@1.1-service',
        'vendor/bin/keyprovd',
        'vendor/lib64/libqtikeymint.so',
        'vendor/lib64/librkp.so',
    ): blob_fixup()
    .add_needed(
        'android.hardware.security.rkp-V3-ndk.so'
    ),
    'vendor/bin/slim_daemon': blob_fixup()
    .add_needed(
        'libc++_shared.so',
    ),
    'vendor/etc/msm_irqbalance.conf': blob_fixup()
    .regex_replace(
        'IGNORED_IRQ=27,23,38', 'IGNORED_IRQ=27,23,38,115,332'
    ),
    'vendor/etc/seccomp_policy/qwesd@2.0.policy': blob_fixup()
    .add_line_if_missing(
        'pipe2: 1'
    ),
    'system_ext/lib64/libwfdservice.so': blob_fixup()
    .replace_needed(
        'android.media.audio.common.types-V2-cpp.so', 'android.media.audio.common.types-V3-cpp.so'
    ),
}


module = ExtractUtilsModule(
    'sm8550-common',
    'sony',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
)
