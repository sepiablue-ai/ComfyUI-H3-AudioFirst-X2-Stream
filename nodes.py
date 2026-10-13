# SPDX-License-Identifier: GPL-3.0-only
"""Audio-first MiniMax H3: finish the voice on a 32x32 pass, then lock it for the 022 video pass."""
import logging

import torch

import node_helpers
from comfy.nested_tensor import NestedTensor
from comfy_extras.nodes_minimax_h3 import _empty_av_latent, _resize

log = logging.getLogger(__name__)
CATEGORY = "H3 AudioFirst X2 Stream"
AUDIO_CANVAS = 32
LOCK_TOLERANCE = 2e-5


def audio_tensor(latent):
    samples = latent["samples"]
    return samples.tensors[1] if samples.is_nested else samples


class H3AudioFirstConditioning:
    """Reuse the full-resolution text/image conditioning with a 32x32 keyframe for the audio pass."""

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "positive": ("CONDITIONING",), "image": ("IMAGE",), "vae": ("VAE",),
            "length": ("INT", {"default": 124, "min": 5, "max": 3600,
                               "tooltip": "Use the same frame count as the video pass"}),
        }}

    RETURN_TYPES = ("CONDITIONING", "LATENT")
    RETURN_NAMES = ("audio_positive", "audio_latent")
    FUNCTION = "prepare"
    CATEGORY = CATEGORY
    DESCRIPTION = "Prepare the 32x32 audio pass from the existing H3 conditioning. The text encoder is not run again."

    def prepare(self, positive, image, vae, length):
        latent, _ = _empty_av_latent(AUDIO_CANVAS, AUDIO_CANVAS, length)
        keyframe = {"resolved_frame_index": 0,
                    "latent": vae.encode(_resize(image[:1], AUDIO_CANVAS, AUDIO_CANVAS, "disabled"))}
        conditioning = node_helpers.conditioning_set_values(positive, {"minimax_keyframes": [keyframe]})
        return (conditioning, latent)


class H3AudioFirstLockAudio:
    """Insert the finished audio latent into the video-pass latent and exclude it from denoising."""

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"video_latent": ("LATENT",), "audio_latent": ("LATENT",)}}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "lock"
    CATEGORY = CATEGORY
    DESCRIPTION = "Connect the empty video-pass latent and the finished audio-pass output."

    def lock(self, video_latent, audio_latent):
        video, empty_audio = video_latent["samples"].tensors
        audio = audio_tensor(audio_latent).to(empty_audio).clone()
        if audio.shape != empty_audio.shape:
            raise ValueError(f"Audio shape {tuple(audio.shape)} does not match the video pass {tuple(empty_audio.shape)}; "
                             "use the same frame count in both passes")
        result = video_latent.copy()
        result["samples"] = NestedTensor([video, audio])
        result["noise_mask"] = NestedTensor([
            torch.ones((video.shape[0], 1, *video.shape[2:]), dtype=torch.float32, device=video.device),
            torch.zeros((audio.shape[0], 1, *audio.shape[2:]), dtype=torch.float32, device=audio.device),
        ])
        return (result,)


class H3AudioFirstCheckLock:
    """Stop before saving if the video pass changed the locked audio latent."""

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"samples": ("LATENT",), "audio_latent": ("LATENT",)}}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "check"
    CATEGORY = CATEGORY
    DESCRIPTION = "Pass the video-pass result through after confirming its audio still equals the audio pass."

    def check(self, samples, audio_latent):
        actual = samples["samples"].tensors[1].detach().cpu().float()
        expected = audio_tensor(audio_latent).detach().cpu().float()
        if actual.shape != expected.shape or not bool(torch.isfinite(actual).all()):
            raise ValueError("Locked audio has a different shape or non-finite values")
        difference = float((actual - expected).abs().max())
        if difference > LOCK_TOLERANCE:
            raise ValueError(f"Audio lock changed the audio latent (max abs diff {difference:.3g})")
        log.info("[H3 AudioFirst] Audio lock preserved (max abs diff %.3g)", difference)
        return (samples,)
