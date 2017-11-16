import numpy as np
from sklearn.utils import check_array


class ActiveLearner:
	"""
	This class is an abstract model of a general active learning algorithm.
	"""
	def __init__(
			self,
			predictor, utility_function, 					# building blocks of the learner
			training_data=None, training_labels=None			# initial data if available
	):
		"""
		:param predictor: an instance of the predictor
		:param utility_function: function to calculate utilities
		:param training_data: initial training data if available
		:param training_labels: labels corresponding to the initial training data
		"""
		assert callable(utility_function), 'utility_function must be callable'

		self.predictor = predictor
		self.utility_function = utility_function
		self.training_data = check_array(training_data)
		self.training_labels = check_array(training_labels, ensure_2d=False)

		if (type(training_data) != type(None)) and (type(training_labels) != type(None)):
			self.fit_to_known()

	def calculate_utility(self, data):
		"""
		This method calls the utility function provided for ActiveLearner
		on the data passed to it. It is used to measure utilities for each
		data point.
		:param data: data points for which the utilities should be measures
		:return: utility values for each datapoint
		"""
		return self.utility_function(self.predictor, data)

	def query(self, data):
		"""
		Finds the most informative point in the data provided, then
		returns the instance and its index
		:param data:
		:return:
		"""
		utilities = self.calculate_utility(data)
		query_idx = np.argmax(utilities)
		return query_idx, data[query_idx]

	def fit_to_known(self):
		"""
		This method fits self.predictor to the training data and labels
		provided to it so far.
		"""
		self.predictor.fit(self.training_data, self.training_labels)

	def add_and_retrain(self, new_data, new_label):
		"""
		This function adds the given data to the training examples
		and retrains the predictor with the augmented dataset
		:param new_data: new training data
		:param new_label: new training labels for the data
		"""
		self.add_training_data(new_data, new_label)
		self.fit_to_known()

	def add_training_data(self, new_data, new_label):
		"""
		Adds the new data and label to the known data, but does
		not retrain the model.
		:param new_data:
		:param new_label:
		:return:
		"""
		# TODO: get rid of the if clause
		# TODO: test if this works with multiple shapes and types of data

		new_data, new_label = check_array(new_data), check_array(new_label, ensure_2d=False)
		assert len(new_data) == len(new_label), 'the number of new data points and number of labels must match'

		if type(self.training_data) != type(None):
			try:
				self.training_data = np.vstack((self.training_data, new_data))
				self.training_labels = np.concatenate((self.training_labels, new_label))
			except ValueError:
				raise ValueError('the dimensions of the new training data and label must'
								 'agree with the training data and labels provided so far')

		else:
			self.training_data = new_data
			self.training_labels = new_label

	def predict(self, data):
		"""
		Interface for the predictor
		:param data:
		:return:
		"""
		return self.predictor.predict


class Committee:
	def __init__(self):
		pass

	def vote(self):
		pass
