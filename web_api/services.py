import json
from datetime import datetime
from subprocess import run
from web_api.models import Annotation, PreprocessedDataset

def detect_async(preprocessed_dataset, is_both):
  try:
    start_time = datetime.now()
    if(is_both):
      completed_process = run(f'{preprocessed_dataset.detector.command} --rgb-path {preprocessed_dataset.dataset.rgb_path} --thermal-path {preprocessed_dataset.dataset.thermal_path}', capture_output=True, text=True, shell=True)
      elapsed_time = datetime.now() - start_time
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
      preprocessed_dataset.status = PreprocessedDataset.SUCCEDED
      preprocessed_dataset.time = elapsed_time;
      preprocessed_dataset.save()
    else:
      completed_process = run(f'{preprocessed_dataset.detector.command} --rgb-path {preprocessed_dataset.dataset.rgb_path}', capture_output=True, text=True, shell=True)
      elapsed_time = datetime.now() - start_time
      if(completed_process.returncode != 0):
        raise Exception(str(completed_process))
      annotate_image_list = json.loads(completed_process.stdout)
      for annotated_image in annotate_image_list:
        a = Annotation(preprocessed_dataset=preprocessed_dataset, rgb_url=annotated_image["name"], rgb_boxes=annotated_image["boxes"])
        a.save()
      preprocessed_dataset.status = PreprocessedDataset.SUCCEDED
      preprocessed_dataset.time = elapsed_time;
      preprocessed_dataset.save()
  except:
    preprocessed_dataset.status = PreprocessedDataset.FAILED
    preprocessed_dataset.save()
    raise