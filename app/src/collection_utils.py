

def fill_counters(keyed_counters, all_keys):
    for (key, counter) in keyed_counters.items():
            for c in all_keys:
                counter[c] += 0
