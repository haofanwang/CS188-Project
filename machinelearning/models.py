import numpy as np

import backend
import nn

class Model(object):
    """Base model class for the different applications"""
    def __init__(self):
        self.get_data_and_monitor = None
        self.learning_rate = 0.0

    def run(self, x, y=None):
        raise NotImplementedError("Model.run must be overriden by subclasses")

    def train(self):
        """
        Train the model.

        `get_data_and_monitor` will yield data points one at a time. In between
        yielding data points, it will also monitor performance, draw graphics,
        and assist with automated grading. The model (self) is passed as an
        argument to `get_data_and_monitor`, which allows the monitoring code to
        evaluate the model on examples from the validation set.
        """
        for x, y in self.get_data_and_monitor(self):
            graph = self.run(x, y)
            graph.backprop()
            graph.step(self.learning_rate)

class RegressionModel(Model):
    """
    A neural network model for app roximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        Model.__init__(self)
        self.get_data_and_monitor = backend.get_data_and_monitor_regression

        # Remember to set self.learning_rate!
        # You may use any learning rate that works well for your architecture
        "*** YOUR CODE HERE ***"
        self.learning_rate = 1
        self.graph = None

    def run(self, x, y=None):
        """
        Runs the model for a batch of examples.

        The correct outputs `y` are known during training, but not at test time.
        If correct outputs `y` are provided, this method must construct and
        return a nn.Graph for computing the training loss. If `y` is None, this
        method must instead return predicted y-values.

        Inputs:
            x: a (batch_size x 1) numpy array
            y: a (batch_size x 1) numpy array, or None
        Output:
            (if y is not None) A nn.Graph instance, where the last added node is
                the loss
            (if y is None) A (batch_size x 1) numpy array of predicted y-values

        Note: DO NOT call backprop() or step() inside this method!
        """
        "*** YOUR CODE HERE ***"
        if y is not None:
            # At training time, the correct output `y` is known.
            # Here, you should construct a loss node, and return the nn.Graph
            # that the node belongs to. The loss node must be the last node
            # added to the graph.
            "*** YOUR CODE HERE ***"
            w1 = nn.Variable(len(x)//4,len(x)//4)
            w2 = nn.Variable(len(x)//4,len(x)//4)
            w3 = nn.Variable(len(x)//4,len(x)//4)
            w4 = nn.Variable(len(x)//4,len(x)//4)
            w5 = nn.Variable(len(x)//4,len(x)//4)
            w6 = nn.Variable(len(x)//4,len(x)//4)
            w7 = nn.Variable(len(x)//4,len(x)//4)
            w8 = nn.Variable(len(x)//4,len(x)//4)
            b1 = nn.Variable(len(x)//4,1)
            b2 = nn.Variable(len(x)//4,1)
            b3 = nn.Variable(len(x)//4,1)
            b4 = nn.Variable(len(x)//4,1)
            b5 = nn.Variable(len(x)//4,1)
            b6 = nn.Variable(len(x)//4,1)
            b7 = nn.Variable(len(x)//4,1)
            b8 = nn.Variable(len(x)//4,1)

            self.graph = nn.Graph([w1,w2,w3,w4,w5,w6,w7,w8,b1,b2,b3,b4,b5,b6,b7,b8])

            input_x = nn.Input(self.graph,x)
            input_y = nn.Input(self.graph,y)

            x1 = nn.Input(self.graph,x[:len(x)//4])
            x2 = nn.Input(self.graph,x[len(x)//4:len(x)//2])
            x3 = nn.Input(self.graph,x[len(x)//2:3*len(x)//4])
            x4 = nn.Input(self.graph,x[3*len(x)//4:])

            mult1 = nn.MatrixMultiply(self.graph, w1, x1)
            mult2 = nn.MatrixMultiply(self.graph, w2, x2)
            mult3 = nn.MatrixMultiply(self.graph, w3, x3)
            mult4 = nn.MatrixMultiply(self.graph, w4, x4)

            add1 = nn.MatrixVectorAdd(self.graph, mult1, mult2)
            add2 = nn.MatrixVectorAdd(self.graph, mult2, mult1)
            add3 = nn.MatrixVectorAdd(self.graph, add1, b1)
            add4 = nn.MatrixVectorAdd(self.graph, add2, b2)

            add5 = nn.MatrixVectorAdd(self.graph, mult3, mult4)
            add6 = nn.MatrixVectorAdd(self.graph, mult4, mult3)
            add7 = nn.MatrixVectorAdd(self.graph, add5, b3)
            add8 = nn.MatrixVectorAdd(self.graph, add6, b4)

            relu1 = nn.ReLU(self.graph, add3)
            relu2 = nn.ReLU(self.graph, add4)
            relu3 = nn.ReLU(self.graph, add7)
            relu4 = nn.ReLU(self.graph, add8)

            mult5 = nn.MatrixMultiply(self.graph, w5, relu1)
            mult6 = nn.MatrixMultiply(self.graph, w6, relu2)
            mult7 = nn.MatrixMultiply(self.graph, w7, relu3)
            mult8 = nn.MatrixMultiply(self.graph, w8, relu4)

            add9 = nn.MatrixVectorAdd(self.graph, mult5, mult6)
            add10 = nn.MatrixVectorAdd(self.graph, mult6, mult5)
            add11 = nn.MatrixVectorAdd(self.graph, add9, b5)
            add12 = nn.MatrixVectorAdd(self.graph, add10, b6)

            add13 = nn.MatrixVectorAdd(self.graph, mult7, mult8)
            add14 = nn.MatrixVectorAdd(self.graph, mult8, mult7)
            add15 = nn.MatrixVectorAdd(self.graph, add13, b7)
            add16 = nn.MatrixVectorAdd(self.graph, add14, b8)

            y1 = nn.Input(self.graph,y[:len(y)//4])
            y2 = nn.Input(self.graph,y[len(y)//4:len(y)//2])
            y3 = nn.Input(self.graph,y[len(y)//2:3*len(y)//4])
            y4 = nn.Input(self.graph,y[3*len(y)//4:])

            loss1 = nn.SquareLoss(self.graph, add7, y1)
            loss2 = nn.SquareLoss(self.graph, add8, y2)
            loss3 = nn.SquareLoss(self.graph, add8, y3)
            loss4 = nn.SquareLoss(self.graph, add8, y4)

            add17 = nn.Add(self.graph, loss1, loss2)
            add17 = nn.Add(self.graph, add17, loss3)
            add17 = nn.Add(self.graph, add17, loss4)
            #print "y4"
            #print y4.data
            #print "y"
            #print input_y.data
            return self.graph

        else:
            # At test time, the correct output is unknown.
            # You should instead return your model's prediction as a numpy array
            vec1 = self.graph.get_output(self.graph.get_nodes()[-11])
            vec2 = self.graph.get_output(self.graph.get_nodes()[-10])
            vec3 = self.graph.get_output(self.graph.get_nodes()[-9])
            vec4 = self.graph.get_output(self.graph.get_nodes()[-8])
            out = np.concatenate((vec1, vec2), axis=0)
            out = np.concatenate((out, vec3), axis=0)
            out = np.concatenate((out, vec4), axis=0)

            return out



class OddRegressionModel(Model):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers.

    Unlike RegressionModel, the OddRegressionModel must be structurally
    constrained to represent an odd function, i.e. it must always satisfy the
    property f(x) = -f(-x) at all points during training.
    """
    def __init__(self):
        Model.__init__(self)
        self.get_data_and_monitor = backend.get_data_and_monitor_regression

        # Remember to set self.learning_rate!
        # You may use any learning rate that works well for your architecture
        "*** YOUR CODE HERE ***"
        self.learning_rate = 0.1
        self.graph = None
        self.list = []

    def run(self, x, y=None):
        """
        Runs the model for a batch of examples.

        The correct outputs `y` are known during training, but not at test time.
        If correct outputs `y` are provided, this method must construct and
        return a nn.Graph for computing the training loss. If `y` is None, this
        method must instead return predicted y-values.

        Inputs:
            x: a (batch_size x 1) numpy array
            y: a (batch_size x 1) numpy array, or None
        Output:
            (if y is not None) A nn.Graph instance, where the last added node is
                the loss
            (if y is None) A (batch_size x 1) numpy array of predicted y-values

        Note: DO NOT call backprop() or step() inside this method!
        """
        "*** YOUR CODE HERE ***"
        n = 4
        if not self.graph:
                w1 = nn.Variable(1, 50)
                w2 = nn.Variable(50, 50)
                w3 = nn.Variable(50, 1)
                b1 = nn.Variable(1, 50)
                b2 = nn.Variable(1, 50)
                b3 = nn.Variable(1, 1)
                self.list = [w1,w2,w3,b1,b2,b3]
                self.graph = nn.Graph(self.list)
        self.graph = nn.Graph(self.list)
        input_x = nn.Input(self.graph,x)
        if y is not None:
            input_y = nn.Input(self.graph,y)
        input_neg = nn.Input(self.graph, np.matrix([-1.]))
        mult = nn.MatrixMultiply(self.graph, input_x, self.list[0])
        add = nn.MatrixVectorAdd(self.graph, mult, self.list[3])
        relu = nn.ReLU(self.graph, add)
        mult2 = nn.MatrixMultiply(self.graph, relu, self.list[1])
        add2 = nn.MatrixVectorAdd(self.graph, mult2, self.list[4])
        relu2 = nn.ReLU(self.graph, add2)
        mult3 = nn.MatrixMultiply(self.graph, relu2, self.list[2])
        add3 = nn.MatrixVectorAdd(self.graph, mult3, self.list[5])
        ad = add3

        neg = nn.MatrixMultiply(self.graph, input_x, input_neg)
        mult = nn.MatrixMultiply(self.graph, neg, self.list[0])
        add = nn.MatrixVectorAdd(self.graph, mult, self.list[3])
        relu = nn.ReLU(self.graph, add)
        mult2 = nn.MatrixMultiply(self.graph, relu, self.list[1])
        add2 = nn.MatrixVectorAdd(self.graph, mult2, self.list[4])
        relu2 = nn.ReLU(self.graph, add2)
        mult3 = nn.MatrixMultiply(self.graph, relu2, self.list[2])
        add3 = nn.MatrixVectorAdd(self.graph, mult3, self.list[5])
        sb = nn.MatrixMultiply(self.graph, add3, input_neg)

        # f(x) = g(x)-g(-x)
        sub = nn.MatrixVectorAdd(self.graph, ad, sb)


        if y is not None:
            # At training time, the correct output y is known.
            # Here, you should construct a loss node, and return the nn.Graph
            # that the node belongs to. The loss node must be the last node
            # added to the graph.

            loss = nn.SquareLoss(self.graph, sub, input_y)
            return self.graph
        else:
            # At test time, the correct output is unknown.
            # You should instead return your model's prediction as a numpy array

            return self.graph.get_output(self.graph.get_nodes()[-1])



