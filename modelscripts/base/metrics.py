# coding=utf-8
from typing import List
from collections import OrderedDict

class Metric(object):

    def __init__(self, label, n, plural=None):
        self.n=n
        self.label=label
        self.plural=plural

    def __str__(self):
        if self.n==0:
            return 'no '+self.label
        elif self.n==1:
            return '1 '+self.label
        else:
            return '%s %s' % (
                str(self.n),
                self.plural if self.plural is not None
                            else self.label+'s')

class Metrics(object):

    def __init__(self):
        self.metricNamed = OrderedDict()

    @property
    def all(self):
        return self.metricNamed.values()

    def add(self, metric):
        #type: (Metric)->Metrics
        self.metricNamed[metric.label]=metric
        return self

    def addList(self, labelAndValues):
        for (l,v) in labelAndValues:
            self.add(Metric(label=l, n=v))
        return self

    def addMetrics(self, metrics):
        #type: (Metrics)->Metrics
        for metric in metrics.all:
            self.add(metric)
        return self

    def accumulate(self, metricsList):
        #type: (List[Metrics])->Metrics
        """
        Increment all metric with the values in the given
        metrics. Add metric entry in case of new metric.
        """
        for metrics in metricsList:
            for metric in metrics.all:
                if metric.label in self.metricNamed:
                    # the metric exists, add the new value
                    self.metricNamed[metric.label]+=\
                        metric.n
                else:
                    self.metricNamed[metric.label]=metric.n

    def __str__(self):
        return ''.join(
            [str(m)+'\n' for m in self.all])