import json

def load_metrics(filename):
    with open(filename, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    base_cc = load_metrics("baseline_complexity.json")
    ref_cc = load_metrics("refactored_complexity.json")
    print("Metrics comparison loaded successfully.")
