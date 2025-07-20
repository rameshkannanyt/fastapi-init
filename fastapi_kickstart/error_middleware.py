from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ErrorMiddleware:
    def __init__(self, app=None):
        self.app = app

    async def __call__(self, request: Request, call_next):
        try:
            response = await call_next(request)
            if response.status_code >= 400:
                return self.handle_error(response)
            return response
        except HTTPException as exc:
            return self.handle_http_exception(exc)
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}")
            return self.handle_unexpected_exception(exc)

    def handle_error(self, response):
        return JSONResponse(
            status_code=response.status_code,
            content={"detail": response.body.decode()},
        )

    def handle_http_exception(self, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    def handle_unexpected_exception(self, exc):
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred."},
        )
    
    def install(self, app=None):
        """Install the error middleware on a FastAPI app."""
        if app is None:
            # Create a simple example app for demonstration
            from fastapi import FastAPI
            app = FastAPI()
        
        # Add middleware to the app
        app.add_middleware(ErrorMiddleware)
        return app
    
    def add_to_project(self, project_path: Path) -> bool:
        """Add error middleware to an existing FastAPI project."""
        try:
            # Create middleware file
            middleware_file = project_path / "app" / "core" / "middleware.py"
            middleware_file.parent.mkdir(parents=True, exist_ok=True)
            
            middleware_content = '''from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class ErrorMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        try:
            response = await call_next(request)
            if response.status_code >= 400:
                return self.handle_error(response)
            return response
        except HTTPException as exc:
            return self.handle_http_exception(exc)
        except Exception as exc:
            logger.error(f"Unhandled exception: {exc}")
            return self.handle_unexpected_exception(exc)

    def handle_error(self, response):
        return JSONResponse(
            status_code=response.status_code,
            content={"detail": response.body.decode()},
        )

    def handle_http_exception(self, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    def handle_unexpected_exception(self, exc):
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred."},
        )
'''
            
            with open(middleware_file, "w", encoding="utf-8") as f:
                f.write(middleware_content)
            
            # Update main.py to include middleware
            main_file = project_path / "app" / "main.py"
            if main_file.exists():
                with open(main_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Add middleware import and usage
                if "from app.core.middleware import ErrorMiddleware" not in content:
                    lines = content.split("\n")
                    new_lines = []
                    middleware_added = False
                    
                    for i, line in enumerate(lines):
                        new_lines.append(line)
                        # Look for FastAPI app creation and add middleware after it
                        if "app = FastAPI(" in line and not middleware_added:
                            # Add import at the top
                            if "from app.core.middleware import ErrorMiddleware" not in content:
                                new_lines.insert(1, "from app.core.middleware import ErrorMiddleware")
                            
                            # Add middleware after app creation
                            new_lines.append("app.add_middleware(ErrorMiddleware)")
                            middleware_added = True
                    
                    with open(main_file, "w", encoding="utf-8") as f:
                        f.write("\n".join(new_lines))
            
            return True
        except Exception as e:
            logger.error(f"Failed to add error middleware to project: {e}")
            return False