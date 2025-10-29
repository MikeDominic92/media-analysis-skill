"""
BMAD-EDI Media Analysis - Performance Test Suite
Tests processing speed and resource usage
"""

import os
import sys
import time
import psutil
from pathlib import Path
import json

SKILL_DIR = Path(__file__).parent


class PerformanceTestSuite:
    """Performance and resource usage tests"""

    def __init__(self):
        self.results = {}
        self.process = psutil.Process()

    def measure_startup_time(self):
        """Measure time to import all modules"""
        sys.path.insert(0, str(SKILL_DIR))

        start = time.time()
        try:
            import gemini_analyzer
            import ocr_processor
            import workflow
            import archival
            elapsed = time.time() - start
            self.results['startup_time'] = {
                'elapsed': elapsed,
                'status': 'SUCCESS',
                'threshold': 5.0,
                'passed': elapsed < 5.0
            }
        except Exception as e:
            elapsed = time.time() - start
            self.results['startup_time'] = {
                'elapsed': elapsed,
                'status': 'FAILED',
                'error': str(e),
                'passed': False
            }

    def measure_memory_baseline(self):
        """Measure baseline memory usage"""
        mem_info = self.process.memory_info()
        self.results['memory_baseline'] = {
            'rss_mb': mem_info.rss / 1024 / 1024,
            'vms_mb': mem_info.vms / 1024 / 1024,
            'threshold_mb': 500,
            'passed': mem_info.rss / 1024 / 1024 < 500
        }

    def measure_file_operations(self):
        """Measure file I/O performance"""
        test_file = SKILL_DIR / "test_io.tmp"

        # Write test
        start = time.time()
        with open(test_file, 'w') as f:
            f.write("x" * 10_000_000)  # 10MB
        write_time = time.time() - start

        # Read test
        start = time.time()
        with open(test_file, 'r') as f:
            _ = f.read()
        read_time = time.time() - start

        # Cleanup
        test_file.unlink()

        self.results['file_io'] = {
            'write_time': write_time,
            'read_time': read_time,
            'write_throughput_mbps': 10 / write_time,
            'read_throughput_mbps': 10 / read_time,
            'passed': write_time < 1.0 and read_time < 0.5
        }

    def measure_directory_operations(self):
        """Measure directory scan performance"""
        incoming_dir = Path.home() / "Documents" / "tickets" / "incoming"

        start = time.time()
        if incoming_dir.exists():
            files = list(incoming_dir.rglob("*"))
            elapsed = time.time() - start

            self.results['directory_scan'] = {
                'elapsed': elapsed,
                'file_count': len(files),
                'files_per_sec': len(files) / elapsed if elapsed > 0 else 0,
                'passed': elapsed < 1.0
            }
        else:
            self.results['directory_scan'] = {
                'status': 'SKIPPED',
                'reason': 'incoming directory not found',
                'passed': True
            }

    def measure_json_operations(self):
        """Measure JSON serialization performance"""
        test_data = {
            'ticket_id': 'TEST-12345',
            'analysis': {
                'entities': ['customer_' + str(i) for i in range(100)],
                'text': 'x' * 10000,
                'metadata': {f'key_{i}': f'value_{i}' for i in range(100)}
            }
        }

        # Serialize test
        start = time.time()
        json_str = json.dumps(test_data)
        serialize_time = time.time() - start

        # Deserialize test
        start = time.time()
        _ = json.loads(json_str)
        deserialize_time = time.time() - start

        self.results['json_operations'] = {
            'serialize_time': serialize_time,
            'deserialize_time': deserialize_time,
            'data_size_kb': len(json_str) / 1024,
            'passed': serialize_time < 0.1 and deserialize_time < 0.1
        }

    def check_disk_space(self):
        """Check available disk space"""
        disk = psutil.disk_usage(str(SKILL_DIR))

        self.results['disk_space'] = {
            'total_gb': disk.total / 1024 / 1024 / 1024,
            'used_gb': disk.used / 1024 / 1024 / 1024,
            'free_gb': disk.free / 1024 / 1024 / 1024,
            'percent_used': disk.percent,
            'threshold_free_gb': 10,
            'passed': disk.free / 1024 / 1024 / 1024 > 10
        }

    def check_cpu_info(self):
        """Check CPU information"""
        self.results['cpu_info'] = {
            'logical_cores': psutil.cpu_count(logical=True),
            'physical_cores': psutil.cpu_count(logical=False),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'passed': psutil.cpu_count(logical=True) >= 2
        }

    def print_results(self):
        """Print performance test results"""
        print("\n" + "="*60)
        print("PERFORMANCE TEST RESULTS")
        print("="*60 + "\n")

        for test_name, result in self.results.items():
            status = "[+] PASS" if result.get('passed', False) else "[!] FAIL"
            print(f"{status} - {test_name}")

            # Pretty print results
            for key, value in result.items():
                if key != 'passed':
                    if isinstance(value, float):
                        print(f"         {key}: {value:.4f}")
                    else:
                        print(f"         {key}: {value}")
            print()

        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results.values() if r.get('passed', False))
        print("="*60)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        print("="*60)

    def run_all_tests(self):
        """Run all performance tests"""
        print("\n" + "="*60)
        print("BMAD-EDI MEDIA ANALYSIS - PERFORMANCE TESTS")
        print("="*60 + "\n")

        print("[*] Running startup time test...")
        self.measure_startup_time()

        print("[*] Measuring memory baseline...")
        self.measure_memory_baseline()

        print("[*] Testing file I/O performance...")
        self.measure_file_operations()

        print("[*] Testing directory operations...")
        self.measure_directory_operations()

        print("[*] Testing JSON operations...")
        self.measure_json_operations()

        print("[*] Checking disk space...")
        self.check_disk_space()

        print("[*] Checking CPU info...")
        self.check_cpu_info()

        self.print_results()

        # Save results to file
        results_file = SKILL_DIR / "performance_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n[+] Results saved to: {results_file}")


def main():
    """Run performance test suite"""
    suite = PerformanceTestSuite()
    suite.run_all_tests()


if __name__ == "__main__":
    main()
