from flask import Flask, request
from flask_cors import CORS, cross_origin
from helpers import *
from models import *
from validation import *


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/dialogue', methods=['POST'])
def create_dialogue():
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_create_dialogue(request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    name = request_data['name']

    # create new dialogue tree
    dt = DialogueTree(name)
    dt.save()
    return success_response(201, {'id': dt.id})


@app.route('/dialogue/<dt_id>', methods=['GET'])
def get_dialogue(dt_id):
    error_msg, status_code = validate_get_dialogue(dt_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    # return JSON representation of dialogue tree
    dt = DialogueTree.load(dt_id)
    return success_response(200, dt.to_json())


@app.route('/dialogue/<dt_id>', methods=['DELETE'])
def delete_dialogue(dt_id):
    if not validate_dialogue_exists(dt_id):
        return failure_response(404, 'provided dialogue tree does not exist')
    
    # delete dialogue tree
    DialogueTree.load(dt_id).delete()
    return success_response(200)


@app.route('/dialogue/<dt_id>/name', methods=['PUT'])
def edit_dialogue_name(dt_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_edit_dialogue_name(dt_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    name = request_data['name']

    # edit dialogue tree name
    dt = DialogueTree.load(dt_id)
    dt.name = name
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/edge', methods=['POST'])
def add_dialogue_edge(dt_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_add_dialogue_edge(dt_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    start_id = request_data['start']
    end_id = request_data['end']

    # add edge to dialogue tree
    dt = DialogueTree.load(dt_id)
    dt.add_edge(start_id, end_id)
    dt.save()
    return success_response(201)


@app.route('/dialogue/<dt_id>/edge', methods=['DELETE'])
def delete_dialogue_edge(dt_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_delete_dialogue_edge(dt_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    start_id = request_data['start']
    end_id = request_data['end']

    # delete edge from dialogue tree
    dt = DialogueTree.load(dt_id)
    dt.delete_edge(start_id, end_id)
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/generation', methods=['POST'])
def add_generation(dt_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_add_generation(dt_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    name = request_data['name']

    # add generation component to dialogue tree
    dt = DialogueTree.load(dt_id)
    gc_id = dt.add_component('gc', name)
    dt.save()
    return success_response(201, {'id': gc_id})


@app.route('/dialogue/<dt_id>/generation/<gc_id>', methods=['GET'])
def get_generation(dt_id, gc_id):
    error_msg, status_code = validate_get_generation(dt_id, gc_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    # return JSON representation of generation component
    gc = DialogueTree.load(dt_id).get_component(gc_id)
    return success_response(200, gc.to_json())


@app.route('/dialogue/<dt_id>/generation/<gc_id>', methods=['DELETE'])
def delete_generation(dt_id, gc_id):
    error_msg, status_code = validate_delete_generation(dt_id, gc_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    # delete generation component from dialogue tree
    dt = DialogueTree.load(dt_id)
    dt.delete_component(gc_id)
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/generation/<gc_id>/name', methods=['PUT'])
def edit_generation_name(dt_id, gc_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_edit_generation_name(dt_id, gc_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    name = request_data['name']

    # edit generation component name
    dt = DialogueTree.load(dt_id)
    dt.get_component(gc_id).name = name
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/generation/<gc_id>/class', methods=['PUT'])
def edit_generation_class(dt_id, gc_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_edit_generation_class(dt_id, gc_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    gen_class = request_data['class']

    # edit generation component class
    dt = DialogueTree.load(dt_id)
    gc = dt.get_component(gc_id)
    status_code = 201 if gc.gen_class == '' else 200
    gc.gen_class = gen_class
    dt.save()
    return success_response(status_code)


@app.route('/dialogue/<dt_id>/generation/<gc_id>/example', methods=['POST'])
def add_generation_example(dt_id, gc_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_add_generation_example(dt_id, gc_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    context = request_data['context']
    response = request_data['response']

    # add example to generation component
    dt = DialogueTree.load(dt_id)
    ex_id = dt.get_component(gc_id).add_example(context, response)
    dt.save()
    return success_response(201, {'id': ex_id})


@app.route('/dialogue/<dt_id>/generation/<gc_id>/example/<ex_id>', methods=['DELETE'])
def delete_generation_example(dt_id, gc_id, ex_id):
    error_msg, status_code = validate_delete_generation_example(dt_id, gc_id, ex_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)
    
    # delete example from generation component
    dt = DialogueTree.load(dt_id)
    dt.get_component(gc_id).delete_example(ex_id)
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/generation/<gc_id>/example/<ex_id>', methods=['PUT'])
def edit_generation_example(dt_id, gc_id, ex_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_edit_generation_example(dt_id, gc_id, ex_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    context = request_data.get('context')
    response = request_data.get('response')

    # edit generation component example
    dt = DialogueTree.load(dt_id)
    dt.get_component(gc_id).get_example(ex_id).edit_example(context, response)
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/generation/<gc_id>/copy', methods=['POST'])
def copy_generation(dt_id, gc_id):
    error_msg, status_code = validate_copy_generation(dt_id, gc_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    # copy generation component and return copy's id
    dt = DialogueTree.load(dt_id)
    gc_copy_id = dt.copy_component('gc', gc_id)
    dt.save()
    return success_response(201, {'id': gc_copy_id})


@app.route('/dialogue/<dt_id>/detection', methods=['POST'])
def add_detection(dt_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_add_detection(dt_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    name = request_data['name']

    # add detection component to dialogue tree
    dt = DialogueTree.load(dt_id)
    dc_id = dt.add_component('dc', name)
    dt.save()
    return success_response(201, {'id': dc_id})


@app.route('/dialogue/<dt_id>/detection/<dc_id>', methods=['GET'])
def get_detection(dt_id, dc_id):
    error_msg, status_code = validate_get_detection(dt_id, dc_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    # return JSON representation of detection component
    dc = DialogueTree.load(dt_id).get_component(dc_id)
    return success_response(200, dc.to_json())


@app.route('/dialogue/<dt_id>/detection/<dc_id>', methods=['DELETE'])
def delete_detection(dt_id, dc_id):
    error_msg, status_code = validate_delete_detection(dt_id, dc_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    # delete detection component from dialogue tree
    dt = DialogueTree.load(dt_id)
    dt.delete_component(dc_id)
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/detection/<dc_id>/name', methods=['PUT'])
def edit_detection_name(dt_id, dc_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_edit_detection_name(dt_id, dc_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    name = request_data['name']

    # edit detection component name
    dt = DialogueTree.load(dt_id)
    dt.get_component(dc_id).name = name
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/detection/<dc_id>/class', methods=['POST'])
def add_detection_class(dt_id, dc_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_add_detection_class(dt_id, dc_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    det_class = request_data['class']

    # add class to detection component
    dt = DialogueTree.load(dt_id)
    cls_id = dt.get_component(dc_id).add_class(det_class)
    dt.save()
    return success_response(201, {'id': cls_id})


@app.route('/dialogue/<dt_id>/detection/<dc_id>/class/<cls_id>', methods=['GET'])
def get_detection_class(dt_id, dc_id, cls_id):
    error_msg, status_code = validate_get_detection_class(dt_id, dc_id, cls_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    # return JSON representation of detection class
    cls = DialogueTree.load(dt_id).get_component(dc_id).get_class(cls_id)
    return success_response(200, cls.to_json())


@app.route('/dialogue/<dt_id>/detection/<dc_id>/class/<cls_id>', methods=['DELETE'])
def delete_detection_class(dt_id, dc_id, cls_id):
    error_msg, status_code = validate_delete_detection_class(dt_id, dc_id, cls_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)
    
    # delete class from detection component
    dt = DialogueTree.load(dt_id)
    dt.get_component(dc_id).delete_class(cls_id)
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/detection/<dc_id>/class/<cls_id>/name', methods=['PUT'])
def edit_detection_class_name(dt_id, dc_id, cls_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_edit_detection_class_name(dt_id, dc_id, cls_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    det_class = request_data['class']

    # edit detection class name
    dt = DialogueTree.load(dt_id)
    dt.get_component(dc_id).get_class(cls_id).det_class = det_class
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/detection/<dc_id>/class/<cls_id>/example', methods=['POST'])
def add_detection_class_example(dt_id, dc_id, cls_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_add_detection_class_example(dt_id, dc_id, cls_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    example = request_data['example']

    # add example to detection class
    dt = DialogueTree.load(dt_id)
    ex_id = dt.get_component(dc_id).get_class(cls_id).add_example(example)
    dt.save()
    return success_response(201, {'id': ex_id})


@app.route('/dialogue/<dt_id>/detection/<dc_id>/class/<cls_id>/example/<ex_id>', methods=['DELETE'])
def delete_detection_class_example(dt_id, dc_id, cls_id, ex_id):
    error_msg, status_code = validate_delete_detection_class_example(dt_id, dc_id, cls_id, ex_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)
    
    # delete example from detection class
    dt = DialogueTree.load(dt_id)
    dt.get_component(dc_id).get_class(cls_id).delete_example(ex_id)
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/detection/<dc_id>/class/<cls_id>/example/<ex_id>', methods=['PUT'])
def edit_detection_class_example(dt_id, dc_id, cls_id, ex_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_edit_detection_class_example(dt_id, dc_id, cls_id, ex_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    example = request_data['example']

    # edit detection class example
    dt = DialogueTree.load(dt_id)
    dt.get_component(dc_id).get_class(cls_id).get_example(ex_id).example = example
    dt.save()
    return success_response(200)


@app.route('/dialogue/<dt_id>/detection/<dc_id>/copy', methods=['POST'])
def copy_detection(dt_id, dc_id):
    error_msg, status_code = validate_copy_detection(dt_id, dc_id)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    # copy detection component and return copy's id
    dt = DialogueTree.load(dt_id)
    dc_copy_id = dt.copy_component('dc', dc_id)
    dt.save()
    return success_response(201, {'id': dc_copy_id})


@app.route('/dialogue/<dt_id>/generation/<gc_id>/prompt', methods=['POST'])
def prompt_generation_component(dt_id, gc_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_prompt_generation_component(dt_id, gc_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)
    
    messages = request_data['messages']
    
    # generate response to most recent message
    gc = DialogueTree.load(dt_id).get_component(gc_id)
    response = perform_generation(gc, messages)
    return success_response(200, {'response': response})


@app.route('/dialogue/<dt_id>/detection/<dc_id>/prompt', methods=['POST'])
def prompt_detection_component(dt_id, dc_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_prompt_detection_component(dt_id, dc_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)

    messages = request_data['messages']

    # classify most recent message, which should be from the student
    dc = DialogueTree.load(dt_id).get_component(dc_id)
    response = perform_detection(dc, messages)
    return success_response(200, {'response': response})


@app.route('/dialogue/<dt_id>/chat/<c_id>', methods=['POST'])
def chat(dt_id, c_id):
    request_data = request.get_json(silent=True)
    error_msg, status_code = validate_chat(dt_id, c_id, request_data)
    if error_msg is not None:
        return failure_response(status_code, error_msg)
    
    messages = request_data['messages']

    # traverse dialogue tree from component c to the next detection component
    # return next detection component's id and generation component outputs
    c = DialogueTree.load(dt_id).get_component(c_id)
    try:
        responses, next_id = traverse_dialogue_tree(c, messages)
        return success_response(200, {'responses': responses, 'next_id': next_id})
    except Exception as e:
        return failure_response(400, e.args[0])


if __name__ == '__main__':
    app.run(port=8000)