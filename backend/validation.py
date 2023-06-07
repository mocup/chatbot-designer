from models import *
import os


def validate_dialogue_exists(id: str):
    return f'{id}.pkl' in os.listdir('data')


def validate_component_exists(dt_id: str, c_id: str):
    return DialogueTree.load(dt_id).get_component(c_id) is not None


def validate_generation_example_exists(dt_id: str, gc_id: str, ex_id: str):
    return DialogueTree.load(dt_id).get_component(gc_id).get_example(ex_id) is not None


def validate_detection_class_exists(dt_id: str, dc_id: str, cls_id: str):
    return DialogueTree.load(dt_id).get_component(dc_id).get_class(cls_id) is not None


def validate_detection_class_example_exists(dt_id: str, dc_id: str, cls_id: str, ex_id: str):
    return DialogueTree.load(dt_id).get_component(dc_id).get_class(cls_id).get_example(ex_id) is not None


def validate_create_dialogue(request_data: dict):
    error_msg, status_code = None, None
    if request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'name' not in request_data.keys():
        error_msg = 'dialogue tree name not provided'
        status_code = 400
    elif type(request_data['name']) != str:
        error_msg = 'dialogue tree name is not a string'
        status_code = 400
    return error_msg, status_code


def validate_get_dialogue(dt_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    return error_msg, status_code


def validate_edit_dialogue_name(dt_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'name' not in request_data.keys():
        error_msg = 'dialogue tree name not provided'
        status_code = 400
    elif type(request_data['name']) != str:
        error_msg = 'dialogue tree name is not a string'
        status_code = 400
    return error_msg, status_code


def validate_add_dialogue_edge(dt_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'start' not in request_data.keys():
        error_msg = 'start component id not provided'
        status_code = 400
    elif type(request_data['start']) != str:
        error_msg = 'start component id is not a string'
        status_code = 400
    elif 'end' not in request_data.keys():
        error_msg = 'end component id not provided'
        status_code = 400
    elif type(request_data['end']) != str:
        error_msg = 'end component id is not a string'
        status_code = 400
    elif not validate_component_exists(dt_id, request_data['start']):
        error_msg = 'provided start component does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, request_data['end']):
        error_msg = 'provided end component does not exist'
        status_code = 404
    return error_msg, status_code


def validate_delete_dialogue_edge(dt_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'start' not in request_data.keys():
        error_msg = 'start component id not provided'
        status_code = 400
    elif type(request_data['start']) != str:
        error_msg = 'start component id is not a string'
        status_code = 400
    elif 'end' not in request_data.keys():
        error_msg = 'end component id not provided'
        status_code = 400
    elif type(request_data['end']) != str:
        error_msg = 'end component id is not a string'
        status_code = 400
    elif not validate_component_exists(dt_id, request_data['start']):
        error_msg = 'provided start component does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, request_data['end']):
        error_msg = 'provided end component does not exist'
        status_code = 404
    elif {'start': request_data['start'], 'end': request_data['end']} not in DialogueTree.load(dt_id).get_edges():
        error_msg = 'provided edge does not exist'
        status_code = 404
    return error_msg, status_code


def validate_add_generation(dt_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'name' not in request_data.keys():
        error_msg = 'generation component name not provided'
        status_code = 400
    elif type(request_data['name']) != str:
        error_msg = 'generation component name is not a string'
        status_code = 400
    return error_msg, status_code


def validate_get_generation(dt_id: str, gc_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, gc_id):
        error_msg = 'provided generation component does not exist'
        status_code = 404
    return error_msg, status_code


def validate_delete_generation(dt_id: str, gc_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, gc_id):
        error_msg = 'provided generation component does not exist'
        status_code = 404
    return error_msg, status_code


def validate_edit_generation_name(dt_id: str, gc_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, gc_id):
        error_msg = 'provided generation component does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'name' not in request_data.keys():
        error_msg = 'generation component name not provided'
        status_code = 400
    elif type(request_data['name']) != str:
        error_msg = 'generation component name is not a string'
        status_code = 400
    return error_msg, status_code


def validate_edit_generation_class(dt_id: str, gc_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, gc_id):
        error_msg = 'provided generation component does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'class' not in request_data.keys():
        error_msg = 'generation class name not provided'
        status_code = 400
    elif type(request_data['class']) != str:
        error_msg = 'generation class name is not a string'
        status_code = 400
    return error_msg, status_code


def validate_add_generation_example(dt_id: str, gc_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, gc_id):
        error_msg = 'provided generation component does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'context' not in request_data.keys():
        error_msg = 'generation example context not provided'
        status_code = 400
    elif type(request_data['context']) != str:
        error_msg = 'generation example context is not a string'
        status_code = 400
    elif 'response' not in request_data.keys():
        error_msg = 'generation example response not provided'
        status_code = 400
    elif type(request_data['response']) != str:
        error_msg = 'generation example response is not a string'
        status_code = 400
    return error_msg, status_code


def validate_delete_generation_example(dt_id: str, gc_id: str, ex_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, gc_id):
        error_msg = 'provided generation component does not exist'
        status_code = 404
    elif not validate_generation_example_exists(dt_id, gc_id, ex_id):
        error_msg = 'provided generation example does not exist'
        status_code = 404
    return error_msg, status_code


def validate_edit_generation_example(dt_id: str, gc_id: str, ex_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, gc_id):
        error_msg = 'provided generation component does not exist'
        status_code = 404
    elif not validate_generation_example_exists(dt_id, gc_id, ex_id):
        error_msg = 'provided generation example does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'context' not in request_data.keys() and 'response' not in request_data.keys():
        error_msg = 'new generation example context and response not provided (need at least one)'
        status_code = 400
    elif 'context' in request_data.keys() and type(request_data['context']) != str:
        error_msg = 'new generation example context is not a string'
        status_code = 400
    elif 'response' in request_data.keys() and type(request_data['response']) != str:
        error_msg = 'new generation example response is not a string'
        status_code = 400
    return error_msg, status_code


def validate_copy_generation(dt_id: str, gc_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, gc_id):
        error_msg = 'provided generation component does not exist'
        status_code = 404
    return error_msg, status_code


def validate_add_detection(dt_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'name' not in request_data.keys():
        error_msg = 'detection component name not provided'
        status_code = 400
    elif type(request_data['name']) != str:
        error_msg = 'detection component name is not a string'
        status_code = 400
    return error_msg, status_code


def validate_get_detection(dt_id: str, dc_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    return error_msg, status_code


def validate_delete_detection(dt_id: str, dc_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    return error_msg, status_code


def validate_edit_detection_name(dt_id: str, dc_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'name' not in request_data.keys():
        error_msg = 'detection component name not provided'
        status_code = 400
    elif type(request_data['name']) != str:
        error_msg = 'detection component name is not a string'
        status_code = 400
    return error_msg, status_code


def validate_add_detection_class(dt_id: str, dc_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'class' not in request_data.keys():
        error_msg = 'detection class name not provided'
        status_code = 400
    elif type(request_data['class']) != str:
        error_msg = 'detection class name is not a string'
        status_code = 400
    return error_msg, status_code


def validate_get_detection_class(dt_id: str, dc_id: str, cls_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    elif not validate_detection_class_exists(dt_id, dc_id, cls_id):
        error_msg = 'provided detection class does not exist'
        status_code = 404
    return error_msg, status_code


def validate_delete_detection_class(dt_id: str, dc_id: str, cls_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    elif not validate_detection_class_exists(dt_id, dc_id, cls_id):
        error_msg = 'provided detection class does not exist'
        status_code = 404
    return error_msg, status_code


def validate_edit_detection_class_name(dt_id: str, dc_id: str, cls_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    elif not validate_detection_class_exists(dt_id, dc_id, cls_id):
        error_msg = 'provided detection class does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'class' not in request_data.keys():
        error_msg = 'detection class name not provided'
        status_code = 400
    elif type(request_data['class']) != str:
        error_msg = 'detection class name is not a string'
        status_code = 400
    return error_msg, status_code


def validate_add_detection_class_example(dt_id: str, dc_id: str, cls_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    elif not validate_detection_class_exists(dt_id, dc_id, cls_id):
        error_msg = 'provided detection class does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'example' not in request_data.keys():
        error_msg = 'detection class example not provided'
        status_code = 400
    elif type(request_data['example']) != str:
        error_msg = 'detection class example is not a string'
        status_code = 400
    return error_msg, status_code


def validate_delete_detection_class_example(dt_id: str, dc_id: str, cls_id: str, ex_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    elif not validate_detection_class_exists(dt_id, dc_id, cls_id):
        error_msg = 'provided detection class does not exist'
        status_code = 404
    elif not validate_detection_class_example_exists(dt_id, dc_id, cls_id, ex_id):
        error_msg = 'provided detection class example does not exist'
        status_code = 404
    return error_msg, status_code


def validate_edit_detection_class_example(dt_id: str, dc_id: str, cls_id: str, ex_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    elif not validate_detection_class_exists(dt_id, dc_id, cls_id):
        error_msg = 'provided detection class does not exist'
        status_code = 404
    elif not validate_detection_class_example_exists(dt_id, dc_id, cls_id, ex_id):
        error_msg = 'provided detection class example does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'example' not in request_data.keys():
        error_msg = 'new detection class example not provided'
        status_code = 400
    elif type(request_data['example']) != str:
        error_msg = 'new detection class example is not a string'
        status_code = 400
    return error_msg, status_code


def validate_copy_detection(dt_id: str, dc_id: str):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    return error_msg, status_code


def validate_prompt_generation_component(dt_id: str, gc_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, gc_id):
        error_msg = 'provided generation component does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'messages' not in request_data.keys():
        error_msg = 'messages not provided'
        status_code = 400
    elif type(request_data['messages']) != list:
        error_msg = 'messages is not a list'
        status_code = 400

    if error_msg is not None:
        return error_msg, status_code

    for element in request_data['messages']:
        if type(element) != dict:
            error_msg = 'messages list does not contain all dictionaries'
            status_code = 400
        elif 'role' not in element.keys():
            error_msg = 'role not provided'
            status_code = 400
        elif element['role'] != 'student' and element['role'] != 'chatbot':
            error_msg = 'role must be "chatbot" or "student"'
            status_code = 400
        elif 'message' not in element.keys():
            error_msg = 'message not provided'
            status_code = 400
        elif type(element['message']) != str:
            error_msg = 'message must be a string'
            status_code = 400
    
    return error_msg, status_code


def validate_prompt_detection_component(dt_id: str, dc_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, dc_id):
        error_msg = 'provided detection component does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'messages' not in request_data.keys():
        error_msg = 'messages not provided'
        status_code = 400
    elif type(request_data['messages']) != list:
        error_msg = 'messages is not a list'
        status_code = 400

    if error_msg is not None:
        return error_msg, status_code

    for element in request_data['messages']:
        if type(element) != dict:
            error_msg = 'messages list does not contain all dictionaries'
            status_code = 400
        elif 'role' not in element.keys():
            error_msg = 'role not provided'
            status_code = 400
        elif element['role'] != 'student' and element['role'] != 'chatbot':
            error_msg = 'role must be "chatbot" or "student"'
            status_code = 400
        elif 'message' not in element.keys():
            error_msg = 'message not provided'
            status_code = 400
        elif type(element['message']) != str:
            error_msg = 'message must be a string'
            status_code = 400
    
    return error_msg, status_code


def validate_chat(dt_id: str, c_id: str, request_data: dict):
    error_msg, status_code = None, None
    if not validate_dialogue_exists(dt_id):
        error_msg = 'provided dialogue tree does not exist'
        status_code = 404
    elif not validate_component_exists(dt_id, c_id):
        error_msg = 'provided component does not exist'
        status_code = 404
    elif request_data is None:
        error_msg = 'request body not provided'
        status_code = 400
    elif 'messages' not in request_data.keys():
        error_msg = 'messages not provided'
        status_code = 400
    elif type(request_data['messages']) != list:
        error_msg = 'messages is not a list'
        status_code = 400

    if error_msg is not None:
        return error_msg, status_code

    for element in request_data['messages']:
        if type(element) != dict:
            error_msg = 'messages list does not contain all dictionaries'
            status_code = 400
        elif 'role' not in element.keys():
            error_msg = 'role not provided'
            status_code = 400
        elif element['role'] != 'student' and element['role'] != 'chatbot':
            error_msg = 'role must be "chatbot" or "student"'
            status_code = 400
        elif 'message' not in element.keys():
            error_msg = 'message not provided'
            status_code = 400
        elif type(element['message']) != str:
            error_msg = 'message must be a string'
            status_code = 400
    
    return error_msg, status_code