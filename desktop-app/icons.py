import sys
import os
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt, QSize

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_icon_from_svg(icon_key: str, color: str) -> QIcon:
    """
    Creates a QIcon from an SVG file, with a specified color.
    
    Args:
        icon_key: The base name of the SVG file (e.g., "printer").
        color: The hex color code for the icon.
        
    Returns:
        A QIcon object.
    """
    icon_path = resource_path(f'assets/icons/{icon_key}.svg')
    
    try:
        with open(icon_path, 'r', encoding='utf-8') as f:
            svg_string = f.read()
    except FileNotFoundError:
        print(f"Error: Icon file not found at {icon_path}")
        return QIcon() # Return an empty icon

    svg_colored = svg_string.replace('stroke="currentColor"', f'stroke="{color}"')
    
    renderer = QSvgRenderer(svg_colored.encode('utf-8'))
    pixmap = QPixmap(renderer.defaultSize())
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)

