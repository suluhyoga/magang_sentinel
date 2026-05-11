from core.jateng_regions import detect_location as region_detector

def detect_location_advanced(text):
    """
    Wrapper untuk memastikan kompatibel
    dengan AI Engine terbaru
    """
    return region_detector(text)