#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow as tf


def weight_variable(shape):
    """
    Create weight variable with "tensorflow.Variable"
    Args:
        shape (list): shape of weight
    Returns:
        initial (tf.Variable)
    Usage:
        >>> weight_variable([100, 100])
    """
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    """
    Create bias variable with "tensorflow.Variable"
    Args:
        shape (list): shape of bias
    Returns:
        initial (tf.Variable)
    Usage:
        >>> bias_variable([100, 1])
    """
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def init_perceptron(dimensions):
    """
    Initial weight/bias variable of multilayer perceptron
    Args:
        dimensions (list): shape of each layer
    Returns:
        weights (list): weight variable list
        biases (list): bias variable list
    Usage:
        >>> weights, biases = init_perceptron([100, 20, 50, 1])
        >>> len(weights)
        4
        >>> len(biases)
        4
    """
    weights = []
    biases = []
    for i in range(len(dimensions) - 1):
        weights.append(weight_variable([dimensions[i], dimensions[i + 1]]))
        biases.append(bias_variable([dimensions[i + 1]]))
    return weights, biases


def multilayer_perceptron(weights, biases, input_data):
    """
    Create multilayer perceptron node for forward feeding
    Args:
        weights (list): weight variable list
        biases (list): bias variable list
        input_data (tensorflow.placeholder): numpy data
    Returns:
        out (tensorflow.Tensor): tensorflow operation node
    Usage:
        >>> out = multilayer_perceptron(weights, biases, x)
        >>> session.run(out, feed_dict={x: numpy_data})
    """
    x = input_data
    for w, b in zip(weights[:-1], biases[:-1]):
        a = tf.nn.relu(tf.add(tf.matmul(x, w), b))
        x = a
    out = tf.add(tf.matmul(x, weights[-1]), biases[-1], name="PerceptronOutput")
    return out
