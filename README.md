# ComfyUI H3 AudioFirst X2 Stream

English | [日本語](README_ja.md)

**ComfyUI nodes that reduce the "talking inside a metal pipe" voice of fast MiniMax H3 settings. The fast (LBH) variant improves the audio and is still faster than before.**

Measured on an RTX 4070 12 GB, 1088 × 1920 video with audio:

| 14 s dialogue video | Generation time | Audio |
|---|---:|---|
| Before (X2 Stream 4-step) | 153.8 s (2 min 33.8 s) | Often metallic |
| AudioFirst standard | 165.1 s (2 min 45.1 s) | Improved |
| **AudioFirst fast (LBH)** | **125.7 s (2 min 5.7 s)** | **Improved** |

- **About 18% faster, with better audio**: 14 s dialogue, 153.8 s → 125.7 s (-28.1 s).
- **About 20% faster in a same-session comparison**: 14 s singing with guitar (640 × 928), 172.1 s before → 137.9 s fast.
- **No slower at 5 s**: the fast variant takes 60.0 s, about the same as before (about 60.8 s), with better audio.
- **Standard keeps the picture unchanged**: the video pass is identical to before; only the audio is replaced (about 11 s added).
- **New speed mode, about 22% faster than fast with the same audio**: 14 s, 131.9 s → 102.9 s in a same-session comparison; 5 s takes 57.3 s and 10 s 77.5 s. See [Speed mode](#speed-mode).

"Before" is the 4-step FL2VA workflow bundled with [ComfyUI-H3-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-X2-Stream) (4 steps at 544 × 960, SLA 5%). Values are single runs (some are two-run means); the three rows above were measured on different days and include a few seconds of day-to-day variation. See [Generation time](#generation-time) and the [measurement record](docs/benchmark.json) for conditions.

> Author: Kamimoto (かみもと) | Quick results on **[X (@sep_is_heim)](https://x.com/sep_is_heim)**, write-ups (Japanese) on **[note](https://note.com/sepiablue)** ([article index](https://note.com/sepiablue/n/n8e612c619a3e)).

## Sample comparisons

Each video plays the left side's audio first, then plays the same picture again from the start with the right side's audio. The orange frame marks the side being heard. "Before" is the 4-step FL2VA workflow bundled with [ComfyUI-H3-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-X2-Stream).

### Fast (LBH) vs before — 14 s, singing with guitar

Left: before (X2 Stream 4-step, 172.1 s). Right: AudioFirst fast (LBH, 137.9 s). Same image, prompt and seed 43, measured in one session on 2026-10-14. Generated at 640 × 928 (fast: 448 × 640 → 640 × 928) and saved at 1280 × 1856.

https://github.com/user-attachments/assets/9f9d5269-91d0-48e7-ba7b-cbe817d62ae3

### Standard vs before — 14 s, five Japanese dialogue lines

Left: before (X2 Stream 4-step). Right: AudioFirst standard.

https://github.com/user-attachments/assets/cf5235c9-6f93-48f9-b12a-ee7db16d43b5

### Standard vs before — 14 s, singing in English while playing guitar

Left: before (X2 Stream 4-step). Right: AudioFirst standard. The image (1248 × 1824) was resized to 657 × 960 without changing its aspect ratio and center-cropped to 544 × 960, the same resolution as the bundled examples.

https://github.com/user-attachments/assets/0b0780da-1946-4184-9c7a-8a4a08fe61d8

## How it works

The voice is finished first in an 8-step audio-only pass on a tiny 32 × 32 canvas, then locked while the unchanged video pass generates the picture. Output is 1088 × 1920 through the X2 VAE and asynchronous NVENC saving. The video pass is the FL2VA configuration from [Sayaka Benchmark](https://sayakabenchmark.pages.dev/), used as is, so picture quality matches the previous workflow.

The fast variant combines the same audio lock with LBH 3+1 from [ComfyUI-H3-LBH-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-LBH-X2-Stream) (3 steps at 384 × 672, then upscaled for 1 step at 544 × 960).

The speed mode runs those three steps at 256 × 448 and skips 10 of the 50 DiT blocks in the last step; the audio pass is unchanged.

## Standard or fast

| | Standard | Fast (LBH) |
|---|---|---|
| Video pass | Same as before (4 steps at 544 × 960) | LBH 3+1 (3 steps at 384 × 672 → 1 step at 544 × 960) |
| Aspect ratio | Free (width and height multiples of 32) | Low and high resolutions must share one aspect ratio; the image is center-cropped for each |
| Extra install | None | ComfyUI-H3-LBH-X2-Stream, the LBH 3D upscaler and the F12 cache (prepared automatically on the first run, about 0.93 GB) |
| Best for | Free aspect ratios, minimal installs | Speed (faster from 5 s up) |

| Video | Standard | Fast (LBH) | Difference |
|---|---:|---:|---:|
| 5 s (544 × 960) | 72.8 s (1 min 12.8 s) | 60.0 s (1 min 0.0 s) | -12.8 s |
| 10 s (544 × 960) | 118.9 s (1 min 58.9 s) | 93.6 s (1 min 33.6 s) | -25.3 s |
| 14 s (544 × 960) | 165.1 s (2 min 45.1 s) | 125.7 s (2 min 5.7 s) | -39.4 s |
| 14 s singing (640 × 928) | 187.2 s (3 min 7.2 s) | 137.9 s (2 min 17.9 s) | -49.3 s |

5 s, 10 s and singing were measured on 2026-10-14 (one run each); for 14 s the standard run is from 2026-10-13 and the fast run from 2026-10-14. The fast singing run used 448 × 640 → 640 × 928, and the previous workflow took 172.1 s (2 min 52.1 s) in the same session. Compared with LBH 3+1 without the audio pass, it adds about 12 s (5 s: 48.3 → 60.0 s, 14 s: 113.6 → 125.7 s).

## Speed mode

The speed mode is the fast workflow with two changes: the three low-resolution steps run at 256 × 448 instead of 384 × 672, and the last step at 544 × 960 skips 10 of the 50 DiT blocks. The audio pass and lock are unchanged, so the audio is identical to the fast variant. The picture is a different take of the same prompt because the earlier steps run at a different size.

| | Fast (LBH) | Speed |
|---|---|---|
| Audio pass | 32 × 32, 8 steps | Same (decoded audio identical to fast) |
| Steps 1–3 | 384 × 672 | 256 × 448 |
| Step 4 (544 × 960) | All 50 DiT blocks | Blocks 9–12, 14–18 and 20 skipped |
| Extra install | LBH X2 Stream, LBH 3D upscaler, F12 cache | Same as fast |

| Video | Fast (LBH) | Speed |
|---|---:|---:|
| 5 s | – | 57.3 s |
| 10 s | – | 77.5 s |
| 14 s | 131.9 s (2 min 11.9 s) | 102.9 s (1 min 42.9 s) |

Single runs of the packaged examples (seed 43) in one session on 2026-10-22 with ComfyUI 0.42.0. Other applications were using the GPU during this session, and the same 14 s fast example took 125.7 s in an earlier, quieter session, so compare the columns rather than the absolute values.

Choosing the blocks: each block was bypassed alone in the last step (at 256 × 448, 14 s, seed 48) and the change of the resulting video latent was measured, following the vital-layer analysis of [Stable Flow](https://arxiv.org/abs/2411.14430). The ten blocks with the smallest change are skipped; blocks 0–2, 29–33, 48 and 49 mattered most. Skipping applies only to the last step, where the audio is already locked. Compared within one run (identical earlier steps), the speed-mode last step differed from the unskipped one by PSNR 24 dB and SSIM 0.85 at 1088 × 1920, while two unskipped last steps differed by 40.9 dB and 0.987. Line sharpness and frame-to-frame flicker did not change, the result looked equally detailed for seeds 48 and 50, and lip sync was judged fine. Ten blocks chosen by a simpler rule (the smallest change of the hidden state, blocks 3–17) lost iris detail, so the choice matters.

## Generation time

Standard versus before, measured on an RTX 4070 12 GB with the same image, prompt and seed 43.

| Video | Frames | Before (X2 Stream 4-step) | AudioFirst standard | Difference |
|---|---:|---:|---:|---:|
| 5 s | 124 | 60.8 s (1 min 0.8 s) | 71.7 s (1 min 11.7 s) | +11.0 s (+18.0%) |
| 10 s | 243 | 105.7 s (1 min 45.7 s) | 117.1 s (1 min 57.1 s) | +11.4 s (+10.8%) |
| 14 s | 345 | 153.8 s (2 min 33.8 s) | 165.1 s (2 min 45.1 s) | +11.3 s (+7.4%) |
| 14 s singing | 345 | 153.2 s (2 min 33.2 s) | 169.6 s (2 min 49.6 s) | +16.4 s (+10.7%) |

5 s is the mean of two runs per method; the others are single runs. For dialogue, the previous workflow was measured on 2026-10-11 and AudioFirst on 2026-10-13, so the values include a few seconds of day-to-day variation. Both singing runs were measured in one session on 2026-10-13; its audio pass was slower than in other sessions (about 1.4 s per step instead of 1.2 s), so that difference is larger. Times are ComfyUI history `execution_start` to `execution_success`, excluding server startup, uploads and inspection.

The 32 × 32 audio pass has little compute; transferring model weights that do not fit in 12 GB is the likely main cost (not profiled). The 8-step audio pass took about 15 s regardless of video length, so the added time stays at roughly 11–12 s and becomes a smaller share for longer videos.

## Pipeline

| Stage | Description |
|---|---|
| Conditioning | TE and the 544 × 960 keyframe exactly as before, run once and shared by both passes |
| Audio pass | 32 × 32, dense attention, 8 steps, same model, sampler, sigma shift and seed |
| Audio lock | The finished audio latent is inserted into the video-pass latent with an audio noise mask of 0 |
| Video pass | Identical to before: 544 × 960, 4 steps, SLA 5%, FFN 8 chunks |
| Check | Saving stops unless the audio latent after the video pass still equals the audio pass |
| Save | Audio VAE decodes the audio-pass latent; INT8 X2 VAE, H.264 NVENC and AAC output |

### Why these settings

| Test | Result |
|---|---|
| Audio-pass steps 4/5/6/8 | 4 and 5 steps still sounded metallic; 6 and 8 were good. 8 steps selected because the cost difference is small |
| Video pass cut to 2 steps, SLA 1% | Rejected for blur and smearing |
| Same-MODEL sequential sampling, deferred audio decode, compiler off, FFN memory reuse | No stable speedup; not adopted |

The audio pass costs about 1.2 s per step. If speed matters more, setting "Audio pass scheduler" to 6 steps saves about 2.5 s; 6 steps also suppressed the metallic sound in testing.

## Requirements

Windows with NVIDIA CUDA. Developed and measured on an RTX 4070 12 GB with ComfyUI 0.38.0, Python 3.13.13, PyTorch 2.14.0+cu130 and comfy-kitchen 0.2.36. Speed and quality on other GPUs, operating systems or models are not guaranteed.

ComfyUI must provide native MiniMax H3 (MiniMaxH3ImageToVideo, MiniMaxH3SigmaShift) and BlockSparseAttention. Measurements used Dynamic VRAM with `--disable-pinned-memory`. Output uses [ComfyUI-H3-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-X2-Stream). Setup never updates ComfyUI or PyTorch.

## Install with ComfyUI-Manager (easiest)

1. In ComfyUI-Manager, search for and install **H3 AudioFirst X2 Stream** ([h3-audiofirst-x2-stream](https://registry.comfy.org/publishers/sepiablue-ai/nodes/h3-audiofirst-x2-stream)) and **H3 X2 Stream** ([h3-x2-stream](https://registry.comfy.org/publishers/sepiablue-ai/nodes/h3-x2-stream)), which every example uses for saving. For the fast variant, also install **H3 LBH X2 Stream** ([h3-lbh-x2-stream](https://registry.comfy.org/publishers/sepiablue-ai/nodes/h3-lbh-x2-stream)). The Manager built into recent ComfyUI is enabled with `--enable-manager`.
2. Restart ComfyUI.
3. Copy the image from [`examples/assets`](examples/assets) into `ComfyUI/input/`. Manager does not copy sample inputs.

Manager installs the code and Python requirements; models are still placed by hand (see [Models](#models)). Prepare the X2 INT8 decoder once with [00_prepare_x2.json](examples/00_prepare_x2.json); for the fast variant, the F12 Loader prepares its cache (about 0.93 GB) on first use. Tested on 2026-10-15 with ComfyUI 0.38.0 and ComfyUI-Manager 4.2.2: all three packs installed without warnings, restart, all nodes registered and the standard and fast examples loaded. Video generation was not part of that test.

Use one installation method only. Manager installs into `custom_nodes/h3-audiofirst-x2-stream`, `custom_nodes/h3-x2-stream` and `custom_nodes/h3-lbh-x2-stream`, while `setup.bat` looks for `ComfyUI-H3-X2-Stream` and `ComfyUI-H3-LBH-X2-Stream`. If the dependencies came from Manager, do not run `setup.bat --install-dependencies` or `--with-lbh`; they would add second copies and register the same nodes twice.

## Windows setup

Place this repo at `ComfyUI/custom_nodes/ComfyUI-H3-AudioFirst-X2-Stream/`, or run setup.bat from any folder. Stop ComfyUI first.

```bat
setup.bat "C:\ComfyUI\ComfyUI" "C:\ComfyUI\.venv\Scripts\python.exe"
```

Without an explicit Python, setup looks for that ComfyUI's portable Python, `.venv` or `venv` and requires exactly one candidate. Global Python is refused. Setup installs the code and sample image, and checks native nodes and models. It never overwrites a differing existing node or sample image and never starts ComfyUI.

If X2 Stream is not installed yet:

```bat
setup.bat "C:\ComfyUI\ComfyUI" "C:\ComfyUI\.venv\Scripts\python.exe" --install-dependencies
```

Add `--with-lbh` to prepare the fast variant as well:

```bat
setup.bat "C:\ComfyUI\ComfyUI" --install-dependencies --with-lbh
```

A missing X2 Stream is fetched at commit `eb148a3d0f91a273668bbe027bfcbafb85f2c5e8`, and LBH X2 Stream at commit `070b78cd7519b56d6684dcaf45ac6bd5f827dbda` only with `--with-lbh`; both are the code used for the measurements. Existing installs are left unchanged. pip runs with `--no-deps` for that dedicated Python. No models are downloaded.

Read-only check:

```bat
setup.bat "C:\ComfyUI\ComfyUI" "C:\ComfyUI\.venv\Scripts\python.exe" --check
```

`--check` performs no copy, pip or conversion.

## Models

No weights or generated videos are distributed. Place the following models yourself. Shared folders can be configured with ComfyUI's standard `extra_model_paths.yaml` ([example](extra_model_paths.yaml.example)); use `--extra-model-paths PATH` to give setup an additional file.

| File | ComfyUI location | Source |
|---|---|---|
| minimax_h3_fused_refdelta_r1024_turbo8_mystic07_int8_convrot.safetensors | models/diffusion_models | [MATLOWAI](https://huggingface.co/MATLOWAI/minimax-h3-fused-turbo-int8-convrot/tree/main/diffusion_models) |
| qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors | models/text_encoders | [Comfy-Org](https://huggingface.co/Comfy-Org/MiniMax-H3/tree/main/text_encoders) |
| minimax_h3_video_vae_int8_convrot.safetensors | models/vae | [Comfy-Org](https://huggingface.co/Comfy-Org/MiniMax-H3/tree/main/vae) |
| minimax_h3_audio_vae_fp32.safetensors | models/vae | [Comfy-Org](https://huggingface.co/Comfy-Org/MiniMax-H3/tree/main/vae) |
| MiniMax-H3-X2-Detail-v1.safetensors | models/vae | [X2 Detail VAE](https://huggingface.co/speach1sdef178/MiniMax-H3-X2-Detail-VAE) |
| minimax_h3_latent_upscaler_3d_fp16.safetensors (fast variant only) | models/latent_upscale_models | [LBH](https://huggingface.co/LBH-123-AI/Minimax_h3_latent_Upscaler) |

For the fast variant, the F12 Loader prepares F12 (W4A4 FC1 in 12 blocks) under `models/h3_lbh_x2/f12` on the first run. See [ComfyUI-H3-LBH-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-LBH-X2-Stream) for details.

## Use in ComfyUI

1. Once, load [00_prepare_x2.json](examples/00_prepare_x2.json) to prepare the INT8 X2 VAE from the original. Skip it if X2 Stream already prepared it.
2. Drag the [5 s](examples/fl2va_audiofirst_05s.json), [10 s](examples/fl2va_audiofirst_10s.json) or [14 s](examples/fl2va_audiofirst_14s.json) workflow onto ComfyUI. API versions are in [examples/api](examples/api).
3. Choose an image in LoadImage and edit the MiniMaxH3ImageToVideo prompt. Setup copies the default sample image to input.
4. To change the length, set the same `length` on MiniMaxH3ImageToVideo and "Audio pass conditioning (32x32)". H3 frame counts follow 17k+5 (124, 243, 345, ...).
5. Keep both sampling width and height multiples of 32. If the image has a different aspect ratio, match it with ImageScale and ImageCrop first.

The fast variant is in the [5 s](examples/fl2va_audiofirst_lbh_05s.json), [10 s](examples/fl2va_audiofirst_lbh_10s.json) and [14 s](examples/fl2va_audiofirst_lbh_14s.json) workflows. To change the length, set the same `length` on Shared image conditioning and "Audio pass conditioning (32x32)". To change the resolution, give Shared image conditioning low and high sizes with the same aspect ratio in multiples of 32, and set LBH video upscale + continue to the high size. The first run spends extra time preparing F12.

The speed mode is in the [5 s](examples/fl2va_audiofirst_speed_05s.json), [10 s](examples/fl2va_audiofirst_speed_10s.json) and [14 s](examples/fl2va_audiofirst_speed_14s.json) workflows. They are the fast workflows with low size 256 × 448 and "Skip 10 DiT blocks (final step only)" between the model and the step-4 guider; length and resolution follow the fast-variant rules. Bypass that node to run the last step with all blocks.

All examples use seed 43, res_multistep/simple, video/audio sigma shift 12/3, 24 fps and CQ18. Output goes to ComfyUI's output/H3_AudioFirst_X2_Stream.

### Nodes

| Node | Purpose |
|---|---|
| H3 AudioFirst 32x32 Audio Conditioning | Reuses the video-pass conditioning and makes a 32 × 32 keyframe and empty latent; the TE is not run again |
| H3 AudioFirst Lock Audio | Inserts the finished audio latent into the video-pass latent with an audio noise mask of 0 |
| H3 AudioFirst Check Audio Lock | Stops if the audio latent after the video pass differs from the audio pass |
| H3 AudioFirst Skip Blocks (final step) | Bypasses the listed DiT blocks (default 9–12, 14–18, 20); connect it only to the last step's guider |

As in native H3 first-frame handling, the audio-pass keyframe is the input image resized to 32 × 32 without cropping. It only conditions the audio and does not affect the output picture.

## Validation scope

[docs/benchmark.json](docs/benchmark.json) records each run's prompt_id, SHA-256 of prompt, workflow and video, stage times and how the step count was chosen.

The 5, 10 and 14 s AudioFirst values come from running the packaged examples with only the output name changed (the singing run changed only the image, prompt and crop of the 14 s example). The two 5 s runs produced identical decoded audio, and every run passed the audio-lock check. A 6-step check made when the nodes were renamed for distribution gave audio identical to the experiment and video differing by the same amount the experiment runs differ from each other (PSNR about 25 dB); video sampling is not bit-reproducible between runs on this setup. See [docs/validation.json](docs/validation.json).

Speed mode: the 14 s example run with seed 48 gave decoded audio identical to the experiment it came from, and the 14 s speed and fast examples (seed 43) gave identical decoded audio. It has not been through a fresh-install test yet.

ComfyUI input validation and GUI/API round-trips pass for all examples; tests cover repeated setup, refusal to overwrite differing files and the example settings.

```bat
"C:\ComfyUI\.venv\Scripts\python.exe" -B -m unittest discover -s tests -v
```

A fresh clone of ComfyUI 0.39.0+49 was set up from a separate checkout of this repo with `setup.bat "COMFY_ROOT" --install-dependencies`; X2 preparation and the 5, 10 and 14 s examples then ran unchanged and all succeeded, with decoded audio identical to the measured runs on 0.38.0. PyTorch and other existing packages were referenced from an existing venv and only the 0.39.0 additions were installed into the dedicated venv, so this is not an install from a completely empty Python environment. A fresh clone of ComfyUI 0.40.0 was then set up with `--install-dependencies --with-lbh`, and X2 preparation, the standard 5 s example and the fast 5, 10 and 14 s examples all ran unchanged and succeeded (the first fast run took 107 s including F12 preparation; fast 10 s 93.5 s, 14 s 125.4 s), with decoded audio matching the measured runs. Browser drag-and-drop was not tested. See [docs/fresh_install_validation.json](docs/fresh_install_validation.json).

## Author and related repositories

I'm Kamimoto (かみもと). I measure and publish MiniMax H3 and ComfyUI speed-ups and VRAM reductions on an RTX 4070 12 GB.

- X: [@sep_is_heim](https://x.com/sep_is_heim) — quick results with step counts, seconds and speed-ups
- note: [かみもと｜ローカルAI生成](https://note.com/sepiablue) — setup guides and measured write-ups in Japanese ([article index](https://note.com/sepiablue/n/n8e612c619a3e))
- [Sayaka Benchmark](https://sayakabenchmark.pages.dev/) — speed and quality comparison of H3 workflows

| Repository | What it does |
|---|---|
| [ComfyUI-H3-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-X2-Stream) | INT8 X2 VAE and asynchronous NVENC saving; the output stage here and the "before" workflow |
| [ComfyUI-H3-LBH-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-LBH-X2-Stream) | LBH 3+1: 3 low-resolution steps + 1 high-resolution step; the base of the fast variant |
| [ComfyUI-MiniMax-H3-W4A4-VSA](https://github.com/sepiablue-ai/ComfyUI-MiniMax-H3-W4A4-VSA) | Ref2VA acceleration with FC1 W4A4 and Streaming VSA |

## License

Package code is GPL-3.0. Model weights keep the terms of their sources. See [NOTICE.md](NOTICE.md) for details and attribution.
