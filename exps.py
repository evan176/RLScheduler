#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import math
import time
import numpy
import random
from simulation import SimulatedStations, TaskScheduler


def save_experience(state_code, action, reward, next_state_code, next_actions):
    with open("experience.txt", "a") as f:
        temp1 = ','.join([str(s) for s in state_code])
        temp2 = ','.join([str(s) for s in next_state_code])
        try:
            temp3 = ','.join([str(s) for s in next_actions])
        except:
            temp3 = ''
        temp = '::'.join([temp1, action, str(reward), temp2, temp3])
        f.write(temp + "\n")


def load_experience():
    with open("experience.txt", "r") as f:
        records = f.readlines()
    pos_exps = list()
    zero_exps = list()
    neg_exps = list()
    for record in records:
        state_code = [float(item) for item in record.split('::')[0].split(',')]
        action = record.split('::')[1]
        reward = float(record.split('::')[2])
        next_state_code = [float(item) for item in record.split('::')[3].split(',')]
        next_actions = record.split('::')[4].split(',')
        if reward == 100:
            pos_exps.append({
                'state_code': state_code, 'action': action, 'reward': reward,
                'next_state_code': next_state_code, 'next_actions': next_actions
            })
        elif reward == -100:
            neg_exps.append({
                'state_code': state_code, 'action': action, 'reward': reward,
                'next_state_code': next_state_code, 'next_actions': next_actions
            })
        else:
            zero_exps.append({
                'state_code': state_code, 'action': action, 'reward': reward,
                'next_state_code': next_state_code, 'next_actions': next_actions
            })

    minimum = min(len(pos_exps), len(neg_exps), len(zero_exps), 500)
    experiences = random.sample(pos_exps, minimum) + random.sample(neg_exps, minimum) + random.sample(zero_exps, minimum)
    return experiences 


"""
def load_experience():
    with open("experience.txt", "r") as f:
        records = f.readlines()
    records = random.sample(records, min(int(len(records) / 10), 1000))
    experiences = list()
    for record in records:
        state_code = [float(item) for item in record.split('::')[0].split(',')]
        action = record.split('::')[1]
        reward = float(record.split('::')[2])
        next_state_code = [float(item) for item in record.split('::')[3].split(',')]
        next_actions = record.split('::')[4].split(',')
        experiences.append({
            'state_code': state_code, 'action': action, 'reward': reward,
            'next_state_code': next_state_code, 'next_actions': next_actions
        })
    return experiences 
"""


"""
def get_reward(action, deadlock_flag):
    try:
        temp = action.split('-')[1]
    except:
        temp = ''
    if temp == 'o_':
        return 100
    elif deadlock_flag > 15:
        return -100
    else:
        return 0
"""

def get_reward(environment, action, deadlock_flag, iteration_flag):
    source = action.split('-')[0]
    destination = action.split('-')[1]
    if destination == 'o_':
        return 100
    elif deadlock_flag > 15:
        return -100
    else:
        return -iteration_flag


def show_state(stations):
    haha = "\
                     {4} {5} \n\
      {0}      {1} {2} {3}          {8}{9}{10}       {15}\n\
                     {6} {7}                      \n\
                   {11} {12} {13} {14}               \n\
    ".format(
        stations['i_']['state'][0],
        stations['a_1']['state'][0],
        stations['a_2']['state'][0],
        stations['a_3']['state'][0],
        stations['b11']['state'][0],
        stations['b12']['state'][0],
        stations['b21']['state'][0],
        stations['b22']['state'][0],
        stations['c_1']['state'][0],
        stations['c_2']['state'][0],
        stations['c_3']['state'][0],
        stations['bf1']['state'][0],
        stations['bf2']['state'][0],
        stations['bf3']['state'][0],
        stations['bf4']['state'][0],
        stations['o_']['state'][0],
    )
    print(haha)


def e_greedy(random_prob, state_code, actions, actions_code):
    action = '' 
    # E-Greedy
    if random.random() <= random_prob:
        try:
            action = random.sample(actions, 1)[0]
        except:
            pass
    else:
        inputs = list()
        for a in actions_code:
            inputs.append(state_code + a)
        if inputs:
            q = agent.get_Q(inputs)
            index = numpy.argmax(q, axis=0)[0]
            action = actions[index]
    return action


def update_model(agent):
    x_list = []
    reward_list = []
    next_x_list = []

    for record in load_experience():
        x_list.append(record['state_code'] + SimulatedStations.encode_actions([record['action']])[0])
        reward_list.append([record['reward']])

        nx = []
        for a in SimulatedStations.encode_actions(record['next_actions']):
            nx.append(record['next_state_code'] + a)
        next_x_list.append(nx)
    if x_list:
        agent.train_QNetwork(x_list, reward_list, next_x_list)
    return agent


def episode(environment, agent, random_prob, decay):
    environment.reset()

    # Skip initial input
    while len(environment.actions) <= 0:
        environment.play()

    # First movement
    current_state_code = environment.state_code
    current_actions = environment.actions
    current_actions_code = environment.actions_code
    action = e_greedy(random_prob, current_state_code, current_actions, current_actions_code)
    environment.interact(action)
    random_prob = random_prob * decay
    environment.play()

    counter = 0
    cumulated_work = 0
    deadlock_flag = 0
    iteration_flag = environment.iteration
    while counter < 2000:
        # Get new state
        next_state_code = environment.state_code
        # Get new action
        next_actions = environment.actions
        next_actions_code = environment.actions_code

        if next_actions:
            # show_state(environment.state)
            # Get reward in new state
            reward = get_reward(environment, action, deadlock_flag, iteration_flag)
            if reward == 100:
                cumulated_work += 1

            # Save experience
            if not deadlock_flag:
                save_experience(current_state_code, action, reward, next_state_code, next_actions)
            # Assign next to current
            current_state_code = next_state_code
            current_actions = next_actions
            current_actions_code = next_actions_code
            # Get action in current state
            action = e_greedy(random_prob, current_state_code, current_actions, current_actions_code)
            # Interact with environment
            environment.interact(action)
            random_prob = max(random_prob * decay, 0.05)

            deadlock_flag = 0
            iteration_flag = environment.iteration
        else:
            deadlock_flag += 1
            iteration_flag += 1

        # Return while deadlock
        if deadlock_flag > 15:
            save_experience(current_state_code, action, -100, next_state_code, next_actions)
            return random_prob, counter, cumulated_work

        # Iterate
        environment.play()

        counter += 1
        if counter % 50 == 0:
            agent = update_model(agent)
            agent.save()

    return random_prob, counter, cumulated_work


if __name__ == "__main__":
    random_prob = 1
    # random_prob = 0.05
    decay = 0.999

    environment = SimulatedStations()
    input_size = len(environment.state_name) + len(environment.action_name)
    agent = TaskScheduler(
        dimensions=[
            input_size,
            input_size,
            input_size,
            input_size,
            1
        ],
        ckpt_file="saved_network/agent.ckpt",
        discount=0.9
    )
    # agent.restore()

    for i in range(100):
        random_prob, counter, cumulated_work = episode(environment, agent, random_prob, decay)
        print("{}: {} - {}".format(random_prob, counter, cumulated_work))
