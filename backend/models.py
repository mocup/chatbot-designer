from copy import deepcopy
import os
import pickle


class DialogueTree():
    def __init__(self, name: str):
        self.id = DialogueTree.generate_dialogue_id()
        self.name = name
        self.components = []

    # Return a unique dialogue tree id of the form dt-{number}
    @staticmethod
    def generate_dialogue_id():
        if not os.path.exists('data'):
            os.mkdir('data')

        max_id_num = -1
        for filename in os.listdir('data'):
            id_num = int(filename[filename.index('-')+1:filename.index('.')])
            max_id_num = max(id_num, max_id_num)
        return f'dt-{max_id_num+1}'
    
    # Return a unique component id of the form {component_type}-{number}
    def generate_component_id(self, component_type: str):
        max_id_num = -1
        for component in self.components:
            if component.id.split('-')[0] == component_type:
                id_num = int(component.id.split('-')[1])
                max_id_num = max(id_num, max_id_num)
        return f'{component_type}-{max_id_num+1}'

    # Load dialogue tree from data directory
    @staticmethod
    def load(id: str):
        with open(f'data/{id}.pkl', 'rb') as file:
            dt = pickle.load(file)
        return dt

    # Save dialogue tree to data directory
    def save(self):
        with open(f'data/{self.id}.pkl', 'wb') as file:
            pickle.dump(self, file)

    # Delete dialogue tree from data directory
    def delete(self):
        os.remove(f'data/{self.id}.pkl')

    # Copy existing component in the dialogue tree and return
    # the copy's id
    def copy_component(self, component_type: str, id: str):
        component_copy = deepcopy(self.get_component(id))
        component_copy.id = self.generate_component_id(component_type)
        component_copy.neighbors = []
        self.components.append(component_copy)
        return component_copy.id

    # Return component with id if it exists, None otherwise
    def get_component(self, id: str):
        for component in self.components:
            if component.id == id:
                return component
        return None
    
    # Return list of component ids for every component in dialogue tree
    def get_component_ids(self):
        component_ids = []
        for component in self.components:
            component_ids.append(component.id)
        return component_ids

    # Return list of edges for every edge in the dialogue tree. Each edge is represented
    # as {"start": "id", "end": "id"}
    def get_edges(self):
        edges = []
        for component in self.components:
            for neighbor in component.neighbors:
                edge = {'start': component.id, 'end': neighbor.id}
                edges.append(edge)
        return edges
    
    # Add component to dialogue tree and return its id
    def add_component(self, component_type: str, name: str):
        id = self.generate_component_id(component_type)
        component = Generation(id, name) if component_type == 'gc' else Detection(id, name)
        self.components.append(component)
        return id
    
    # Add directed edge between components
    def add_edge(self, start_id: str, end_id: str):
        start_component = self.get_component(start_id)
        end_component = self.get_component(end_id)
        start_component.neighbors.append(end_component)

    # Delete component and any edges connected to it
    def delete_component(self, id: str):
        component = self.get_component(id)
        for edge in self.get_edges():
            if component.id == edge['end']:
                self.delete_edge(edge['start'], edge['end'])
        self.components.remove(component)

    # Delete directed edge between components with ids start_id and end_id
    def delete_edge(self, start_id: str, end_id: str):
        start_component = self.get_component(start_id)
        end_component = self.get_component(end_id)
        start_component.neighbors.remove(end_component)

    # Return a JSON representation for a dialogue tree
    def to_json(self):
        result = {}
        result['id'] = self.id
        result['name'] = self.name

        if self.components == []:
            result['components'] = 'not provided'
        else:
            result['components'] = self.get_component_ids()

        if self.get_edges() == []:
            result['edges'] = 'not provided'
        else:
            result['edges'] = self.get_edges()
        
        return result


class Component:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.neighbors = []

    # Return True if component is a leaf in the tree, False otherwise
    def is_leaf(self):
        return self.neighbors == []


