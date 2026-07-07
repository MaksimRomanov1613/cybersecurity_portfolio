from os import popen
from sys import argv

def main():
    if len(argv) != 2:
        print(f"Использование: python {argv[0]} <CIDR>")
        exit(1)

    target = argv[-1]
    cmd = f"nmap --open --script=mongodb-databases.nse -p 27017 {target}"
    print(f"[*] Выполняю: {cmd}\n")

    try:
        raw = popen(cmd).read()
        reports = raw.split("Nmap scan report for ")

        for report in reports[1:]:
            if "| mongodb-databases:" in report:
                host = report.split("\n")[0].strip()
                print(f"[+] MongoDB без пароля найден: {host}")
                # Выводим строки, начинающиеся с |
                for line in report.split("\n"):
                    if line.strip().startswith("|"):
                        print(line)
                print()
    except Exception as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    main()