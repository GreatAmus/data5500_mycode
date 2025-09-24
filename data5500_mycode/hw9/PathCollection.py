class PathCollection:
    def __init__(self):
        self.collection = {}

    def add_path(self, key, path):
        self.collection[key] = path

    def all_paths_dict(self):
        data = {}
        for pair, path_list in self.collection.items():
            data[pair] = []
            for path in path_list:
                data[pair].append(path.get_dict())

        return data

    def min_max(self):
        deviations = {}
        for pair, path_info in self.collection.items():
            for path in path_info:
                if path.deviation is None:
                    continue
                elif len(deviations) == 0:
                    deviations['max_path'] = f'{path.forward} {path.reverse}'
                    deviations['min_path'] = f'{path.forward} {path.reverse}'
                    deviations['max_weight'] = path.ratio
                    deviations['min_weight'] = path.ratio
                    deviations['min_dev'] = path.deviation
                    deviations['max_dev'] = path.deviation
                elif deviations['min_dev'] > path.deviation:
                    deviations['min_path'] = f'{path.forward} {path.reverse}'
                    deviations['min_weight'] = path.ratio
                    deviations['min_dev'] = path.deviation
                elif deviations['max_dev'] < path.deviation:
                    deviations['max_path'] = f'{path.forward} {path.reverse}'
                    deviations['max_weight'] = path.ratio
                    deviations['max_dev'] = path.deviation
        return deviations

class PathData:
    def __init__(self, forward, reverse, fwd_weight, rev_weight):
        self.forward = forward
        self.reverse = reverse
        self.fwd_weight = fwd_weight
        self.rev_weight = rev_weight
        self.ratio = self.fwd_weight * self.rev_weight if self.fwd_weight and self.rev_weight else None
        self.deviation = abs(self.ratio - 1.0) if self.ratio is not None else None

    def get_data(self):
        if self.fwd_weight is None or self.rev_weight is None:
            return f"{self.forward} does not have a valid reverse path"
        else:
            return f"{self.forward} {self.fwd_weight}\n{self.reverse} {self.rev_weight}\n{self.ratio}"

    def get_dict(self):
        return {
            'forward': self.forward,
            'reverse': self.reverse,
            'forward_weight': self.fwd_weight,
            'reverse_weight': self.rev_weight,
            'ratio': self.ratio
        }