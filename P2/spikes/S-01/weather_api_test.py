import json
import time
from urllib.request import urlopen

URL = (
    'https://api.open-meteo.com/v1/forecast'
    '?latitude=32.985&longitude=-96.750'
    '&current=temperature_2m,precipitation'
    '&timezone=America%2FChicago'
)

successes = 0
response_times = []
lines = []

for number in range(1, 6):
    start = time.perf_counter()
    try:
        with urlopen(URL, timeout=15) as response:
            data = json.load(response)
        elapsed = time.perf_counter() - start
        current = data.get('current', {})
        if 'temperature_2m' not in current or 'precipitation' not in current:
            raise ValueError('Missing temperature or precipitation data')
        successes += 1
        response_times.append(elapsed)
        line = (f'Test {number}: SUCCESS | {elapsed:.3f} seconds | '
                f'Temperature: {current["temperature_2m"]} °C | '
                f'Precipitation: {current["precipitation"]} mm')
    except Exception as error:
        line = f'Test {number}: FAILED | {type(error).__name__}: {error}'
    print(line)
    lines.append(line)

average = sum(response_times) / len(response_times) if response_times else 0
summary = f'{successes} successful requests out of 5 tests. Average response time: {average:.3f} seconds.'
print('\n' + summary)
with open('results.txt', 'w', encoding='utf-8') as output:
    output.write('\n'.join(lines) + '\n\n' + summary + '\n')
print('Saved results to results.txt')
