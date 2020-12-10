from functions import (
    get_token,
    create_task,
    task_delete,
    attatch_data,
    export_dataset,
    dump_annotations,
    upload_annotation,
    job_annotation_update,
    auto_annotation
    )


"""
========== base information ========== 
"""
ip = '10.1.3.20:8080'
username = 'medicalai'
pwd = 'tangodown'
key = get_token(username, pwd, ip)
token = f'Token {key}'
#"key":"706c3a2fccae00f84d1a272fc1cfef4b47c5c4f5"
# uncomment the code you need below to use it

"""
========== create a new task ==========
"""
# labels = [{      
#             "name": "person",
#             "id": 12,
#             "color": "#c06060",
#             "attributes": []
#             }]
# name = "testAPI"
# t_id = create_task(ip, token, name, labels)
# resource_type = 'local'
# resources = [
#     '/home/share/hank_2020/cvat-images/dcm/mdb260rl_rot.png',
#     '/home/share/hank_2020/cvat-images/dcm/mdb259ll_rot.png',
#     '/home/share/hank_2020/cvat-images/dcm/mdb261ls_rot.png',
#     ]
# attatch_data(t_id, ip, resource_type, resources, token)


"""
========== delete a task ==========
"""
task_id = 4
r = task_delete(task_id, ip, token)



"""
========== dump annotations ==========
"""
# data_type = 'CVAT%20XML%201.1%20for%20images'
# # data_type = 'CVAT XML 1.1 for images' 
# task_id = 1
# filename = 'dump_annotation'
# dump_annotations(ip, token, task_id, data_type, filename)


"""
========== export data ==========
"""
# task_id = 1
# data_type = 'cvat_type'
# mode = 'completed'

# export_dataset(ip, token, task_id, data_type, mode)

"""
========== auto annotation ==========
"""
# profit_url = "10.1.3.21:35000"
# model_name = "breast"
# task_id = 1

# auto_annotation(task_id, ip, token, profit_url, model_name)


"""
========== upload annotation ==========
"""
# file = '/Users/yijulai/Desktop/dump_annotation.xml'
# task_id = 1
# # data_type = 'CVAT%20XML%201.1'
# data_type = 'CVAT XML 1.1'
# upload_annotation(task_id, ip, token, data_type, file)
