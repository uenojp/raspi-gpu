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
`def execute(self, code, uniforms=None, timeout_sec=10, workgroup=(16, 1, 1), wgs_per_sg=16, thread=1)`

## errata
- p. 20
    - s/result変数/out変数/

