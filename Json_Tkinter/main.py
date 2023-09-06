import os
import requests
import threading
import tkinter as tk


def download_file(url, headers, local_path, file_number, status_label):
    try:
        response = requests.get(url + str(file_number), headers=headers)
        if response.status_code == 200:
            with open(os.path.join(local_path, f"file_{file_number}.json"), "w") as f:
                f.write(response.text)
        else:
            print(f"Failed to download file {file_number}")
            status_label.config(text="Error", foreground="red")
    except Exception as error:
        print(f"An error occurred while downloading file {file_number}: {error}")
        status_label.config(text="Error", foreground="red")


def download_files(num_files, status_label):
    try:
        url = "https://jsonplaceholder.typicode.com/posts/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) "
            "Chrome/102.0.0.0 Safari/537.36"
        }

        local_path = os.path.join(os.path.dirname(__file__), "json")
        os.makedirs(local_path, exist_ok=True)

        threads = []

        for i in range(1, num_files + 1):
            thread = threading.Thread(
                target=download_file, args=(url, headers, local_path, i, status_label)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        status_label.config(text="Successful", foreground="green")
    except Exception as error:
        status_label.config(text="Error", foreground="red")


def main():
    global status_label
    root = tk.Tk()
    root.title("JSON File Downloader")

    label = tk.Label(
        root, text="Введите количество json файлов, которые хотите скачать:"
    )
    label.pack(pady=5)

    entry = tk.Entry(root)
    entry.pack(pady=5)
    status_label = tk.Label(root, text="", foreground="green")
    status_label.pack(pady=2)

    download_button = tk.Button(
        root,
        text="Скачать",
        command=lambda: threading.Thread(
            target=download_files, args=(int(entry.get()), status_label)
        ).start(),
    )
    download_button.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
