
#!/bin/bash

set -ex

# exec python3 model_inspect.py --runmode=saved_model \
#   --model_name=$MODEL_NAME --ckpt_path=/ckpt  \
#   --hparams="image_size=640x640" \
#   --saved_model_dir=/saved_model

exec python3 model_inspect.py \
  --runmode=saved_model_infer \
  --model_name=$MODEL_NAME  \
  --saved_model_dir=/saved_model  \
  --input_image=/img_folder/img.png \
  --output_image_dir=/img_folder/

exec "$@"
