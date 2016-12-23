#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from .qnetwork import *


class TaskScheduler(object):
    """
    Args:
    Returns:
    Usage:
        >>> agent = TaskScheduler([], "")
        >>> agent.save()
        >>> agent.restore()
        >>> agent.train_QNetwork()
    """
    def __init__(self, dimensions, ckpt_file, discount=0.9):
        # Set attributes
        self.dimensions = dimensions
        self.discount = discount
        self.ckpt_file = ckpt_file
        # Set placeholder for tensroflow input
        self.x = tf.placeholder(
            tf.float32, [None, self.dimensions[0]], name="X"
        )
        self.next_x = tf.placeholder(
            tf.float32, [None, self.dimensions[0]], name="NextX"
        )
        self.next_value  = tf.placeholder(
            tf.float32, [None, 1], name="NextValue"
        )
        self.reward = tf.placeholder(
            tf.float32, [None, 1], name="Reward"
        )
        # Initial tensorflow variables
        self.weights, self.biases = init_perceptron(dimensions)
        # Initial tensorflow operation node
        self._create_q_op()
        self._create_max_op()
        self._create_loss_op()
        self._create_training_op()
        # Initial saver object
        self.saver = tf.train.Saver()
        # Initial session for agent
        self.session = tf.Session()
        # Initial above variables
        self.session.run(tf.initialize_all_variables())

    def save(self):
        self.saver.save(self.session, self.ckpt_file)

    def restore(self):
        self.saver.restore(self.session, self.ckpt_file)

    def get_loss(self, x, rewards, next_x):
        next_values = self._get_next_value(next_x, rewards)
        loss_value = self.session.run(self.loss_op, feed_dict={
            self.x: x, self.reward: rewards, self.next_value: next_values
        })
        return loss_value

    def get_Q(self, x):
        return self.session.run(self.q_op, feed_dict={self.x: x})

    def train_QNetwork(self, x, rewards, next_x):
        next_values = self._get_next_value(next_x, rewards)
        self.session.run(self.train_op, feed_dict={
            self.x: x, self.reward: rewards, self.next_value: next_values
        })

    def _create_q_op(self):
        """
        Create q_op, next_q_op for getting q value
        """
        self.q_op = multilayer_perceptron(self.weights, self.biases, self.x)
        self.next_q_op = multilayer_perceptron(self.weights, self.biases, self.next_x)

    def _create_max_op(self):
        """
        Create max_nextq_op for getting max q value
        """
        self.next_max_op = tf.reduce_max(self.next_q_op, name="NextMaxQ")

    def _create_loss_op(self):
        """
        Create loss_op for computing loss
        """
        self.loss_op = tf.div(tf.square(tf.sub(self.next_value, self.q_op)), 2, name="Loss")

    def _create_training_op(self):
        """
        Create train_op for training process
        """
        self.train_op = tf.train.AdamOptimizer(1e-4).minimize(self.loss_op)

    def _get_next_value(self, next_x, rewards):
        """
        Args:
            next_x (numpy data):
            rewards (numpy data):
        Returns:
            values (list): next state value
        """
        values = list()
        for x_, r in zip(next_x, rewards):
            q_ = self.session.run(self.next_max_op, feed_dict={self.next_x: x_})
            if r[0] != -100:
                values.append(r + self.discount * q_)
            else:
                values.append(r)
        return values
