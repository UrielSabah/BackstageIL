"""Mount all route modules under a single API router (auto-discovery)."""
import importlib
import pkgutil
import pathlib

from fastapi import APIRouter

api_router = APIRouter()
package_dir = pathlib.Path(__file__).resolve().parent

for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
    if module_name != "__init__":
        module = importlib.import_module(f"{__package__}.{module_name}")
        api_router.include_router(module.router)
