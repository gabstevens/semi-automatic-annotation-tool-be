import json
import os
import shutil
from datetime import datetime
from subprocess import run
from web_api.models import Annotation, PreprocessedDataset

def detect_async(preprocessed_dataset, is_both):
  try:
    batch_size = 1000
    start_time = datetime.now()
    if(is_both):
      for i in range((len(os.listdir(preprocessed_dataset.dataset.thermal_path)) // batch_size) + 1):
        os.mkdir("web_api/datasets/rgb_tmp")
        os.mkdir("web_api/datasets/thermal_tmp")
        for img_name in os.listdir(preprocessed_dataset.dataset.thermal_path)[batch_size * i: batch_size * (i + 1)]:
          os.symlink(os.path.join(preprocessed_dataset.dataset.thermal_path, img_name), os.path.join("web_api/datasets/thermal_tmp", img_name))
          os.symlink(os.path.join(preprocessed_dataset.dataset.rgb_path, img_name), os.path.join("web_api/datasets/rgb_tmp", img_name))
        completed_process = run(f'{preprocessed_dataset.detector.command} --rgb-path web_api/datasets/rgb_tmp --thermal-path web_api/datasets/thermal_tmp', capture_output=True, text=True, shell=True)
        shutil.rmtree("web_api/datasets/rgb_tmp")
        shutil.rmtree("web_api/datasets/thermal_tmp")
        if(completed_process.returncode != 0):
          raise Exception(str(completed_process))
        annotate_image_list = json.loads(completed_process.stdout)
        for annotated_image in annotate_image_list:
          a = Annotation(preprocessed_dataset=preprocessed_dataset,
              thermal_url=annotated_image["thermal"]["name"],
              thermal_boxes=annotated_image["thermal"]["boxes"],
              rgb_url=annotated_image["rgb"]["name"],
              rgb_boxes=annotated_image["rgb"]["boxes"]
            )
          a.save()
      elapsed_time = datetime.now() - start_time
      preprocessed_dataset.status = PreprocessedDataset.SUCCEEDED
      preprocessed_dataset.time = elapsed_time;
      preprocessed_dataset.save()
    else:
      dataset_path = preprocessed_dataset.dataset.rgb_path or preprocessed_dataset.dataset.thermal_path
      for i in range((len(os.listdir(dataset_path)) // batch_size) + 1):
        os.mkdir("web_api/datasets/tmp")
        for img_name in os.listdir(dataset_path)[batch_size * i: batch_size * (i + 1)]:
          os.symlink(os.path.join(dataset_path, img_name), os.path.join("web_api/datasets/tmp", img_name))
        completed_process = run(f'{preprocessed_dataset.detector.command} --path web_api/datasets/tmp', capture_output=True, text=True, shell=True)
        shutil.rmtree("web_api/datasets/tmp")
        if(completed_process.returncode != 0):
          raise Exception(str(completed_process))
        annotate_image_list = json.loads(completed_process.stdout)
        for annotated_image in annotate_image_list:
          if(preprocessed_dataset.dataset.rgb_path):
            a = Annotation(preprocessed_dataset=preprocessed_dataset, rgb_url=annotated_image["name"], rgb_boxes=annotated_image["boxes"])
          else:
            a = Annotation(preprocessed_dataset=preprocessed_dataset, thermal_url=annotated_image["name"], thermal_boxes=annotated_image["boxes"])
          a.save()
      elapsed_time = datetime.now() - start_time
      preprocessed_dataset.status = PreprocessedDataset.SUCCEEDED
      preprocessed_dataset.time = elapsed_time;
      preprocessed_dataset.save()
  except:
    preprocessed_dataset.status = PreprocessedDataset.FAILED
    preprocessed_dataset.save()
    raise