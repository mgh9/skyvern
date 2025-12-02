from __future__ import annotations

import typing
from typing import Any

if typing.TYPE_CHECKING:
    from skyvern.forge.forge_app import ForgeApp


class AppHolder:
    def __init__(self) -> None:
        object.__setattr__(self, "_inst", None)

    def set_app(self, inst: ForgeApp) -> None:
        object.__setattr__(self, "_inst", inst)

    def __getattr__(self, name: str) -> Any:
        inst = object.__getattribute__(self, "_inst")
        if inst is None:
            # Lazily initialize to avoid crashes when the app is accessed before startup hooks run.
            from skyvern.forge.forge_app_initializer import start_forge_app

            inst = start_forge_app()
            object.__setattr__(self, "_inst", inst)

        return getattr(inst, name)

    def __setattr__(self, name: str, value: Any) -> None:
        inst = object.__getattribute__(self, "_inst")
        if inst is None:
            from skyvern.forge.forge_app_initializer import start_forge_app

            inst = start_forge_app()
            object.__setattr__(self, "_inst", inst)

        setattr(inst, name, value)


_app_holder = AppHolder()
if typing.TYPE_CHECKING:
    app: ForgeApp
else:
    app = _app_holder  # type: ignore


def set_force_app_instance(inst: ForgeApp) -> None:
    # Always set on the holder and keep the package attribute pointing to it.
    _app_holder.set_app(inst)  # type: ignore[name-defined]
    globals()["app"] = _app_holder  # ensure subsequent imports see the holder
