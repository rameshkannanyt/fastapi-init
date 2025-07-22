# Example usage of the FastAPI Kickstart Toolkit

from fastapi_init import cli

def main():
    # Initialize a new FastAPI project
    cli.init_project("myproject")

    # Check the environment for missing dependencies
    cli.env_check()

    # Add error middleware for better error handling
    cli.add_error_middleware()

    # Set up async test support
    cli.test_init()

if __name__ == "__main__":
    main()