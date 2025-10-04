from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt, QSize  # <<< THE MISSING IMPORT IS ADDED HERE

# --- SVG Path Data for each icon (like a font for icons) ---
# Sourced from the open-source "Feather Icons" library

SVG_DATA = {
    "printer": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>""",
    "play": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>""",
    "pause": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>""",
    "brain": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v0A2.5 2.5 0 0 1 9.5 7h-3A2.5 2.5 0 0 0 4 9.5v0A2.5 2.5 0 0 0 6.5 12h3A2.5 2.5 0 0 1 12 14.5v0A2.5 2.5 0 0 1 9.5 17h-3A2.5 2.5 0 0 0 4 19.5v0A2.5 2.5 0 0 0 6.5 22h11A2.5 2.5 0 0 0 20 19.5v0a2.5 2.5 0 0 0-2.5-2.5h-3A2.5 2.5 0 0 1 12 14.5v0A2.5 2.5 0 0 1 14.5 12h3a2.5 2.5 0 0 0 2.5-2.5v0A2.5 2.5 0 0 0 17.5 7h-3A2.5 2.5 0 0 1 12 4.5v0A2.5 2.5 0 0 1 14.5 2z"></path></svg>""",
    "wind": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.7 7.7a2.5 2.5 0 1 0-3.5-3.5"></path><path d="M14.2 11.2a2.5 2.5 0 1 0-3.5-3.5"></path><path d="M11.2 14.2a2.5 2.5 0 1 0-3.5-3.5"></path><path d="M14.2 17.7a2.5 2.5 0 1 0-3.5-3.5"></path><path d="M6.3 7.7a2.5 2.5 0 1 0-3.5-3.5"></path><path d="M9.8 11.2a2.5 2.5 0 1 0-3.5-3.5"></path><path d="M6.8 14.2a2.5 2.5 0 1 0-3.5-3.5"></path><path d="M9.8 17.7a2.5 2.5 0 1 0-3.5-3.5"></path></svg>""",
}

def create_icon_from_svg(svg_key: str, color: str) -> QIcon:
    """
    Creates a QIcon from SVG data, with a specified color.
    
    Args:
        svg_key: The key for the SVG data in the SVG_DATA dictionary.
        color: The hex color code for the icon.
        
    Returns:
        A QIcon object.
    """
    svg_string = SVG_DATA.get(svg_key, "").replace('stroke="currentColor"', f'stroke="{color}"')
    
    renderer = QSvgRenderer(svg_string.encode('utf-8'))
    pixmap = QPixmap(renderer.defaultSize())
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)