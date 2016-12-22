#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import random
from abc import ABCMeta, abstractmethod, abstractproperty


class Environment(metaclass=ABCMeta):

    @abstractproperty
    def state(self):
        pass

    @abstractproperty
    def actions(self):
        pass

    @abstractproperty
    def state_code(self):
        pass

    @abstractproperty
    def actions_code(self):
        pass

    @abstractmethod
    def interact(self):
        pass

    @abstractmethod
    def play(self):
        pass


class SimulatedStations(Environment):
    """
    """
    state_name = ["a_1-none","a_1-running","a_1-complete","a_1-error","a_1-a_","a_1-b1","a_1-b2","a_1-c_","a_2-none","a_2-running","a_2-complete","a_2-error","a_2-a_","a_2-b1","a_2-b2","a_2-c_","a_3-none","a_3-running","a_3-complete","a_3-error","a_3-a_","a_3-b1","a_3-b2","a_3-c_","b11-none","b11-running","b11-complete","b11-error","b11-a_","b11-b1","b11-b2","b11-c_","b12-none","b12-running","b12-complete","b12-error","b12-a_","b12-b1","b12-b2","b12-c_","b21-none","b21-running","b21-complete","b21-error","b21-a_","b21-b1","b21-b2","b21-c_","b22-none","b22-running","b22-complete","b22-error","b22-a_","b22-b1","b22-b2","b22-c_","c_1-none","c_1-running","c_1-complete","c_1-error","c_1-a_","c_1-b1","c_1-b2","c_1-c_","c_2-none","c_2-running","c_2-complete","c_2-error","c_2-a_","c_2-b1","c_2-b2","c_2-c_","c_3-none","c_3-running","c_3-complete","c_3-error","c_3-a_","c_3-b1","c_3-b2","c_3-c_","bf1-none","bf1-running","bf1-complete","bf1-error","bf1-a_","bf1-b1","bf1-b2","bf1-c_","bf2-none","bf2-running","bf2-complete","bf2-error","bf2-a_","bf2-b1","bf2-b2","bf2-c_","bf3-none","bf3-running","bf3-complete","bf3-error","bf3-a_","bf3-b1","bf3-b2","bf3-c_","bf4-none","bf4-running","bf4-complete","bf4-error","bf4-a_","bf4-b1","bf4-b2","bf4-c_","i_","o_"]
    action_name = ["bf3-a_3","bf3-a_1","bf3-a_2","bf3-b12","bf3-b11","bf3-b22","bf3-b21","bf3-c_1","bf3-c_3","bf3-c_2","bf3-o_","bf3-bf3","bf3-bf2","bf3-bf4","bf3-bf1","a_3-a_3","a_3-a_1","a_3-a_2","a_3-b12","a_3-b11","a_3-b22","a_3-b21","a_3-bf3","a_3-bf2","a_3-bf4","a_3-bf1","a_1-a_3","a_1-a_1","a_1-a_2","a_1-b12","a_1-b11","a_1-b22","a_1-b21","a_1-bf3","a_1-bf2","a_1-bf4","a_1-bf1","i_-a_3","i_-a_1","i_-a_2","i_-bf3","i_-bf2","i_-bf4","i_-bf1","bf2-a_3","bf2-a_1","bf2-a_2","bf2-b12","bf2-b11","bf2-b22","bf2-b21","bf2-c_1","bf2-c_3","bf2-c_2","bf2-o_","bf2-bf3","bf2-bf2","bf2-bf4","bf2-bf1","bf4-a_3","bf4-a_1","bf4-a_2","bf4-b12","bf4-b11","bf4-b22","bf4-b21","bf4-c_1","bf4-c_3","bf4-c_2","bf4-o_","bf4-bf3","bf4-bf2","bf4-bf4","bf4-bf1","b22-b12","b22-b11","b22-b22","b22-b21","b22-c_1","b22-c_3","b22-c_2","b22-bf3","b22-bf2","b22-bf4","b22-bf1","b21-b12","b21-b11","b21-b22","b21-b21","b21-c_1","b21-c_3","b21-c_2","b21-bf3","b21-bf2","b21-bf4","b21-bf1","c_1-c_1","c_1-c_3","c_1-c_2","c_1-bf3","c_1-bf2","c_1-bf4","c_1-bf1","c_1-o_","bf1-a_3","bf1-a_1","bf1-a_2","bf1-b12","bf1-b11","bf1-b22","bf1-b21","bf1-c_1","bf1-c_3","bf1-c_2","bf1-o_","bf1-bf3","bf1-bf2","bf1-bf4","bf1-bf1","c_3-c_1","c_3-c_3","c_3-c_2","c_3-bf3","c_3-bf2","c_3-bf4","c_3-bf1","c_3-o_","c_2-c_1","c_2-c_3","c_2-c_2","c_2-bf3","c_2-bf2","c_2-bf4","c_2-bf1","c_2-o_","b12-b12","b12-b11","b12-b22","b12-b21","b12-c_1","b12-c_3","b12-c_2","b12-bf3","b12-bf2","b12-bf4","b12-bf1","b11-b12","b11-b11","b11-b22","b11-b21","b11-c_1","b11-c_3","b11-c_2","b11-bf3","b11-bf2","b11-bf4","b11-bf1","a_2-a_3","a_2-a_1","a_2-a_2","a_2-b12","a_2-b11","a_2-b22","a_2-b21","a_2-bf3","a_2-bf2","a_2-bf4","a_2-bf1"]

    def __init__(self):
        self.reset()
        self.iteration = 1

    @classmethod
    def encode_actions(cls, actions):
        action_code_set = list()
        for action in set(actions):
            action_code = [0.0] * len(SimulatedStations.action_name)
            try:
                action_code[SimulatedStations.action_name.index(action.strip())] = 1.0
            except:
                pass
            action_code_set.append(action_code)
        return action_code_set

    @staticmethod
    def decode_actions(cls, action_code_set):
        action_set = set()
        for action_code in action_code_set:
            try:
                index = action_code.index(1)
                action_set.update([SimulatedStations.action_name[index]])
            except:
                pass
        return list(action_set)

    @property
    def state(self):
        return self.stations

    @property
    def actions(self):
        action_set = list()
        for key, sub_dict in self.stations.items():
            if sub_dict['state'][0] > 1:
                wanted = ['bf']
                if sub_dict['state'][1]['a_'] == 1:
                    if sub_dict['state'][1]['b1'] == 1 and sub_dict['state'][1]['b2'] == 0:
                        wanted.append('b2')
                    elif sub_dict['state'][1]['b2'] == 1 and sub_dict['state'][1]['b1'] == 0:
                        wanted.append('b1')
                    elif sub_dict['state'][1]['b2'] == 1 and sub_dict['state'][1]['b1'] == 1:
                        if sub_dict['state'][1]['b2'] == 1 and sub_dict['state'][1]['b1'] == 1 and sub_dict['state'][1]['c_'] == 1:
                            wanted.append('o_')
                        else:
                            wanted.append('c_')
                    else:
                        wanted.append('b1')
                        wanted.append('b2')
                else:
                    wanted.append('a_')

                for s_type in sub_dict['next'].keys():
                    for n in [n for n in self.stations.keys() if s_type in n and s_type in wanted]:
                        if self.stations[n]['state'][0] == 0:
                            action = key + '-' + n
                            action_set.append(action)
                    if sub_dict['state'][0] == 3:
                            action = key + '-' + key
                            action_set.append(action)

        if self.stations['i_']['state'][0] > 0:
            for s_type in self.stations['i_']['next'].keys():
                for n in [n for n in self.stations.keys() if s_type in n]:
                    if self.stations[n]['state'][0] == 0:
                        action = 'i_-' + n
                        action_set.append(action)
        return list(set(action_set))

    @property
    def state_code(self):
        state = [0] * len(SimulatedStations.state_name)

        for name in self.stations.keys():
            if name not in ['i_', 'o_']:
                if self.stations[name]['state'][0] == 0:
                    index = SimulatedStations.state_name.index(name + "-none")
                    state[index] = 1
                else:
                    if self.stations[name]['state'][0] == 1:
                        index = SimulatedStations.state_name.index(name + "-running")
                        state[index] = 1
                    elif self.stations[name]['state'][0] == 2:
                        index = SimulatedStations.state_name.index(name + "-complete")
                        state[index] = 1
                    else:
                        index = SimulatedStations.state_name.index(name + "-error")
                        state[index] = 1
                    index = SimulatedStations.state_name.index(name + "-a_")
                    state[index] = self.stations[name]['state'][1]['a_']
                    index = SimulatedStations.state_name.index(name + "-b1")
                    state[index] = self.stations[name]['state'][1]['b1']
                    index = SimulatedStations.state_name.index(name + "-b2")
                    state[index] = self.stations[name]['state'][1]['b2']
                    index = SimulatedStations.state_name.index(name + "-c_")
                    state[index] = self.stations[name]['state'][1]['c_']
        if self.stations['i_']['state'][0] == 1:
            index = SimulatedStations.state_name.index("i_")
            state[index] = 1
        if self.stations['o_']['state'][0] == 1:
            index = SimulatedStations.state_name.index("o_")
            state[index] = 1
        return state

    @property
    def actions_code(self):
        return SimulatedStations.encode_actions(self.actions)

    def interact(self, action):
        # Split action
        source = action.split('-')[0]
        destination = action.split('-')[1]
        # Move target to destination
        self.stations[destination]['state'][0] = 1
        self.stations[destination]['state'][1] = copy.copy(self.stations[source]['state'][1])
        # Assign waiting time
        try:
            self.stations[destination]['time'] = random.sample(range(self.stations[destination]['range'][0], self.stations[destination]['range'][1]), 1)[0]
        except:
            self.stations[destination]['time'] = 0
        # Reset source
        self.stations[source]['state'][0] = 0
        self.stations[source]['state'][1] = {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}
        # Reset input
        if source != 'i_':
            self.stations[source]['time'] = 0
        # Set iteration
        self.iteration = self.stations[source]['next'][destination[:2]]

    def play(self):
        # Process input & output
        self.stations['i_']['time'] -= self.iteration
        self.stations['o_']['time'] -= self.iteration
        if self.stations['i_']['time'] <= 0:
            self.stations['i_']['state'] = [1, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}]
            self.stations['i_']['time'] = random.sample(range(self.stations['i_']['range'][0], self.stations['i_']['range'][1]), 1)[0]
        if self.stations['o_']['time'] <= 0:
            self.stations['o_']['state'] = [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}]
        # Process other stations
        for key, sub_dict in self.stations.items():
            if key[:2] not in ['i_', 'o_', 'bf']:
                if sub_dict['state'][0] > 0:
                    if sub_dict['state'][0] == 1:
                        sub_dict['time'] -= self.iteration
                        if sub_dict['time'] <= 0:
                            if random.random() > 0.8:
                                sub_dict['state'][0] = 3
                            else:
                                sub_dict['state'][0] = 2
                                sub_dict['state'][1][key[:2]] = 1
                    sub_dict['state'][1]['during'] += self.iteration
            if key[:2] == 'bf' and sub_dict['state'][0] == 1:
                sub_dict['state'][0] = 2
        # Reset iteration
        self.iteration = 1

    def reset(self):
        self.stations = {
            'i_': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 15,
                'range': [5, 10],
                'next': {'a_': 1, 'bf': 3},
            },
            'a_1': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 5,
                'range': [5, 10],
                'next': {'a_': 1, 'b1': 1, 'b2': 2, 'bf': 3},
            },
            'a_2': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 5,
                'range': [5, 10],
                'next': {'a_': 1, 'b1': 1, 'b2': 2, 'bf': 3},
            },
            'a_3': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 5,
                'range': [5, 10],
                'next': {'a_': 1, 'b1': 1, 'b2': 2, 'bf': 3},
            },
            'b11': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 10,
                'range': [10, 13],
                'next': {'b1': 1, 'b2': 1, 'c_': 3, 'bf': 2},
            },
            'b12': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 10,
                'range': [10, 13],
                'next': {'b1': 1, 'b2': 1, 'c_': 3, 'bf': 2},
            },
            'b21': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 7,
                'range': [5, 8],
                'next': {'b1': 1, 'b2': 1, 'c_': 3, 'bf': 2},
            },
            'b22': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 7,
                'range': [5, 8],
                'next': {'b1': 1, 'b2': 1, 'c_': 3, 'bf': 2},
            },
            'c_1': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 20,
                'range': [16, 22],
                'next': {'c_': 1, 'bf': 3, 'o_': 1},
            },
            'c_2': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 20,
                'range': [16, 22],
                'next': {'c_': 1, 'bf': 3, 'o_': 1},
            },
            'c_3': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 20,
                'range': [16, 22],
                'next': {'c_': 1, 'bf': 3, 'o_': 1},
            },
            'bf1': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 0,
                'range': [1, 2],
                'next': {'a_': 3, 'b1': 2, 'b2': 1, 'c_': 3, 'o_': 3},
            },
            'bf2': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 0,
                'range': [1, 2],
                'next': {'a_': 3, 'b1': 2, 'b2': 1, 'c_': 3, 'o_': 3},
            },
            'bf3': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 0,
                'range': [1, 2],
                'next': {'a_': 3, 'b1': 2, 'b2': 1, 'c_': 3, 'o_': 3},
            },
            'bf4': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 0,
                'range': [1, 2],
                'next': {'a_': 3, 'b1': 2, 'b2': 1, 'c_': 3, 'o_': 3},
            },
            'o_': {
                'state': [0, {'a_': 0, 'b1': 0, 'b2': 0, 'c_': 0, 'during': 0}],
                'time': 15,
                'range': [10, 15],
                'next': {},
            },
        }