class DigitClassificationModel(Model):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        Model.__init__(self)
        self.get_data_and_monitor = backend.get_data_and_monitor_digit_classification

        # Remember to set self.learning_rate!
        # You may use any learning rate that works well for your architecture
        "*** YOUR CODE HERE ***"
        self.learning_rate = 0.2
        self.graph = None

    def run(self, x, y=None):
        """
        Runs the model for a batch of examples.

        The correct labels are known during training, but not at test time.
        When correct labels are available, `y` is a (batch_size x 10) numpy
        array. Each row in the array is a one-hot vector encoding the correct
        class.

        Your model should predict a (batch_size x 10) numpy array of scores,
        where higher scores correspond to greater probability of the image
        belonging to a particular class. You should use `nn.SoftmaxLoss` as your
        training loss.

        Inputs:
            x: a (batch_size x 784) numpy array
            y: a (batch_size x 10) numpy array, or None
        Output:
            (if y is not None) A nn.Graph instance, where the last added node is
                the loss
            (if y is None) A (batch_size x 10) numpy array of scores (aka logits)
        """
        "*** YOUR CODE HERE ***"

        if len(x) == 1:
            return 0

        if not self.graph:
                w1 = nn.Variable(784, 500)
                w2 = nn.Variable(500, 500)
                w3 = nn.Variable(500, 10)
                b1 = nn.Variable(1, 500)
                b2 = nn.Variable(1, 500)
                b3 = nn.Variable(1, 10)
                self.l = [w1,w2,w3,b1,b2,b3]
                self.graph = nn.Graph(self.l)

        self.graph = nn.Graph(self.l)
        input_x = nn.Input(self.graph,x)

        if y is not None:
            input_y = nn.Input(self.graph,y)

        mult = nn.MatrixMultiply(self.graph, input_x, self.l[0])
        add = nn.MatrixVectorAdd(self.graph, mult, self.l[3])
        relu = nn.ReLU(self.graph, add)
        mult2 = nn.MatrixMultiply(self.graph, relu, self.l[1])
        add2 = nn.MatrixVectorAdd(self.graph, mult2, self.l[4])
        relu2 = nn.ReLU(self.graph, add2)
        mult3 = nn.MatrixMultiply(self.graph, relu2, self.l[2])
        add3 = nn.MatrixVectorAdd(self.graph, mult3, self.l[5])
        if y is not None:
            # At training time, the correct output `y` is known.
            # Here, you should construct a loss node, and return the nn.Graph
            # that the node belongs to. The loss node must be the last node
            # added to the graph.
            loss = nn.SoftmaxLoss(self.graph, add3, input_y)
            return self.graph
        else:
            # At test time, the correct output is unknown.
            # You should instead return your model's prediction as a numpy array
            return self.graph.get_output(self.graph.get_nodes()[-1])

