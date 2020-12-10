import requests
import json
import time
from typing import List, Dict

# authorization


def get_token(username: str, pwd: str, ip_port: str) -> str:
    """
    :param ip_port: 伺服器ip and port
    :param username: 使用者名稱
    :param pwd: 密碼
    """
    url = f"http://{ip_port}/api/v1/auth/login"
    data = {
        'username': username,
        'password': pwd
    }
    headers = {
        'Content-Type': 'application/json'
    }
    payload = json.dumps(data)
    response = requests.request("POST", url, data=payload, headers=headers)
    print('got the token')
    return response.json()['key']


# create task
def create_task(ip_port: str, token: str, name: str, labels: List[Dict]):
    """
    :param ip_port: 伺服器的ip和port
    :param token: 使用者認證 token
    :param name: task的名稱, required
    :param labels: 要附加的標籤，至少要有一個
    """
    url = f"http://{ip_port}/api/v1/tasks"  # change the url to your server ip port
    data = {
        "name": name,  # required
        "labels":  labels,  # at least one
        "z_order": False,
    }
    payload = json.dumps(data)
    headers = {
        'Authorization': token,   # use your token
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    r = response.json()
    return r['id']


# attatch data to task
def attatch_data(task_id: int, ip_port: str, resource_type: str, resources: List[str], token: str) -> None:
    """
    :param task_id: task id
    :param ip_port: 伺服器的ip和port
    :param token: 使用者認證 token
    :param resource_type: 資料來源，local, share or remote
    :param resources: 檔案清單
    """
    url = f"http://{ip_port}/api/v1/tasks/{task_id}/data"
    data = {}
    headers = {
        'Authorization': token,  # use your token
    }
    files = None
    if resource_type == 'local':
        files = {'client_files[{}]'.format(i): open(
            f, 'rb') for i, f in enumerate(resources)}
    elif resource_type == 'remote':
        data = {'remote_files[{}]'.format(
            i): f for i, f in enumerate(resources)}
    elif resource_type == 'share':
        data = {'server_files[{}]'.format(
            i): f for i, f in enumerate(resources)}
    # files = {'client_files[0]': open('/Users/yijulai/Downloads/shiro.png', 'rb')}
    data['image_quality'] = 50
    data['use_zip_chunk'] = 'true'
    r = requests.post(url=url, headers=headers, data=data, files=files)
    print(r.text)


# export annotations
def export_dataset(ip: str, token: str, task_id: int, data_type: str, mode: str) -> None:
    """
    :param ip: 伺服器ip
    :param token: 使用者認證token
    :param task_id: 特定task的id
    :param data_type: cvat_yolo, cvat_tfrecord, cvat_coco三選一
    :param mode: completed 或是 all 
    """

    if mode == 'completed':
        url = f'http://{ip}/api/v1/tasks/{task_id}/dataset?format={data_type}'
    elif mode == 'all':
        url = f'http://{ip}/api/v1/tasks/{task_id}/datasetAll?format={data_type}'
    else:
        print('a mode which is not supported')
        return None

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    request = requests.get(url, headers=headers)
    print('finish')


# export annotations and download
def dump_annotations(ip: str, token: str, task_id: int, data_type: str, filename: str) -> None:
    """
    :param ip: 伺服器ip
    :param token: 使用者認證token
    :param task_id: 特定task的id
    :param data_type: cvat_yolo, cvat_tfrecord, cvat_coco三選一
    :param filename: 下載儲存的檔名
    """

    url = f'http://{ip}/api/v1/tasks/{task_id}/annotations/{filename}?format={data_type}&action=download'

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
    }
    response = requests.get(url, headers=headers)
    while response.status_code == 202:
        print('still waiting...')
        time.sleep(2)
        response = requests.get(url, headers=headers)
    f = open(f'{filename}.xml', 'w')
    f.write(response.text)
    f.close()
    print('finish')


# delete a task by id
def task_delete(task_id: int, ip: str, token: str):
    """ Delete a list of tasks, ignoring those which don't exist. """
    data = {}
    headers = {
        'Authorization': token,  # use your token
        'content-type': 'application/json'
    }
    url = f'http://{ip}/api/v1/tasks/{task_id}'
    response = requests.delete(
        url,
        headers=headers,
        data=data
    )
    try:
        response.raise_for_status()
        print(f'Task ID {task_id} deleted')
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f'Task ID {task_id} not found.')
        else:
            raise e


