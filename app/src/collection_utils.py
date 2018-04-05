from collections import Counter


def fill_counters(keyed_counters, all_keys):
    for (key, counter) in keyed_counters.items():
        for c in all_keys:
            counter[c] += 0


def init_counter(keyed_counters, label, all_keys):
    for key in all_keys:
        keyed_counters[label] = Counter()


def fill_labels(keyed_counters, labels, all_keys):
    for label in labels:
        c_id = f"[{label}]"
        if c_id not in keyed_counters:
            init_counter(keyed_counters, c_id, all_keys)
