import sys


def run(env):
    if env not in ['dev', 'qa', 'prod']:
        print(f"Invalid environment: {env}")
        sys.exit(1)
    print(f"Running script in {env} environment...")


if __name__ == "__main__":
    # Read environment from command-line argument
    if len(sys.argv) < 2:
        print("Usage: python main.py <env>")
        sys.exit(1)
    environment = sys.argv[1]
    run(environment)