# upload annotation file
def upload_annotation(task_id: int, ip: str, token: str, data_type: str, file: str) -> None:
    
    url = f'http://{ip}/api/v1/tasks/{task_id}/annotations?format={data_type}'
    headers = {
        'Authorization': token,  # use your token
    }
    files = {'annotation_file': open(file, 'rb')}
    response = requests.put(url, headers=headers, files=files)
    print(response, response.text)
    while response.status_code == 202:
        print('waiting...')
        time.sleep(2)
        response = requests.put(url, headers=headers)

    print('complete')

# job annotation update(create, delete, update)
def job_annotation_update(job_id: int, ip: str, token: str) -> None:
    url = f'http://{ip}/api/v1/jobs/{job_id}/annotations?action=create'
    url2 = f'http://{ip}/api/v1/jobs/{job_id}/annotations?action=delete'
    url3 = f'http://{ip}/api/v1/jobs/{job_id}/annotations?action=update'
    headers = {
        'Authorization': token,  # use your token
    }
    data_create = {}
    data_delete = {}
    data_update = {}
    '''
    data struncture should be like:
    data={
        shapes:[
            {
                attributes: []
                frame: 0
                group: 0
                label_id: 1
                occluded: false
                points: [372.5029296875, 448.3203125, 1032.9961547851562, 1188]
                type: "rectangle"
                z_order: 0
            }
            ]
        tags: []
        tracks: []
        version: 8
    }
    '''
    r1 = requests.patch(url, headers=headers, data=data_create)
    r2 = requests.patch(url2, headers=headers, data=data_delete)
    r3 = requests.patch(url3, headers=headers, data=data_update)

    print('finish')


def auto_annotation(task_id: int, ip: str, token: str, profit_url: str, model_name: str) -> None:
    url = f'http://{ip}/tensorflow/annotation/create/task/{task_id}'
    headers = {
        'Authorization': token, # use your token
        'Connection': 'keep-alive',
        'Content-Type': 'application/json'
    }
    data = {
        "jobstr":"1",
        "type":"detect_box_tf",
        "version":1,
        "name": model_name,
        "profit_url": profit_url,
        "labels":{
            "frisbee":34,
            "baseball_bat":39,
            "umbrella":28,
            "laptop":73,
            "bottle":44,
            "bus":6,
            "cup":47,
            "bicycle":2,
            "hot_dog":58,
            "baseball_glove":40,
            "elephant":22,
            "pizza":59,
            "fire_hydrant":11,
            "hair_drier":89,
            "oven":79,
            "suitcase":33,
            "snowboard":36,
            "surfboard":42,
            "skis":35,
            "toothbrush":90,
            "sink":81,
            "banana":52,
            "apple":53,
            "cat":17,
            "vase":86,
            "cell_phone":77,
            "sports_ball":37,
            "fork":48,
            "teddy_bear":88,
            "stop_sign":13,
            "bowl":51,
            "wine_glass":46,
            "backpack":27,
            "kite":38,
            "sandwich":54,
            "truck":8,
            "sheep":20,
            "orange":55,
            "tennis_racket":43,
            "refrigerator":83,
            "traffic_light":10,
            "potted_plant":64,
            "dog":18,
            "horse":19,
            "handbag":31,
            "book":84,
            "remote":75,
            "scissors":87,
            "cake":61,
            "broccoli":56,
            "mouse":74,
            "dining_table":67,
            "toilet":70,
            "car":3,
            "keyboard":76,
            "person":1,
            "zebra":24,
            "train":7,
            "couch":63,
            "giraffe":25,
            "bench":15,
            "motorcycle":4,
            "tie":32,
            "tv":72,
            "chair":62,
            "parking_meter":14,
            "bird":16,
            "toaster":80,
            "knife":49,
            "airplane":5,
            "boat":9,
            "bear":23,
            "skateboard":41,
            "carrot":57,
            "donut":60,
            "bed":65,
            "cow":21,
            "microwave":78,
            "clock":85,
            "spoon":50}
            }
    payload = json.dumps(data)
    # sent the create action
    response = requests.post(url, headers=headers, data=payload)
    print('first response', response)
    print(response.text)
    url = f'http://{ip}/tensorflow/annotation/meta/get'
    # get meta
    data = json.dumps([task_id])
    response = requests.post(url, headers=headers, data=data)
    print('second response', response)
    status = response.json()[str(task_id)]
    # wait for it to be finished
    print('the status is: ', status)
    if status['success'] and status['active']:
        url = f'http://{ip}/tensorflow/annotation/check/task/{task_id}'
        headers = {
            'Authorization': token, # use your token
            'Connection': 'keep-alive',
        }
        response = requests.get(url, headers=headers)
        print(response)
        print(response.text)
        while response.json()['status'] != 'finished':
            print('waiting')
            time.sleep(2)
            response = requests.get(url, headers=headers)
        print('finish')
    
    else:
        print('error', 'status not ok')
