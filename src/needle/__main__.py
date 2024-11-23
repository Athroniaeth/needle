import logging
import sys

from dotenv import load_dotenv

from needle import PROJECT_PATH
from needle.cli import cli


def main():
    """
    Main function to run the application.

    Raises:
        SystemExit: If the program is exited.

    Returns:
        int: The return code of the program.

    """
    # Load dotenv file
    load_dotenv(dotenv_path=PROJECT_PATH / ".env")

    # Get the arguments for the program
    arguments = " ".join(sys.argv[1:])

    # Add the user command to the logs (first is src path)
    logging.info(f"Arguments passed: {arguments}")

    try:
        cli()
    except Exception as exception:
        logging.error(f"Traceback (most recent call last):\n{exception}")
    except KeyboardInterrupt:
        logging.debug("Exiting the program due to keyboard interrupt.")


if __name__ == "__main__":
    main()
