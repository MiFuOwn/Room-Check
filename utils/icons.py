"""
Inline SVG icons (Heroicons-style outline, stroke=currentColor).

design.md บอกว่า "No emojis in UI — use icon system only (Lucide, Heroicons)".
Streamlit ไม่มี icon library ให้ import ตรงๆ แบบ React เลยเก็บเป็น SVG string
ไว้ที่นี่ที่เดียว ใช้ร่วมกันทุกหน้า.
"""

_STROKE = "#1A1A1A"

BUILDING = f"""
<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{_STROKE}"
     stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 21h18" />
  <path d="M5 21V5a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v16" />
  <path d="M15 21V9a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v12" />
  <path d="M8 7h1M8 11h1M8 15h1M11 7h1M11 11h1M11 15h1" />
</svg>
"""

BULB = f"""
<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
     stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M9 18h6" />
  <path d="M10 22h4" />
  <path d="M12 2a6 6 0 0 0-4 10.5c.6.5 1 1.3 1 2.1V16h6v-1.4c0-.8.4-1.6 1-2.1A6 6 0 0 0 12 2Z" />
</svg>
"""

SPEAKER = f"""
<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
     stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M11 5 6 9H3v6h3l5 4V5Z" />
  <path d="M16 8a5 5 0 0 1 0 8" />
  <path d="M19 5a9 9 0 0 1 0 14" />
</svg>
"""

HOME = f"""
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{_STROKE}"
     stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="m3 11 9-8 9 8" />
  <path d="M5 10v10a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1V10" />
</svg>
"""

DOOR = f"""
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{_STROKE}"
     stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <rect x="5" y="2" width="14" height="20" rx="1" />
  <path d="M14 12h.01" />
</svg>
"""

OVERVIEW = f"""
<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor"
     stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
  <rect x="3" y="3" width="7" height="7" rx="1" />
  <rect x="14" y="3" width="7" height="7" rx="1" />
  <rect x="3" y="14" width="7" height="7" rx="1" />
  <rect x="14" y="14" width="7" height="7" rx="1" />
</svg>
"""

def icon_html(svg: str, css_class: str = "") -> str:
    """Wrap an SVG string in a span so it can sit inline next to text."""
    return f'<span class="icon {css_class}">{svg}</span>'