class DeepQModel(Model):
    """
    A model that uses a Deep Q-value Network (DQN) to approximate Q(s,a) as part
    of reinforcement learning.

    (We recommend that you implement the RegressionModel before working on this
    part of the project.)
    """
    def __init__(self):
        Model.__init__(self)
        self.get_data_and_monitor = backend.get_data_and_monitor_rl

        self.num_actions = 2
        self.state_size = 4

        # Remember to set self.learning_rate!
        # You may use any learning rate that works well for your architecture
        "*** YOUR CODE HERE ***"
        self.learning_rate = 0.01
        self.graph = None

    def run(self, states, Q_target=None):
        """
        Runs the DQN for a batch of states.

        The DQN takes the state and computes Q-values for all possible actions
        that can be taken. That is, if there are two actions, the network takes
        as input the state s and computes the vector [Q(s, a_1), Q(s, a_2)]

        When Q_target == None, return the matrix of Q-values currently computed
        by the network for the input states.

        When Q_target is passed, it will contain the Q-values which the network
        should be producing for the current states. You must return a nn.Graph
        which computes the training loss between your current Q-value
        predictions and these target values, using nn.SquareLoss.

        Inputs:
            states: a (batch_size x 4) numpy array
            Q_target: a (batch_size x 2) numpy array, or None
        Output:
            (if Q_target is not None) A nn.Graph instance, where the last added
                node is the loss
            (if Q_target is None) A (batch_size x 2) numpy array of Q-value
                scores, for the two actions
        """
        "*** YOUR CODE HERE ***"

        if not self.graph:
            w1 = nn.Variable(4, 50)
            w2 = nn.Variable(50, 50)
            w3 = nn.Variable(50, 2)
            b1 = nn.Variable(1, 50)
            b2 = nn.Variable(1, 50)
            b3 = nn.Variable(1, 2)
            self.list = [w1,w2,w3,b1,b2,b3]
            self.graph = nn.Graph(self.l)

        self.graph = nn.Graph(self.l)
        input_x = nn.Input(self.graph,states)

        if Q_target is not None:
            input_y = nn.Input(self.graph, Q_target)

        mult = nn.MatrixMultiply(self.graph, input_x, self.list[0])
        add = nn.MatrixVectorAdd(self.graph, mult, self.list[3])
        relu = nn.ReLU(self.graph, add)
        mult2 = nn.MatrixMultiply(self.graph, relu, self.list[1])
        add2 = nn.MatrixVectorAdd(self.graph, mult2, self.list[4])
        relu2 = nn.ReLU(self.graph, add2)
        mult3 = nn.MatrixMultiply(self.graph, relu2, self.list[2])
        add3 = nn.MatrixVectorAdd(self.graph, mult3, self.list[5])

        if Q_target is not None:
            "* YOUR CODE HERE *"
            loss = nn.SquareLoss(self.graph, add3, input_y)
            return self.graph
        else:
            "* YOUR CODE HERE *"
            return self.graph.get_output(self.graph.get_nodes()[-1])

    def get_action(self, state, eps):
        """
        Select an action for a single state using epsilon-greedy.

        Inputs:
            state: a (1 x 4) numpy array
            eps: a float, epsilon to use in epsilon greedy
        Output:
            the index of the action to take (either 0 or 1, for 2 actions)
        """
        if np.random.rand() < eps:
            return np.random.choice(self.num_actions)
        else:
            scores = self.run(state)
            return int(np.argmax(scores))


