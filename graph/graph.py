from disco.core import Job, result_iterator
import csv, sys


class Graph(Job):
    partitions = 2
    sort = True

    def map(self, row, params):
        yield row[0], row[1:]

    def reduce(self, rows_iter, out, params):
        from disco.util import kvgroup
        from itertools import chain
        #for url_key, descriptors in kvgroup(sorted(rows_iter)):
        for url_key, descriptors in kvgroup(rows_iter):
            merged_descriptors = list(chain.from_iterable(descriptors))
            if len(merged_descriptors) > 1:
                out.add(url_key, merged_descriptors)


if __name__ == '__main__':
    input_filename = "input.csv"
    output_filename = "output.txt"
    parts = 2
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        if len(sys.argv) > 2:
            output_filename = sys.argv[2]
            if len(sys.argv) > 3:
              parts = sys.argv[3]

    from graph import Graph
    job = ().run(input=[input_filename],
                partitions=parts)

    with open(output_filename, 'w') as fp:
        writer = csv.writer(fp)
        for url_key, descriptors in result_iterator(job.wait(show=True)):
            writer.writerow([url_key] + descriptors)
