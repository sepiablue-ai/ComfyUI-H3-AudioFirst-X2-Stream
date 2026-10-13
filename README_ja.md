# ComfyUI H3 AudioFirst X2 Stream

[English](README.md) | 日本語

MiniMax H3の高速設定で生成したセリフが、金属管の中で話しているように響く問題を抑えるComfyUIノードとワークフローです。先に32×32の小さな画面で音声だけを6stepで作り切り、その音声を固定したまま022と同じ映像パスで動画を生成します。X2 VAEと非同期NVENC保存で1088×1920を出力します。

映像パスは[さやかベンチマーク](https://sayakabenchmark.pages.dev/)のFL2VA `022-matlow-fused4-sla5-x2vae-int8-stream`をそのまま使います。画質は022と同等で、音声だけを置き換えます。

## サンプル比較

どちらも左が022（改善前）、右がAudioFirst（改善後）です。前半は左の音声、後半は同じ映像を最初から流して右の音声を再生します。再生中の側をオレンジ枠で示しています。

| 内容 | 動画 |
|---|---|
| 14秒・日本語のセリフ5文 | [docs/media/compare_14s_talk.mp4](docs/media/compare_14s_talk.mp4) |
| 14秒・ギターを弾きながら英語の歌 | [docs/media/compare_14s_sing.mp4](docs/media/compare_14s_sing.mp4) |

歌のサンプルは1248×1824の画像を縦横比を保って640×928で生成しています（同梱exampleは544×960）。

## 生成時間

RTX 4070 12GBでの実測です。022とAudioFirstは同じ画像・プロンプト・seed43で比較しています。

| 動画 | フレーム | 022 | AudioFirst | 差 |
|---|---:|---:|---:|---:|
| 5秒 | 124 | 60.8秒（1分0.8秒） | 71.4秒（1分11.4秒） | +10.6秒（+17.5%） |
| 10秒 | 243 | 105.7秒（1分45.7秒） | 116.5秒（1分56.5秒） | +10.8秒（+10.2%） |
| 14秒 | 345 | 153.8秒（2分33.8秒） | 164.2秒（2分44.2秒） | +10.4秒（+6.8%） |
| 14秒・歌（640×928） | 345 | 172.0秒（2分52.0秒） | 185.6秒（3分5.6秒） | +13.7秒（+8.0%） |

5秒は各2回の平均、その他は各1回です。ComfyUI標準historyの`execution_start`から`execution_success`までで、サーバー起動・アップロード・検査を含みません。

32×32の音声パスは計算量が小さく、12GBに収まらないモデル重みの転送が主な時間と考えられます（プロファイルは未取得）。実測では動画の長さにかかわらず約14〜16秒でした。追加時間はおよそ10秒台で一定なので、長い動画ほど割合は小さくなります。

## 生成の流れ

| 工程 | 内容 |
|---|---|
| 条件付け | TEと544×960のキーフレームは022と同じ。1回だけ実行して両パスで共有 |
| 音声パス | 32×32、dense attention、6step。同じモデル・sampler・sigma shift・seed |
| 音声の固定 | 完成した音声latentを映像パスのlatentへ入れ、noise maskを0にする |
| 映像パス | 022と同一。544×960、4step、SLA 5%、FFN 8分割 |
| 確認 | 映像パス後の音声latentが音声パスと一致することを確認してから保存 |
| 保存 | 音声パスの音声をAudio VAEで波形化し、INT8 X2 VAE・H.264 NVENC・AACで保存 |

### 設定を選んだ理由

| 検証 | 結果 |
|---|---|
| 音声パスのstep数（4/5/6/8） | 4・5stepは金属的な響きが残り、6・8stepは良好。6stepを採用 |
| 映像パスを2step・SLA 1%に削る | 滲み・ぼやけが出たため不採用 |
| 同じMODELでの連続サンプリング、音声デコードの後回し、compiler無効、FFNメモリ再利用 | 安定した短縮が確認できず不採用 |

音声パスは1stepあたり約1.2秒で、8stepから6stepにすると約2.5秒短くなります。

## 必要な環境

WindowsとNVIDIA CUDA向けです。開発検証はRTX 4070 12GB、ComfyUI 0.38.0、Python 3.13.13、PyTorch 2.14.0+cu130、comfy-kitchen 0.2.36で行いました。他のGPU・OS・モデルで同じ速度や品質を保証するものではありません。

ComfyUIにネイティブMiniMax H3（MiniMaxH3ImageToVideo、MiniMaxH3SigmaShift）とBlockSparseAttentionが必要です。実測はDynamic VRAM有効、`--disable-pinned-memory`で行いました。出力には[ComfyUI-H3-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-X2-Stream)を使います。ComfyUI本体やPyTorchはsetupで更新しません。

## Windowsセットアップ

このrepoを`ComfyUI/custom_nodes/ComfyUI-H3-AudioFirst-X2-Stream/`へ配置するか、任意のフォルダからsetup.batを実行してください。ComfyUIを停止してから準備します。

```bat
setup.bat "C:\ComfyUI\ComfyUI" "C:\ComfyUI\.venv\Scripts\python.exe"
```

専用Pythonを省略すると、そのComfyUIのPortable Python、`.venv`、`venv`を探します。候補が1つでなければ明示指定が必要です。グローバルPythonは拒否します。setupはコードとサンプル画像を配置し、ネイティブノードとモデルを確認します。既存の異なるノードやサンプル画像を上書きしません。ComfyUIを起動しません。

X2 Streamが未導入なら、専用Pythonを指定して次を実行します。

```bat
setup.bat "C:\ComfyUI\ComfyUI" "C:\ComfyUI\.venv\Scripts\python.exe" --install-dependencies
```

未導入のX2 Streamはcommit `eb148a3d0f91a273668bbe027bfcbafb85f2c5e8`から取得します。これは実測に使ったX2 Streamと同じコードです。既存のX2 Streamは更新しません。pipはその専用Pythonに対して`--no-deps`で実行します。モデルはダウンロードしません。

検査のみ行う場合:

```bat
setup.bat "C:\ComfyUI\ComfyUI" "C:\ComfyUI\.venv\Scripts\python.exe" --check
```

`--check`は配置・pip・変換を行いません。

## モデル

重み・動画生成結果は同梱しません。次のモデルを自分で配置してください。共有フォルダはComfyUI標準の`extra_model_paths.yaml`で指定できます（[設定例](extra_model_paths.yaml.example)）。setupだけ追加設定を読む場合は`--extra-model-paths PATH`を使います。

| ファイル | ComfyUI内の場所 | 配布元 |
|---|---|---|
| minimax_h3_fused_refdelta_r1024_turbo8_mystic07_int8_convrot.safetensors | models/diffusion_models | [MATLOWAI](https://huggingface.co/MATLOWAI/minimax-h3-fused-turbo-int8-convrot/tree/main/diffusion_models) |
| qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors | models/text_encoders | [Comfy-Org](https://huggingface.co/Comfy-Org/MiniMax-H3/tree/main/text_encoders) |
| minimax_h3_video_vae_int8_convrot.safetensors | models/vae | [Comfy-Org](https://huggingface.co/Comfy-Org/MiniMax-H3/tree/main/vae) |
| minimax_h3_audio_vae_fp32.safetensors | models/vae | [Comfy-Org](https://huggingface.co/Comfy-Org/MiniMax-H3/tree/main/vae) |
| MiniMax-H3-X2-Detail-v1.safetensors | models/vae | [X2 Detail VAE](https://huggingface.co/speach1sdef178/MiniMax-H3-X2-Detail-VAE) |

## ComfyUIで使う

1. 初回だけ[00_prepare_x2.json](examples/00_prepare_x2.json)を読み込み、元のX2 VAEからINT8版を準備します。X2 Streamで準備済みなら省略できます。
2. [5秒](examples/fl2va_audiofirst_05s.json)、[10秒](examples/fl2va_audiofirst_10s.json)、[14秒](examples/fl2va_audiofirst_14s.json)のいずれかをComfyUIへドラッグします。API版は[examples/api](examples/api)です。
3. LoadImageで画像を選び、MiniMaxH3ImageToVideoのプロンプトを変更します。初期サンプル画像はsetupがinputへコピーします。
4. 動画の長さを変える場合は、MiniMaxH3ImageToVideoと「Audio pass conditioning (32x32)」の`length`を同じ値にします。H3のフレーム数は17k+5（124、243、345など）です。
5. 生成解像度はwidth・heightとも32の倍数にしてください。画像の縦横比と異なる場合は、ImageScaleとImageCropで合わせてから入力します。

全例はseed43、res_multistep/simple、video/audio sigma shift 12/3、24fps、CQ18です。保存先はComfyUIのoutput/H3_AudioFirst_X2_Streamです。

### ノード

| ノード | 役割 |
|---|---|
| H3 AudioFirst 32x32 Audio Conditioning | 映像パスと同じ条件付けを使い、32×32のキーフレームと空latentを作る。TEは再実行しない |
| H3 AudioFirst Lock Audio | 完成した音声latentを映像パスのlatentへ入れ、音声のnoise maskを0にする |
| H3 AudioFirst Check Audio Lock | 映像パス後の音声latentが音声パスと一致しなければ停止する |

音声パスのキーフレームは、ネイティブH3の先頭フレーム処理と同じく、入力画像をクロップせず32×32へ縮小します。音声の条件付けのためだけに使い、出力映像には影響しません。

## 検証範囲

[実測記録](docs/benchmark.json)に、各runのprompt_id、プロンプト・ワークフロー・動画のSHA-256、工程別時間、step数の選定経緯を記録しています。

配布版のノード名へ変更した後、5秒exampleを実行しました。音声はデコード後に実測runと完全一致し、映像は実測run同士の差と同程度（PSNR約25dB）でした。このPCの設定では映像サンプリングがrun間でビット一致しないため、この差は名前変更によるものではありません。[検証記録](docs/validation.json)。

全exampleのComfyUI入力検査とGUI/API往復の一致、setupの再実行・上書き拒否、exampleの設定値を確認しています。

```bat
"C:\ComfyUI\.venv\Scripts\python.exe" -B -m unittest discover -s tests -v
```

新規ComfyUIへの`--install-dependencies`による導入と、ブラウザーでのドラッグ操作は未検査です。

## ライセンス

本パッケージのコードはGPL-3.0です。モデル重みには各配布元の条件が適用されます。詳細と出典は[NOTICE.md](NOTICE.md)を参照してください。
