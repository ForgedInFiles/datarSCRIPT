"""Graphics context manages PySide6 Qt application, window, scene, and event loop."""

from __future__ import annotations

import threading
from typing import Callable, Dict, Any

try:
    from PySide6 import QtWidgets, QtGui, QtCore

    PYSIDE_AVAILABLE = True
except ImportError:
    PYSIDE_AVAILABLE = False

from ..errors import DatarError


class GraphicsContext:
    """Singleton-like context for the graphics subsystem."""

    _instance: GraphicsContext | None = None

    def __init__(self):
        if not PYSIDE_AVAILABLE:
            raise DatarError(
                "PySide6 is not installed. Install with: pip install pyside6"
            )
        self.app: QtWidgets.QApplication | None = None
        self.window: QtWidgets.QWidget | None = None
        self.scene: QtWidgets.QGraphicsScene | None = None
        self.view: QtWidgets.QGraphicsView | None = None
        self.pen: QtGui.QPen | None = None
        self.brush: QtGui.QBrush | None = None
        self.event_handlers: Dict[str, list[Callable]] = {}
        self.images: Dict[str, QtGui.QPixmap] = {}
        self._lock = threading.RLock()
        self._blocking = False
        self._timer: QtCore.QTimer | None = None

    @classmethod
    def get(cls) -> GraphicsContext:
        if cls._instance is None:
            cls._instance = GraphicsContext()
        return cls._instance

    def ensure_app(self) -> QtWidgets.QApplication:
        if self.app is None:
            self.app = QtWidgets.QApplication.instance()
            if self.app is None:
                self.app = QtWidgets.QApplication([])
        return self.app

    def init(
        self, title: str = "DatarScript", width: int = 800, height: int = 600
    ) -> None:
        app = self.ensure_app()
        from PySide6 import QtGui

        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle(str(title))
        self.scene = QtWidgets.QGraphicsScene(self.window)
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("white")))
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setGeometry(0, 0, int(width), int(height))
        self.window.resize(int(width), int(height))
        # Default pen/brush black
        self.pen = QtGui.QPen(QtGui.QColor("black"))
        self.brush = QtGui.QBrush(QtGui.QColor("black"))
        # Install event filter for callbacks
        if not self.window.eventFilter:
            self.window.eventFilter = self._event_filter

    def _event_filter(self, obj, event):
        # Translate Qt events to our callbacks
        from PySide6 import QtCore

        ev_type = None
        if event.type() == QtCore.QEvent.MouseButtonPress:
            pos = self.view.mapToScene(event.pos())
            ev_type = "mouse_click"
            data = (pos.x(), pos.y(), event.button())
        elif event.type() == QtCore.QEvent.KeyPress:
            ev_type = "key_press"
            data = event.key()
        else:
            return False
        handlers = self.event_handlers.get(ev_type, [])
        for fn in handlers:
            try:
                fn(data)
            except Exception:
                pass
        return False

    def set_background(self, color: str) -> None:
        from PySide6 import QtGui

        col = QtGui.QColor(color)
        if not col.isValid():
            raise DatarError(f"Invalid color: {color}")
        self.scene.setBackgroundBrush(QtGui.QBrush(col))

    def draw_rect(
        self, x: float, y: float, w: float, h: float, color: str | None = None
    ) -> None:
        from PySide6 import QtGui

        col = QtGui.QColor(color) if color else self.brush.color()
        if not col.isValid():
            raise DatarError(f"Invalid color: {color}")
        pen = self.pen
        brush = self.brush if color else None
        self.scene.addRect(float(x), float(y), float(w), float(h), pen, brush)

    def draw_ellipse(
        self, x: float, y: float, w: float, h: float, color: str | None = None
    ) -> None:
        from PySide6 import QtGui

        col = QtGui.QColor(color) if color else self.brush.color()
        if not col.isValid():
            raise DatarError(f"Invalid color: {color}")
        pen = self.pen
        brush = self.brush if color else None
        self.scene.addEllipse(float(x), float(y), float(w), float(h), pen, brush)

    def draw_polygon(
        self, points: list[tuple[float, float]], color: str | None = None
    ) -> None:
        from PySide6 import QtGui

        if not points:
            raise DatarError("draw_polygon: at least one point required")
        col = QtGui.QColor(color) if color else self.brush.color()
        if not col.isValid():
            raise DatarError(f"Invalid color: {color}")
        from PySide6 import QtCore

        qpoints = [QtCore.QPointF(float(x), float(y)) for x, y in points]
        polygon = QtGui.QPolygonF(qpoints)
        pen = self.pen
        brush = self.brush if color else None
        self.scene.addPolygon(polygon, pen, brush)

    def draw_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str | None = None,
        width: int = 1,
    ) -> None:
        from PySide6 import QtGui

        col = QtGui.QColor(color) if color else self.pen.color()
        if not col.isValid():
            raise DatarError(f"Invalid color: {color}")
        pen = QtGui.QPen(col)
        pen.setWidth(int(width))
        self.scene.addLine(float(x1), float(y1), float(x2), float(y2), pen)

    def draw_text(
        self, x: float, y: float, text: str, color: str | None = None, size: int = 12
    ) -> None:
        from PySide6 import QtGui

        col = QtGui.QColor(color) if color else QtGui.QColor("black")
        if not col.isValid():
            raise DatarError(f"Invalid color: {color}")
        font = QtGui.QFont()
        font.setPointSize(int(size))
        text_item = self.scene.addText(str(text), font)
        text_item.setDefaultTextColor(col)
        text_item.setPos(float(x), float(y))

    def load_image(self, path: str) -> str:
        from PySide6 import QtGui

        if not isinstance(path, str):
            raise DatarError("load_image: path must be a string")
        if path in self.images:
            return path  # use path as handle
        pixmap = QtGui.QPixmap(path)
        if pixmap.isNull():
            raise DatarError(f"Failed to load image: {path}")
        self.images[path] = pixmap
        return path

    def draw_image(
        self,
        handle: str,
        x: float,
        y: float,
        w: float | None = None,
        h: float | None = None,
    ) -> None:
        if handle not in self.images:
            raise DatarError(f"Image not loaded: {handle}")
        pixmap = self.images[handle]
        if w is not None and h is not None:
            pixmap = pixmap.scaled(int(w), int(h))
        self.scene.addPixmap(pixmap).setPos(float(x), float(y))

    def on_event(self, event_type: str, handler_name: str, interpreter: Any) -> None:
        """Register a DatarScript function as event handler."""

        # handler_name is a string; interpreter will look it up at runtime
        def wrapper(data):
            # Call DatarScript function with event data
            try:
                interpreter.call_user_function(handler_name, [data])
            except Exception:
                pass

        self.event_handlers.setdefault(event_type, []).append(wrapper)

    def show(self, blocking: bool = True) -> None:
        if not self.window:
            raise DatarError("Graphics not initialized; call init first")
        self.window.show()
        app = self.app
        if app is None:
            raise DatarError("Graphics app not initialized")
        if blocking:
            app.exec()
        else:
            # Use timer to process events periodically; interpreter continues
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(lambda: app.processEvents())
            self._timer.start(50)  # ~20 FPS event processing
            # Start event loop in non-blocking mode
            QtCore.QTimer.singleShot(0, app.exec)

    def process_events(self) -> None:
        if self.app:
            self.app.processEvents()

    def clear(self) -> None:
        if self.scene:
            self.scene.clear()

    def close(self) -> None:
        if self.window:
            self.window.close()
        if self.app:
            self.app.quit()
