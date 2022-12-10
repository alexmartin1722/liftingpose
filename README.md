# How Good Is Your Pose? Pose Estimation for Weight Lifting Form Correction
Paper: overleaf_veiwer_link

## Environment Creation
conda install pytorch==1.10.1 torchvision==0.11.2 torchaudio==0.10.1 -c pytorch
git clone https://github.com/open-mmlab/mmcv.git
cd mmcv
git checkout v1.3.9
MMCV_WITH_OPS=1 pip install -e .
cd ..
git clone https://github.com/alexmartin1722/liftingpose.git
cd liftingpose
cd ViTPose
pip install -v -e .
pip install timm==0.4.9 einops

## Usage
### Full Framework Demo



### CNN
#### Training CNN


#### Testing CNN


#### Demo CNN



### ViTPose
#### Training ViTPose 
```bash
bash ViTPose/tools/dist_train.sh <Config PATH> <NUM GPUs> --cfg-options model.pretrained=<Pretrained PATH> --seed 0
```

#### Testing ViTPose
```bash
bash tools/dist_test.sh <Config PATH> <Checkpoint PATH> <NUM GPUs>
```

#### Demo ViTPose






## CNN for Lift Classification

## ViTPose for Pose Estimation 


