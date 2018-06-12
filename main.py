import argparse
import requests
import base64
import json
import sys
import os

# [START generate_json]
def main(input_path, output_filename):
  """Translates the input file into a json output file.

  Args:
      input_file: a file object, containing lines of input to convert.
      output_filename: the name of the file to output the json to.
  """
  for current_file in os.listdir(input_path):
    if current_file.endswith('.jpg'):

      # init new request list
      request_list = []

      with open(input_path + '/' + current_file, 'rb') as image_file:
        content_json_obj = {
            'content': base64.b64encode(image_file.read()).decode('UTF-8')
        }

      feature_json_obj = []
      feature_json_obj.append({
        'type': DETECTION_TYPES[4],
        'maxResults': MAX_RESULTS,
      })
      feature_json_obj.append({
        'type': DETECTION_TYPES[7],
      })

      request_list.append({
          'features': feature_json_obj,
          'image': content_json_obj,
      })

      request = {'requests': request_list}
      #print(json.dumps(request, indent=4))
      call_api(json.dumps(request, indent=4))




API_KEY = ""
MAX_RESULTS = 10

API_URI= 'https://vision.googleapis.com/v1/images:annotate?key='

IMG_EXTENSIONS = ['.jpg', '.jpeg', '.bmp', '.png']
CONTENT_TYPE = 'application/json'
DETECTION_TYPES = [
    'TYPE_UNSPECIFIED',
    'FACE_DETECTION',
    'LANDMARK_DETECTION',
    'LOGO_DETECTION',
    'LABEL_DETECTION',
    'TEXT_DETECTION',
    'SAFE_SEARCH_DETECTION',
    'IMAGE_PROPERTIES'
]

def get_detection_type(detect_num):
  """Return the Vision API symbol corresponding to the given number."""
  detect_num = int(detect_num)
  if 0 < detect_num < len(DETECTION_TYPES):
      return DETECTION_TYPES[detect_num]
  else:
      return DETECTION_TYPES[0]
# [END generate_json]

def call_api(request_data):
  response = requests.post(
    url     = API_URI + API_KEY,
    data    = request_data,
    headers = {
      'Content-Type': CONTENT_TYPE
    })
  
  print(response.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-i', dest='input_file', required=True,
        help='The input folder with all images to convert to json.')
    parser.add_argument(
        '-o', dest='output_file', required=True,
        help='The name of the json file to output to.')
    args = parser.parse_args()

    main(args.input_file, args.output_file)