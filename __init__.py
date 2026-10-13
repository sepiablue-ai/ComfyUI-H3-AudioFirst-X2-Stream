# SPDX-License-Identifier: GPL-3.0-only
"""MiniMax H3 audio-first two-pass generation with X2 streaming output."""
from .nodes import H3AudioFirstCheckLock, H3AudioFirstConditioning, H3AudioFirstLockAudio

NODE_CLASS_MAPPINGS = {
    "H3AudioFirstConditioning": H3AudioFirstConditioning,
    "H3AudioFirstLockAudio": H3AudioFirstLockAudio,
    "H3AudioFirstCheckLock": H3AudioFirstCheckLock,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "H3AudioFirstConditioning": "H3 AudioFirst 32x32 Audio Conditioning",
    "H3AudioFirstLockAudio": "H3 AudioFirst Lock Audio",
    "H3AudioFirstCheckLock": "H3 AudioFirst Check Audio Lock",
}
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
