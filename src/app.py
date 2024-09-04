""" The main entry point of the application """

import logging
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from mangum import Mangum

from api.routers import model, chat, embeddings
from api.setting import (
    API_ROUTE_PREFIX,
    AZURE_API_ROUTE_PREFIX,
    TITLE,
    DESCRIPTION,
    SUMMARY,
    VERSION,
)


# kiku: ANSI color codes
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"


class ColoredFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: Colors.BLUE
        + "%(asctime)s [%(levelname)s] %(message)s"
        + Colors.RESET,
        logging.INFO: Colors.GREEN
        + "%(asctime)s [%(levelname)s] %(message)s"
        + Colors.RESET,
        logging.WARNING: Colors.YELLOW
        + "%(asctime)s [%(levelname)s] %(message)s"
        + Colors.RESET,
        logging.ERROR: Colors.RED
        + "%(asctime)s [%(levelname)s] %(message)s"
        + Colors.RESET,
        logging.CRITICAL: Colors.MAGENTA
        + "%(asctime)s [%(levelname)s] %(message)s"
        + Colors.RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


config = {
    "title": TITLE,
    "description": DESCRIPTION,
    "summary": SUMMARY,
    "version": VERSION,
}

logging.basicConfig(
    level=logging.INFO,
    format="\n%(asctime)s [%(levelname)s] %(message)s",
)

# kiku: for logging each request
logger = logging.getLogger(__name__)

app = FastAPI(**config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# kiku: for logging each request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    status_color = Colors.GREEN if response.status_code < 400 else Colors.RED
    logger.info(
        f"{Colors.BLUE}kikuLogger{Colors.RESET}: {request.method} {request.url.path} - Status: {status_color}{response.status_code}{Colors.RESET} - took: {Colors.CYAN}{process_time:.2f}s{Colors.RESET}"
    )

    return response


print("API_ROUTE_PREFIX:", API_ROUTE_PREFIX)

""" 
The primary purpose of this application is to provide an OpenAI-compatible API 
interface for Amazon Bedrock AI services. It supports:
 - Chat completions
 - Embeddings
 - Model information
"""
app.include_router(model.router)
app.include_router(embeddings.router)  # also at root
app.include_router(embeddings.router, prefix=API_ROUTE_PREFIX)
app.include_router(embeddings.router, prefix=AZURE_API_ROUTE_PREFIX)
app.include_router(chat.router, prefix=API_ROUTE_PREFIX)
app.include_router(chat.router, prefix=AZURE_API_ROUTE_PREFIX)


@app.get("/health")
async def health():
    """For health check if needed"""
    return {"status": "OK"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # print(f"{Colors.RED}RequestValidationError: {exc}{Colors.RESET}")
    logging.error(f"{Colors.RED}RequestValidationError:{Colors.RESET}: {exc}")
    return PlainTextResponse(str(exc), status_code=400)


# The inclusion of the Mangum handler suggests that this application can be deployed
# as an AWS Lambda function.
handler = Mangum(app)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
