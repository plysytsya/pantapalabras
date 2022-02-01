from pathlib import Path

ENV_LOCAL = "LOCAL"
ENV_DEV = "DEVELOPMENT"
ENV_PROD = "PRODUCTION"


PROJECT_PARENT_DIR = Path(__file__).absolute().parent.parent.parent
PROJECT_DIR = Path(__file__).absolute().parent
