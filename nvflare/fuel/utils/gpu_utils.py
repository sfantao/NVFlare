# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
# Modifications Copyright (c) 2025 Advanced Micro Devices, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import amdsmi
from typing import List

_is_amdsmi_initialized = False
_handles = []
def _get_handles():
    if not _is_amdsmi_initialized:
        amdsmi.amdsmi_init()
        _handles = amdsmi.amdsmi_get_processor_handles()
    return _handles

def get_host_gpu_memory_total(unit="MiB") -> List:
    assert unit=="MiB", "Only MiB supported"
    res = [int(amdsmi.amdsmi_get_gpu_memory_total(h, amdsmi.amdsmi_interface.AmdSmiMemoryType.VRAM)) // (1024*1024) for h in _get_handles()]
    return res

def get_host_gpu_memory_free(unit="MiB") -> List:
    assert unit=="MiB", "Only MiB supported"

    total = get_host_gpu_memory_total(unit)
    used = [int(amdsmi.amdsmi_get_gpu_memory_usage(h, amdsmi.amdsmi_interface.AmdSmiMemoryType.VRAM)) // (1024*1024) for h in _get_handles()]
    free = [t - u for t, u in zip(total, used)]
    return free

def get_host_gpu_ids() -> List:
    return [x for x, _ in enumerate(_get_handles())]