class Generation(Component):
    def __init__(self, id: str, name: str):
        super().__init__(id, name)
        self.gen_class = ''
        self.examples = []

    # Return a unique example id of the form ex-{number}
    def generate_example_id(self):
        max_id_num = -1
        for example in self.examples:
            id_num = int(example.id.split('-')[1])
            max_id_num = max(id_num, max_id_num)
        return f'ex-{max_id_num+1}'
    
    # Return example with id if it exists, None otherwise
    def get_example(self, id: str):
        for example in self.examples:
            if example.id == id:
                return example
        return None
    
    # Return a list of examples to be used in generation prompt
    def get_examples(self):
        return self.examples
    
    # Return component on the outgoing edge from this generation component
    def get_next_component(self):
        return self.neighbors[0]

    # Add example to generation component, where example
    # consists of context and response, and return its id
    def add_example(self, context: str, response: str):
        id = self.generate_example_id()
        new_example = self.GenerationExample(id, context, response)
        self.examples.append(new_example)
        return id
    
    # Delete example with id from examples
    def delete_example(self, id: str):
        example = self.get_example(id)
        self.examples.remove(example)

    # Return a JSON representation for a generation component
    def to_json(self):
        result = {}
        result['id'] = self.id
        result['name'] = self.name

        if self.gen_class != '':
            result['class'] = self.gen_class
        else: 
            result['class'] = 'not provided'
            
        if self.examples == []:
            result['examples'] = 'not provided'
        else:
            examples = []
            for example in self.examples:
                examples.append({'id': example.id,
                                 'context': example.context, 
                                 'response': example.response})
            result['examples'] = examples

        return result

    class GenerationExample:
        def __init__(self, id: str, context: str, response: str):
            self.id = id
            self.context = context
            self.response = response
        
        # Edit context and/or response of example
        def edit_example(self, context: str or None, response: str or None):
            if context is not None:
                self.context = context
            if response is not None:
                self.response = response


class Detection(Component):
    def __init__(self, id: str, name: str):
        super().__init__(id, name)
        self.classes = []

    # Return a unique class id of the form cls-{number}
    def generate_class_id(self):
        max_id_num = -1
        for cls in self.classes:
            id_num = int(cls.id.split('-')[1])
            max_id_num = max(id_num, max_id_num)
        return f'cls-{max_id_num+1}'
    
    # Return DetectionClass with id if it exists, None otherwise
    def get_class(self, id: str):
        for cls in self.classes:
            if cls.id == id:
                return cls
        return None
    
    # Return a list of class names to be used in detection prompt
    def get_classes(self):
        classes = []
        for cls in self.classes:
            classes.append(cls.det_class)
        return classes
    
    # Return a dictionary of examples to be used in detection prompt
    def get_examples(self):
        examples = {}
        for cls in self.classes:
            examples[cls.det_class] = cls.get_examples()
        return examples
    
    # Return list of generation components that are on the outgoing edges
    # from this detection component
    def get_generation_edges(self):
        components = []
        for component in self.neighbors:
            if isinstance(component, Generation):
                components.append(component)
        return components
    
    # Add new detection class and return its id
    def add_class(self, det_class: str):
        id = self.generate_class_id()
        new_class = self.DetectionClass(id, det_class)
        self.classes.append(new_class)
        return id
    
    # Delete DetectionClass with id from classes
    def delete_class(self, id: str):
        cls = self.get_class(id)
        self.classes.remove(cls)

    # Return a JSON representation for a detection component
    def to_json(self):
        result = {}
        result['id'] = self.id
        result['name'] = self.name

        if self.classes == []:
            result['classes'] = 'not provided'
        else:
            classes = []
            for cls in self.classes:
                classes.append({'id': cls.id,
                                'class': cls.det_class})
            result['classes'] = classes

        return result

    class DetectionClass:
        def __init__(self, id: str, det_class: str):
            self.id = id
            self.det_class = det_class
            self.examples = []

        # Return a unique example id of the form ex-{number}
        def generate_example_id(self):
            max_id_num = -1
            for example in self.examples:
                id_num = int(example.id.split('-')[1])
                max_id_num = max(id_num, max_id_num)
            return f'ex-{max_id_num+1}'
        
        # Return DetectionExample with id if it exists, None otherwise
        def get_example(self, id: str):
            for example in self.examples:
                if example.id == id:
                    return example
            return None
        
        # Return list of examples in detection class
        def get_examples(self):
            lst = []
            for detection_example in self.examples:
                lst.append(detection_example.example)
            return lst

        # Add new example to detection class and return its id
        def add_example(self, example: str):
            id = self.generate_example_id()
            new_example = self.DetectionExample(id, example)
            self.examples.append(new_example)
            return id
        
        # Delete example with id from examples
        def delete_example(self, id: str):
            example = self.get_example(id)
            self.examples.remove(example)

        # Return a JSON representation for a detection class
        def to_json(self):
            result = {}
            result['id'] = self.id
            result['class'] = self.det_class

            if self.examples == []:
                result['examples'] = 'not provided'
            else:
                examples = []
                for example in self.examples:
                    examples.append({'id': example.id,
                                     'example': example.example})
                result['examples'] = examples

            return result

        class DetectionExample:
            def __init__(self, id: str, example: str):
                self.id = id
                self.example = example