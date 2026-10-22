# Attribution and model terms

Package code is GPL-3.0; see LICENSE. No model weights, converted weights or generated outputs other than the two comparison videos in docs/media are distributed.

- [ComfyUI-H3-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-X2-Stream), by sepiablue-ai, is the separate GPL-3.0 X2 conversion, FFN chunking and NVENC dependency. The reproducible setup reference is commit eb148a3d0f91a273668bbe027bfcbafb85f2c5e8, byte-identical to the code used for the measurements.
- The video pass is FL2VA 022-matlow-fused4-sla5-x2vae-int8-stream from [Sayaka Benchmark](https://sayakabenchmark.pages.dev/), by the same author.
- The nodes call [ComfyUI](https://github.com/Comfy-Org/ComfyUI)'s native MiniMax H3 helpers (_empty_av_latent, _resize), conditioning utilities and NestedTensor unchanged.
- examples/assets/fl2va_case01_no_text_948x1659.png is the same sample image distributed with ComfyUI-H3-X2-Stream.
- The MATLOW fused model and Comfy-Org H3 weights identify their license as MiniMax H3 Community License on their model pages. The X2 VAE retains the terms on its distribution page. This code license does not replace model or derived-weight terms. [X2 source](https://huggingface.co/speach1sdef178/MiniMax-H3-X2-Detail-VAE).

Measurements are in docs/benchmark.json and the package check is in docs/validation.json. No private experiment folder is required at runtime.

The optional fast workflows use [ComfyUI-H3-LBH-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-LBH-X2-Stream) (GPL-3.0, by sepiablue-ai) at commit 070b78cd7519b56d6684dcaf45ac6bd5f827dbda, installed only with `--with-lbh`. Its LBH upscaler weights and vendored MIT code keep the terms listed in that repository's NOTICE.

The speed mode uses the same LBH dependency. Its skipped-block list was measured with a single-block bypass test modelled on the vital-layer analysis of Stable Flow (Avrahami et al., CVPR 2025, [arXiv 2411.14430](https://arxiv.org/abs/2411.14430)); only the idea is used, no code from that project.
