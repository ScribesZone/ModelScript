# coding=utf-8
"""Metrics"""

__all__ = (
    'Metric',
    'Metrics'
)

from typing import List, Dict, Any, Optional, Iterable, Tuple
from collections import OrderedDict


class Metric(object):
    """A metric, basically an integer associated with a label."""

    label: str
    n: int
    plural: Optional[str]

    def __init__(self, label, n, plural=None):
        self.label = label
        self.n = n
        self.plural = plural

    def add(self, n):
        """Add a value to the metric."""
        self.n += n
        return self

    @property
    def _pair(self):
        if self.n == 0:
            return ('no', self.label)
        elif self.n == 1:
            return ('1', self.label)
        else:
            return (
                str(self.n),
                self.plural if self.plural is not None
                            else self.label+'s')

    def __str__(self):
        return '%s %s' % self._pair

    def __repr__(self):
        return '<"%s",%i>' % (self.label, self.n)


class Metrics(object):
    """Collections of metrics."""

    metricNamed: Dict[str, Metric]

    def __init__(self):
        self.metricNamed = OrderedDict()

    @property
    def all(self):
        """All metrics."""
        return list(self.metricNamed.values())

    def add(self, metric: Metric) -> 'Metrics':
        """Add a metric."""
        if metric.label not in self.metricNamed:
            self.metricNamed[metric.label] = \
                Metric(metric.label, 0)
        self.metricNamed[metric.label].add(metric.n)
        return self

    def addList(self,
                labelsAndValues: Iterable[Tuple[str, int]])\
            -> 'Metrics':
        """Add a list of pairs (label, value)"""
        for (l, v) in labelsAndValues:
            self.add(Metric(label=l, n=v))
        return self

    def addMetrics(self, metrics: 'Metrics') -> 'Metrics':
        for metric in metrics.all:
            self.add(metric)
        return self

    def addMetricsList(self, metricsList: List['Metrics']) -> 'Metrics':
        """
        Increment all metric with the values in the given
        metrics. Add metric entry in case of new metric.
        """
        for metrics in metricsList:
            self.addMetrics(metrics)
        return self
            # for metric in metrics.all:
            #     if metric.label in self.metricNamed:
            #         # the metric exists, add the new value
            #         self.metricNamed[metric.label]+=\
            #             metric.n
            #     else:
            #         self.metricNamed[metric.label]=metric.n

    def collect(self, elements: List[Any]) -> 'Metrics':
        for e in elements:
            print(('CC'*15, type(e)))
            print(('CC'*15, 'metrics' in dir(e)))
        metrics_list=[
            e.metrics for e in elements
            # hasattr does not work
            # see
            if 'metrics' in dir(e)]
        self.addMetricsList(metrics_list)
        print(('CC'*10, len(elements), len(metrics_list)))

        return self

    def __len__(self):
        return len(self.metricNamed)

    def __str__(self):
        return ''.join(
            [str(m)+'\n' for m in self.all])

    def __repr__(self):
        return 'Metrics(%s)' % \
               ','.join(m.__repr__() for m in self.all)
