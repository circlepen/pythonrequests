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
ip = '172.29.89.74:32118'
username = 'user1'
pwd = '1qaz2wsx'
key = get_token(username, pwd, ip)
token = f'Token {key}'

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
# resources = ['/Users/yijulai/Downloads/shiro.png',]
# attatch_data(t_id, ip, resource_type, resources)


"""
========== delete a task ==========
"""
# task_id = 1
# r = task_delete(task_id, ip, token)



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
# profit_url = "http://10.43.119.194:5000"
# model_name = "frcnn_inceptionresnetv2_coco"
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
