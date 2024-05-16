from env.get_env import CONFIG


def main() -> None:
    print("All environment variables are:")

    for key, val in CONFIG.items():
        print(f"{key}: {val}")


if __name__ == "__main__":
    main()