class LanguageIDModel(Model):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        Model.__init__(self)
        self.get_data_and_monitor = backend.get_data_and_monitor_lang_id

        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Remember to set self.learning_rate!
        # You may use any learning rate that works well for your architecture
        "*** YOUR CODE HERE ***"

    def run(self, xs, y=None):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        (batch_size x self.num_chars) numpy array, where every row in the array
        is a one-hot vector encoding of a character. For example, if we have a
        batch of 8 three-letter words where the last word is "cat", we will have
        xs[1][7,0] == 1. Here the index 0 reflects the fact that the letter "a"
        is the inital (0th) letter of our combined alphabet for this task.

        The correct labels are known during training, but not at test time.
        When correct labels are available, `y` is a (batch_size x 5) numpy
        array. Each row in the array is a one-hot vector encoding the correct
        class.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node that represents a (batch_size x hidden_size)
        array, for your choice of hidden_size. It should then calculate a
        (batch_size x 5) numpy array of scores, where higher scores correspond
        to greater probability of the word originating from a particular
        language. You should use `nn.SoftmaxLoss` as your training loss.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a (batch_size x self.num_chars) numpy array
            y: a (batch_size x 5) numpy array, or None
        Output:
            (if y is not None) A nn.Graph instance, where the last added node is
                the loss
            (if y is None) A (batch_size x 5) numpy array of scores (aka logits)

        Hint: you may use the batch_size variable in your code
        """
        batch_size = xs[0].shape[0]

        "*** YOUR CODE HERE ***"

        if y is not None:
            "*** YOUR CODE HERE ***"
        else:
            "*** YOUR CODE HERE ***"
