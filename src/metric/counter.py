import apache_beam as beam
from apache_beam.metrics import Metrics


class CountingTransform(beam.PTransform):
    def __init__(self, counter_name):
        super().__init__()
        self.counter_name = counter_name

    def expand(self, pcoll):
        def count_element(element, counter_name):
            Metrics.counter("group", counter_name).inc()
            return element

        return pcoll | "Count " + self.counter_name >> beam.Map(count_element, self.counter_name)
