# Copyright (C) 2009 The Android Open Source Project
# Copyright (C) 2019 The Mokee Open Source Project
# Copyright (C) 2019 The LineageOS Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import common

def FullOTA_InstallBegin(info):
  info.script.AppendExtra("ifelse(is_mounted(\"/apex\"), unmount(\"/apex\"));")
  return

def FullOTA_InstallEnd(info):
  OTA_InstallEnd(info, False)

def IncrementalOTA_InstallEnd(info):
  OTA_InstallEnd(info, True)

def AddImageOnly(info, basename, incremental, firmware):
  if incremental:
    input_zip = info.source_zip
  else:
    input_zip = info.input_zip
  if firmware:
    data = input_zip.read("RADIO/" + basename)
  else:
    data = input_zip.read("IMAGES/" + basename)
  common.ZipWriteStr(info.output_zip, basename, data)

def AddImage(info, basename, dest, incremental):
  AddImageOnly(info, basename, incremental, False)
  info.script.Print("Patching {} image unconditionally...".format(dest.split('/')[-1]))
  info.script.AppendExtra('package_extract_file("%s", "%s");' % (basename, dest))

def OTA_InstallEnd(info, incremental):
  AddImage(info, "vbmeta.img", "/dev/block/by-name/vbmeta", incremental)
  AddImage(info, "vbmeta_system.img", "/dev/block/by-name/vbmeta_system", incremental)
  AddImage(info, "vbmeta_vendor.img", "/dev/block/by-name/vbmeta_vendor", incremental)
  AddImage(info, "dtbo.img", "/dev/block/by-name/dtbo", incremental)

  bin_map = {
      'lk': ['lk'],
      'lk2': ['lk2'],
      'audio_dsp': ['audio_dsp'],
      'boot_para': ['boot_para'],
      'cam_vpu1': ['cam_vpu1'],
      'cam_vpu2': ['cam_vpu2'],
      'cam_vpu3': ['cam_vpu3'],
      'cdt_engineering': ['cdt_engineering'],
      'dpm_1': ['dpm_1'],
      'dpm_2': ['dpm_2'],
      'expdb': ['expdb'],
      'flashinfo': ['flashinfo'],
      'gpt': ['gpt'],
      'gpt_backup': ['gpt_backup'],
      'gz1': ['gz1'],
      'gz2': ['gz2'],
      'logo': ['logo'],
      'mcupm_1': ['mcupm_1'],
      'mcupm_2': ['mcupm_2'],
      'md1img': ['md1img'],
      'metadata': ['metadata'],
      'misc': ['misc'],
      'ocdt': ['ocdt'],
      'oplus_custom': ['oplus_custom'],
      'oplusreserve1': ['oplusreserve1'],
      'oplusreserve2': ['oplusreserve2'],
      'oplusreserve3': ['oplusreserve3'],
      'oplusreserve5': ['oplusreserve5'],
      'oplusreserve6': ['oplusreserve6'],
      'otp': ['otp'],
      'para': ['para'],
      'param': ['param'],
      'pi_img': ['pi_img'],
      'scp1': ['scp1'],
      'scp2': ['scp2'],
      'sec1': ['sec1'],
      'spmfw': ['spmfw'],
      'sspm_1': ['sspm_1'],
      'sspm_2': ['sspm_2'],
      'tee1': ['tee1'],
      'tee2': ['tee2'],
      'vendor_boot': ['vendor_boot']
  }

  pl = 'preloader'
  pl_part = ['sda', 'sdb']

  fw_cmd = 'ui_print("Patching radio images unconditionally...");\n'

  AddImageOnly(info, "{}.img".format(pl), incremental, True)
  for part in pl_part:
      fw_cmd += 'package_extract_file("{}.img", "/dev/block/{}");\n'.format(pl, part)

  for _bin in bin_map.keys():
    AddImageOnly(info, '{}.bin'.format(_bin), incremental, True)
    for part in bin_map[_bin]:
      fw_cmd += 'package_extract_file("{}.bin", "/dev/block/by-name/{}");\n'.format(_bin, part)

  # Radio
  fw_cmd += 'package_extract_file("md1img.img", "/dev/block/by-name/md1img");\n'

  info.script.AppendExtra(fw_cmd)
