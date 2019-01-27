from prometheus_client import start_http_server
from flask import Flask
import time
import random
from prometheus_client import Histogram, Counter
import sys

if len(sys.argv) > 1:
    print('ustawiam ze ścieżki:', sys.argv[1])
    pan_tadeusz_path = sys.argv[1]
else:
    print('ustawiam pan-tadeusz.txt')
    pan_tadeusz_path = 'pan-tadeusz.txt'

app = Flask(__name__)
hist = Histogram('request_latency_seconds', 'Czas czekania na odpowiedz')
request_counter = Counter("request_counter", "Liczba żądań", ['response_code'])

def process(word):
    #time.sleep(random.randint(0, 300) / 100)
    for i in range(random.randint(0,100)):
        with open(pan_tadeusz_path, 'r', encoding = 'utf8') as fhin:
            text = fhin.read()
            text.lower().split().count(word)
    return text.lower().split().count(word)

@app.route("/hello")
def hello():
    return("Czesc.")

@app.route("/process/<word>/")
def process_word(word):
    start_time = time.time()
    word_count = process(word)
    result_dice = random.randint(0,100)
    print(result_dice)
    if result_dice < 80:
        took_time = time.time() - start_time
        hist.observe(took_time)
        request_counter.labels('200').inc(1)
        return word + " pojawiło się w Panu Tadeuszu razy: " + str(word_count), 200
    elif result_dice < 90:
        took_time = time.time() - start_time
        hist.observe(took_time)
        request_counter.labels('404').inc(1)
        return "Not found", 404
    else:
        took_time = time.time() - start_time
        hist.observe(took_time)
        request_counter.labels('500').inc(1)
        return "Ups!", 500

start_http_server(9100)
app.run(host="0.0.0.0", threaded = True)

# delta(request_counter[5m])
# histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le))
