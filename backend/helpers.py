from dotenv import load_dotenv
from flask import Response
import json
from models import *
import openai
import os


# Returns a success response with a custom status code and payload
def success_response(status: int, payload: dict=None):
    response = {'success': True}
    if payload is not None:
        response['data'] = payload
    return Response(
        response=json.dumps(response),
        status=status,
        mimetype="application/json"
    )


# Returns a failure response with a custom status code and error message
def failure_response(status: int, error_message: str):
    return Response(
        response=json.dumps({'success': False,
                             'error_message': error_message}),
        status=status,
        mimetype='application/json'
    )


# Return response from GPT, given input prompt
def prompt_gpt_openai(prompt: str):
    load_dotenv()
    openai.api_key = os.getenv('API_KEY_OPENAI')
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=0,
        max_tokens=16
    )
    return response['choices'][0]['text']


# Return response from GPT, given input prompt, using Azure subscription
def prompt_gpt_azure(prompt: str, max_tokens: int):
    load_dotenv()
    openai.api_key = os.getenv('API_KEY_AZURE')
    openai.api_base =  'https://gpt-for-social-media-chatbot.openai.azure.com/'
    openai.api_type = 'azure'
    openai.api_version = '2022-12-01'
    response = openai.Completion.create(
        engine='gpt3_davinci',
        prompt=prompt,
        temperature=0,
        max_tokens=max_tokens
    )
    return response['choices'][0]['text']


# Do basic formatting on classification prediction outputs
def format_detection_response(response: str):
    return response.lower().strip()


# Build detection prompt and perform GPT call
def perform_detection(dc: type[Detection], messages: list):
    # construct instruction portion of prompt
    classes = dc.get_classes()
    prompt_classes = ''
    for cls in classes:
        prompt_classes += f'{cls}, '
    prompt_classes = prompt_classes[:prompt_classes.rindex(',')]
    instruction = f'Classify the user inputs into one of the following categories: {prompt_classes}\n'

    # construct few-shot examples portion of prompt
    examples = dc.get_examples()
    example_num = 0
    few_shot_examples = ''
    for cls in examples.keys():
        for example in examples[cls]:
            example_num += 1
            few_shot_examples += f'Input {example_num}: {example}\n'
            few_shot_examples += f'Category {example_num}: {cls}\n'
    
    # construct classification input portion of prompt
    message_to_classify = messages[-1]['message']
    new_input = f'Input {example_num+1}: {message_to_classify}\nCategory {example_num+1}: '

    # construct full prompt, call GPT, and return predicted class
    prompt = instruction + few_shot_examples + new_input
    predicted_class = format_detection_response(prompt_gpt_azure(prompt, 16))
    return predicted_class


# Build generation prompt and perform GPT call
def perform_generation(gc: type[Generation], messages: list):
    # TODO: Consider making instruction more general. Generation may be in response to student comments on social media, students
    # directly talking to the chatbot, or the output of other generation components (in the case of sequential generation components.)

    # construct instruction portion of prompt
    instruction = f'The student sees a cyberbully on social media and makes a comment in response to the bully.  Teach students to counteract cyberbullies based on the following examples:\n'

    # construct few-shot examples portion of prompt
    examples = gc.get_examples()
    example_num = 0
    few_shot_examples = ''
    for example in examples:
        example_num += 1
        few_shot_examples += f'Example {example_num}:\n'
        few_shot_examples += f'Context: {example.context}\n'
        few_shot_examples += f'Response: {example.response}\n'
    
    # add conversation history
    conversation_history = ''
    if len(messages) >= 2:
        conversation_history = f'Here is the conversation history with the student:\n'
        for i in range(len(messages) - 1):
            message = messages[i]['message']
            role = messages[i]['role']
            if role == 'student':
                conversation_history += f'Student: {message}\n'
            elif role == 'chatbot':
                conversation_history += f'Chatbot: {message}\n'

    #TODO: Consider making new_input more general. message_to_answer might be from either the student or chatbot. 

    # construct generation input portion of prompt
    new_input = "Here is what the student said, fill in the answer:\n"
    message_to_answer = messages[-1]['message']
    new_input += f'Context: {message_to_answer}\Response: '

    # construct full prompt, call GPT, and return generated response
    prompt = instruction + few_shot_examples + conversation_history + new_input
    return prompt_gpt_azure(prompt, 100).strip()


# Starting at component c in its respective dialogue tree, process the input messages
# appropriately. Return chatbot responses from generation components as a list
# and the next component in the tree as an id (or "exit" if leaf node is reached).
def traverse_dialogue_tree(c: type[Component], messages: list, responses=None, first_detection=True):
    # base cases:
    # 1) current component is a generation component and a leaf node
    #    - do last generation call
    #    - return responses and 'exit'
    # 2) current component is a detection component and a leaf node
    #    - ignore classifier call since there are no generation components to go to
    #    - return responses and 'exit'
    #    - with complete tree, should not reach this base case
    # 3) current component is a detection component and is not the first detection component in API call
    #    - return responses and c.id
    if isinstance(c, Generation) and c.is_leaf():
        response = perform_generation(c, messages)
        if responses is None:
            responses = [response]
        else:
            responses.append(response)
        return responses, 'exit'
    elif isinstance(c, Detection) and c.is_leaf():
        if responses is None:
            responses = []
        return responses, 'exit'
    elif isinstance(c, Detection) and not first_detection:
        return responses, c.id


    # recursive cases:
    # 1) current component is detection component
    #    - classify most recent student message in messages
    #    - use classification result to go to the correct generation component
    # 2) current component is a generation component
    #    - generate response using current component and messages
    #    - add response to messages and responses
    #    - go to next component in tree
    if isinstance(c, Detection):
        det_class = perform_detection(c, messages)
        outgoing_gcs = c.get_generation_edges()
        next_c = None
        for gc in outgoing_gcs:
            if gc.gen_class == det_class:
                next_c = gc
        if next_c is not None:
            return traverse_dialogue_tree(next_c, messages, responses, False)
        else:
            raise Exception(f'no edge found from {c.id} to generation component with class {det_class}')
    else:
        response = perform_generation(c, messages)
        if responses is None:
            responses = [response]
        else:
            responses.append(response)
        messages.append({'role': 'chatbot', 'message': response})
        next_c = c.get_next_component()
        return traverse_dialogue_tree(next_c, messages, responses, first_detection)