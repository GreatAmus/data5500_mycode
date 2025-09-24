from pathlib import Path
import json

class CryptoPrinter:
    def print_data(self, data):
        for pair, path_info in data.collection.items():
            print(f'paths from {pair} ------------------------------------')
            for path in path_info:
                if not path.ratio is None:
                    print(path.get_data())
            print()

        min_max = data.min_max()
        print(f"Smallest Paths weight factor: {min_max['min_weight']}")
        print(f"Path: {min_max['min_path']}")
        print(f"Greatest Paths weight factor: {min_max['max_weight']}")
        print(f"Path: {min_max['max_path']}")

    def export_data(self, filename, data):
        file_path = Path(__file__).parent
        data_dict = data.all_paths_dict()
        with open(f"{file_path}/{filename}.json", "w") as file:
            json.dump(data_dict, file, indent=2)

        return data_dict
