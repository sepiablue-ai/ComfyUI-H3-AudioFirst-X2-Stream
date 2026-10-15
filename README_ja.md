# ComfyUI H3 AudioFirst X2 Stream

[English](README.md) | 日本語

**MiniMax H3の高速設定で出やすい「金属管の中で話しているような声」を抑えるComfyUIノードです。高速版（LBH）なら、音声を改善したうえで従来より速く生成できます。**

RTX 4070 12GB、1088×1920・音声付き動画の実測です。

| 14秒のセリフ動画 | 生成時間 | 音声 |
|---|---:|---|
| 従来（X2 Stream 4step） | 153.8秒（2分33.8秒） | 金属的な響きが出やすい |
| AudioFirst 標準版 | 165.1秒（2分45.1秒） | 改善 |
| **AudioFirst 高速版（LBH）** | **125.7秒（2分5.7秒）** | **改善** |

- **従来より約18%速く、音声も改善**：14秒のセリフで153.8秒→125.7秒（−28.1秒）。
- **同じセッションでの比較でも約20%短縮**：14秒のギター弾き語り（640×928）で、従来172.1秒→高速版137.9秒。
- **5秒でも遅くならない**：高速版60.0秒。従来（約60.8秒）とほぼ同じ時間で、音声だけ良くなります。
- **標準版は画質そのまま**：映像の生成は従来と同一で、音声だけを置き換えます（追加は約11秒）。

