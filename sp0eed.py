import speedtest
import threading
import itertools
import sys
import time

# Spinner animation
def spinner(task_done_flag, message):
    for char in itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]):
        if task_done_flag["done"]:
            break
        sys.stdout.write(f"\r{char} {message}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r✔ " + message + " completed\n")

def run_speed_test():
    st = speedtest.Speedtest()
    results = {}

    # Download test
    done = {"done": False}
    t = threading.Thread(target=spinner, args=(done, "Testing download speed"))
    t.start()

    results["download"] = st.download() / 1_000_000  # Mbps
    done["done"] = True
    t.join()

    # Upload test
    done = {"done": False}
    t = threading.Thread(target=spinner, args=(done, "Testing upload speed"))
    t.start()

    results["upload"] = st.upload() / 1_000_000  # Mbps
    done["done"] = True
    t.join()

    # Ping
    results["ping"] = st.results.ping

    return results


if __name__ == "__main__":
    print("\n🌐 Internet Speed Test\n")
    speed = run_speed_test()

    print("\n📊 Results")
    print("────────────────────────")
    print(f"⬇ Download : {speed['download']:.2f} Mbps")
    print(f"⬆ Upload   : {speed['upload']:.2f} Mbps")
    print(f"📡 Ping     : {speed['ping']:.0f} ms\n")
