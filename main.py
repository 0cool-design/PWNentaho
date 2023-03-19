import os
import requests
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from tqdm import tqdm


class PWNentaho:
    def __init__(self):
        self.histfile = os.path.join(os.path.expanduser("~"), ".endpoints_history")
        self.history = FileHistory(self.histfile)

    def run(self):
        try:
            target = prompt("Enter target: ", history=self.history)
            if not target.startswith("http"):
                target = "http://" + target
            if not os.path.exists("outputs"):
                os.makedirs("outputs")
            endpoints = self._read_endpoints()
            for endpoint in tqdm(endpoints):
                try:
                    response = requests.get(f"{target}/{endpoint}", timeout=5)
                    response.raise_for_status()
                    filename = self._extract_filename(endpoint) + ".txt"
                    with open(f"outputs/{filename}", "w") as f:
                        f.write(response.text)
                except requests.exceptions.Timeout:
                    pass
                    #print(f"Error: Request timed out for endpoint '{endpoint}'.")
                except requests.exceptions.HTTPError as e:
                    print(f"Error: {e}")

        except KeyboardInterrupt:
            print("\nExecution interrupted by user.")

        finally:
            with open(self.histfile, "w") as f:
                f.write("\n".join(self.history.get_strings()[-1000:]))

    def _read_endpoints(self):
        endpoints = []
        with open("endpoints.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    endpoints.append(line)
        return endpoints

    def _extract_filename(self, endpoint):
        return endpoint.rsplit("/", 1)[-1]


if __name__ == "__main__":
    PWNentaho().run()