「従来」は[ComfyUI-H3-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-X2-Stream)同梱の4step FL2VAワークフロー（544×960で4step、SLA 5%）です。数値は各1回（一部は2回平均）の実測で、上の表の3行は計測日が異なるため数秒の揺れを含みます。条件の詳細は[生成時間](#生成時間)と[実測記録](docs/benchmark.json)にあります。

> 作者：かみもと（Kamimoto）｜検証結果の速報は **[X（@sep_is_heim）](https://x.com/sep_is_heim)**、解説記事は **[note](https://note.com/sepiablue)**（[記事INDEX](https://note.com/sepiablue/n/n8e612c619a3e)）で公開しています。

## サンプル比較

どちらも左が従来（X2 Stream 4step）、右がAudioFirst（標準版）です。前半は左の音声、後半は同じ映像を最初から流して右の音声を再生します。再生中の側をオレンジ枠で示しています。

| 内容 | 動画 |
|---|---|
| 14秒・日本語のセリフ5文 | ▶ [docs/media/compare_14s_talk.mp4](docs/media/compare_14s_talk.mp4) |
| 14秒・ギターを弾きながら英語の歌 | ▶ [docs/media/compare_14s_sing.mp4](docs/media/compare_14s_sing.mp4) |

歌のサンプルは1248×1824の画像を縦横比を保って657×960に縮小し、中央を切り抜いて544×960で生成しています（同梱exampleと同じ解像度）。

**14 s, five Japanese dialogue lines**

https://github.com/user-attachments/assets/cf5235c9-6f93-48f9-b12a-ee7db16d43b5

**14 s, singing in English while playing guitar**

https://github.com/user-attachments/assets/0b0780da-1946-4184-9c7a-8a4a08fe61d8

## 仕組み

先に32×32の小さな画面で音声だけを8stepで作り切り、その音声を固定したまま従来と同じ映像パスで動画を生成します。X2 VAEと非同期NVENC保存で1088×1920を出力します。映像パスは[さやかベンチマーク](https://sayakabenchmark.pages.dev/)のFL2VA構成をそのまま使うため、画質は従来と同等です。

高速版は、[ComfyUI-H3-LBH-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-LBH-X2-Stream)のLBH 3+1（384×672で3step、拡大して544×960で1step）に同じ音声固定を組み合わせたワークフローです。

## 標準版と高速版の使い分け

| | 標準版 | 高速版（LBH） |
|---|---|---|
| 映像パス | 従来と同一（544×960で4step） | LBH 3+1（384×672で3step→544×960で1step） |
| 縦横比 | 自由（width・heightが32の倍数） | 低・高解像度を同じ比率にする。画像は解像度ごとに中央クロップ |
| 追加の導入 | なし | ComfyUI-H3-LBH-X2-Stream、LBH 3D upscaler、F12キャッシュ（初回自動準備、約0.93GB） |
| 向いている用途 | 縦横比を自由に決めたい、導入を増やしたくない | 速さを優先したい（5秒から効果あり） |

| 動画 | 標準版 | 高速版（LBH） | 差 |
|---|---:|---:|---:|
| 5秒（544×960） | 72.8秒（1分12.8秒） | 60.0秒（1分0.0秒） | -12.8秒 |
| 10秒（544×960） | 118.9秒（1分58.9秒） | 93.6秒（1分33.6秒） | -25.3秒 |
| 14秒（544×960） | 165.1秒（2分45.1秒） | 125.7秒（2分5.7秒） | -39.4秒 |
| 14秒・歌（640×928） | 187.2秒（3分7.2秒） | 137.9秒（2分17.9秒） | -49.3秒 |

5・10秒と歌は2026年10月14日の同日計測（各1回）、14秒は標準版が10月13日、高速版が10月14日です。歌の高速版は448×640→640×928で生成し、同じセッションの従来版は172.1秒（2分52.1秒）でした。音声改善を入れないLBH 3+1と比べた追加時間は約12秒（5秒48.3→60.0秒、14秒113.6→125.7秒）でした。

## 生成時間

標準版と従来の比較です。RTX 4070 12GBでの実測で、同じ画像・プロンプト・seed43で比較しています。

| 動画 | フレーム | 従来（X2 Stream 4step） | AudioFirst 標準版 | 差 |
|---|---:|---:|---:|---:|
| 5秒 | 124 | 60.8秒（1分0.8秒） | 71.7秒（1分11.7秒） | +11.0秒（+18.0%） |
| 10秒 | 243 | 105.7秒（1分45.7秒） | 117.1秒（1分57.1秒） | +11.4秒（+10.8%） |
| 14秒 | 345 | 153.8秒（2分33.8秒） | 165.1秒（2分45.1秒） | +11.3秒（+7.4%） |
| 14秒・歌 | 345 | 153.2秒（2分33.2秒） | 169.6秒（2分49.6秒） | +16.4秒（+10.7%） |

5秒は各2回の平均、その他は各1回です。セリフの従来版は2026年10月11日、AudioFirstは10月13日の計測で、日による数秒の揺れを含みます。歌は10月13日に同じセッションで両方を計測しました。歌のAudioFirstは音声パスがこのセッションだけ遅く（1stepあたり約1.4秒、他は約1.2秒）、差が大きめに出ています。ComfyUI標準historyの`execution_start`から`execution_success`までで、サーバー起動・アップロード・検査を含みません。

32×32の音声パスは計算量が小さく、12GBに収まらないモデル重みの転送が主な時間と考えられます（プロファイルは未取得）。8stepの音声パスは動画の長さにかかわらず約15秒でした。追加時間は約11〜12秒でほぼ一定なので、長い動画ほど割合は小さくなります。

## 生成の流れ

| 工程 | 内容 |
|---|---|
| 条件付け | TEと544×960のキーフレームは従来と同じ。1回だけ実行して両パスで共有 |
| 音声パス | 32×32、dense attention、8step。同じモデル・sampler・sigma shift・seed |
| 音声の固定 | 完成した音声latentを映像パスのlatentへ入れ、noise maskを0にする |
| 映像パス | 従来と同一。544×960、4step、SLA 5%、FFN 8分割 |
| 確認 | 映像パス後の音声latentが音声パスと一致することを確認してから保存 |
| 保存 | 音声パスの音声をAudio VAEで波形化し、INT8 X2 VAE・H.264 NVENC・AACで保存 |

### 設定を選んだ理由

| 検証 | 結果 |
|---|---|
| 音声パスのstep数（4/5/6/8） | 4・5stepは金属的な響きが残り、6・8stepは良好。差が小さいため8stepを採用 |
| 映像パスを2step・SLA 1%に削る | 滲み・ぼやけが出たため不採用 |
| 同じMODELでの連続サンプリング、音声デコードの後回し、compiler無効、FFNメモリ再利用 | 安定した短縮が確認できず不採用 |

音声パスは1stepあたり約1.2秒です。速度を優先する場合は「Audio pass scheduler」を6stepにすると約2.5秒短くなります（6stepでも金属的な響きは抑えられていました）。

## 必要な環境

WindowsとNVIDIA CUDA向けです。開発検証はRTX 4070 12GB、ComfyUI 0.38.0、Python 3.13.13、PyTorch 2.14.0+cu130、comfy-kitchen 0.2.36で行いました。他のGPU・OS・モデルで同じ速度や品質を保証するものではありません。

ComfyUIにネイティブMiniMax H3（MiniMaxH3ImageToVideo、MiniMaxH3SigmaShift）とBlockSparseAttentionが必要です。実測はDynamic VRAM有効、`--disable-pinned-memory`で行いました。出力には[ComfyUI-H3-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-X2-Stream)を使います。ComfyUI本体やPyTorchはsetupで更新しません。

## Windowsセットアップ

このrepoを`ComfyUI/custom_nodes/ComfyUI-H3-AudioFirst-X2-Stream/`へ配置するか、任意のフォルダからsetup.batを実行してください。ComfyUIを停止してから準備します。

```bat
setup.bat "C:\ComfyUI\ComfyUI" "C:\ComfyUI\.venv\Scripts\python.exe"
```

専用Pythonを省略すると、そのComfyUIのPortable Python、`.venv`、`venv`を探します。候補が1つでなければ明示指定が必要です。グローバルPythonは拒否します。setupはコードとサンプル画像を配置し、ネイティブノードとモデルを確認します。既存の異なるノードやサンプル画像を上書きしません。ComfyUIを起動しません。

X2 Streamが未導入なら、次を実行します。

```bat
setup.bat "C:\ComfyUI\ComfyUI" "C:\ComfyUI\.venv\Scripts\python.exe" --install-dependencies
```

高速版も使う場合は`--with-lbh`を加えます。

```bat
setup.bat "C:\ComfyUI\ComfyUI" --install-dependencies --with-lbh
```

未導入のX2 Streamはcommit `eb148a3d0f91a273668bbe027bfcbafb85f2c5e8`、LBH X2 Streamは`--with-lbh`のときだけcommit `070b78cd7519b56d6684dcaf45ac6bd5f827dbda`から取得します。どちらも実測に使ったコードと同じです。既存のものは更新しません。pipはその専用Pythonに対して`--no-deps`で実行します。モデルはダウンロードしません。

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
| minimax_h3_latent_upscaler_3d_fp16.safetensors（高速版のみ） | models/latent_upscale_models | [LBH](https://huggingface.co/LBH-123-AI/Minimax_h3_latent_Upscaler) |

高速版のF12（FC1の12層をW4A4）は、初回実行時にF12 Loaderが`models/h3_lbh_x2/f12`へ準備します。詳細は[ComfyUI-H3-LBH-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-LBH-X2-Stream)を参照してください。

## ComfyUIで使う

1. 初回だけ[00_prepare_x2.json](examples/00_prepare_x2.json)を読み込み、元のX2 VAEからINT8版を準備します。X2 Streamで準備済みなら省略できます。
2. [5秒](examples/fl2va_audiofirst_05s.json)、[10秒](examples/fl2va_audiofirst_10s.json)、[14秒](examples/fl2va_audiofirst_14s.json)のいずれかをComfyUIへドラッグします。API版は[examples/api](examples/api)です。
3. LoadImageで画像を選び、MiniMaxH3ImageToVideoのプロンプトを変更します。初期サンプル画像はsetupがinputへコピーします。
4. 動画の長さを変える場合は、MiniMaxH3ImageToVideoと「Audio pass conditioning (32x32)」の`length`を同じ値にします。H3のフレーム数は17k+5（124、243、345など）です。
5. 生成解像度はwidth・heightとも32の倍数にしてください。画像の縦横比と異なる場合は、ImageScaleとImageCropで合わせてから入力します。

高速版は[5秒](examples/fl2va_audiofirst_lbh_05s.json)、[10秒](examples/fl2va_audiofirst_lbh_10s.json)、[14秒](examples/fl2va_audiofirst_lbh_14s.json)です。長さを変える場合はShared image conditioningと「Audio pass conditioning (32x32)」の`length`を同じ値にします。解像度を変える場合は、Shared image conditioningの低・高解像度を同じ縦横比の32の倍数にし、LBH video upscale + continueのwidth・heightを高解像度と同じ値にします。初回はF12の準備に時間がかかります。

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

表のAudioFirstの値のうち5・10・14秒は、配布版のexampleを出力名だけ変えて実行したものです（歌は14秒exampleの画像・プロンプト・切り抜きだけを変更）。5秒の2回は音声がデコード後に完全一致し、全runで音声固定を確認しました。ノード名を配布版へ変更した際の6step検証では、音声が実験版と完全一致し、映像は実験版のrun同士の差と同程度（PSNR約25dB）でした。このPCの設定では映像サンプリングがrun間でビット一致しません。[検証記録](docs/validation.json)。

全exampleのComfyUI入力検査とGUI/API往復の一致、setupの再実行・上書き拒否、exampleの設定値を確認しています。

```bat
"C:\ComfyUI\.venv\Scripts\python.exe" -B -m unittest discover -s tests -v
```

新規cloneしたComfyUI 0.39.0+49に、別フォルダのこのrepoから`setup.bat "COMFY_ROOT" --install-dependencies`で導入し、X2準備と5・10・14秒exampleを無変更で実行しました。すべて成功し、音声は0.38.0での実測runとデコード後に完全一致しました。PyTorch等は既存venvを参照し、0.39.0の追加要件だけを専用venvへ導入した試験で、完全に空のPython環境からの導入ではありません。さらに新規cloneしたComfyUI 0.40.0に`--install-dependencies --with-lbh`で導入し、X2準備、標準版5秒、高速版5・10・14秒を無変更で実行して全て成功しました（初回の高速版はF12準備を含み107秒、高速版10秒93.5秒・14秒125.4秒）。音声は実測runとデコード後に一致しました。ブラウザーでのドラッグ操作は未検査です。[導入検証記録](docs/fresh_install_validation.json)。

## 作者・関連リポジトリ

かみもと（Kamimoto）です。RTX 4070 12GBで、MiniMax H3とComfyUIの高速化・省VRAM化を実測しながら公開しています。

- X：[@sep_is_heim](https://x.com/sep_is_heim) — step数・秒数・短縮率などの検証速報
- note：[かみもと｜ローカルAI生成](https://note.com/sepiablue) — 導入方法と実測の解説記事（[記事INDEX](https://note.com/sepiablue/n/n8e612c619a3e)）
- [さやかベンチマーク](https://sayakabenchmark.pages.dev/) — H3ワークフローの速度・画質比較

| リポジトリ | 内容 |
|---|---|
| [ComfyUI-H3-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-X2-Stream) | X2 VAEのINT8化と非同期NVENC保存。本repoの出力と「従来」構成の元 |
| [ComfyUI-H3-LBH-X2-Stream](https://github.com/sepiablue-ai/ComfyUI-H3-LBH-X2-Stream) | 低解像度3step＋高解像度1stepのLBH 3+1。高速版の土台 |
| [ComfyUI-MiniMax-H3-W4A4-VSA](https://github.com/sepiablue-ai/ComfyUI-MiniMax-H3-W4A4-VSA) | Ref2VAの高速化（FC1 W4A4、Streaming VSA） |

## ライセンス

本パッケージのコードはGPL-3.0です。モデル重みには各配布元の条件が適用されます。詳細と出典は[NOTICE.md](NOTICE.md)を参照してください。
