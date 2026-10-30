import json
import subprocess
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit

def analyze_file(filename):
    with open(filename, 'r') as f:
        code = f.read()
    
    cc_results = cc_visit(code)
    avg_cc = sum(item.complexity for item in cc_results) / len(cc_results) if cc_results else 0
    mi_score = mi_visit(code, multi=True)
    halstead = h_visit(code)
    
    metrics = {
        "average_cyclomatic_complexity": avg_cc,
        "maintainability_index": mi_score,
        "halstead_difficulty": halstead.difficulty,
        "halstead_effort": halstead.effort
    }
    return metrics

def save_metrics(metrics, output_file):
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    metrics = analyze_file("legacy_calculator.py")
    save_metrics(metrics, "baseline_metrics_summary.json")
    print("Baseline metrics saved successfully.")
