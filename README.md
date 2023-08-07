Inspired by [Raspberry Pi 4 GPGPU【入門】](https://techbookfest.org/product/tB65RxqBCqhCpAQE7M2YsB)

## setup

Raspberry Pi OS or Ubuntu

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    python3-pip \
    python3-numpy \
    python3-pil \
    ;

# py-videocore6
pip3 install --user --upgrade pip setuptools wheel
pip3 install --user git+https://github.com/Idein/py-videocore6.git

# GPU memory.
# default: 64 (MB)
# ref. https://www.raspberrypi.com/documentation/computers/config_txt.html
echo -e '\n# GPU available memory\ngpu_mem=256' | sudo tee -a /boot/config.txt
# [Ubuntu]
# echo -e '\n# GPU available memory\ngpu_mem=256' | sudo tee -a /boot/firmware/usercfg.txt

# Allow $USER access to the GPU.
sudo usermod --append --groups video $USER

sudo reboot now
```

## note
- `def execute(self, code, uniforms=None, timeout_sec=10, workgroup=(16, 1, 1), wgs_per_sg=16, thread=1)`
- p.26
    - r0-5, rf0-63: 32bit x16
- p.27
    - g['in_a'] = g['rf0']はレジスタのalias
        - 以降のin_aをすべてrf0にすれば動くし、in_aとrf0を混在させても動く
        - noalias-exchange.pyはエイリアス張らない版
    - 各レジスタ（r0とかrf10とか）はグローバル変数なので、globals()['x']=globals()['y']でエイリアス張れる
    - qpuデコレータを見るとわかりやすい
        - py-videocore6/videocore6/assembler.py
            - decoratorはwrapperなので、funcがkernelになる
        - 処理としては、
            1. kernelを実行する前にグローバル変数としてレジスタ定義
                - g['raw'] = functools.partial(Raw, asm) etc...
            2. kernel実行
                - func(asm, *args, **kwargs)
            3. 実行前のグローバル変数の状態に戻す
               - g.clear()
               - for key, value in g_orig.items():
               -     g[key] = value
- p.31
    - drv.allocで確保した2次元配列のアドレスは連続

## errata
- p.20
    - s/result変数/out変数/
- p.22
    - s/リストの4要素目/リストの3要素目/
    - ここだけuniformが1-basedになっている
        - p.23 > 出力を見てみるとuniformの0番目と...

