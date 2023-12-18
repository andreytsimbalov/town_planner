class PROJ:
    # EPSG - проекция в метрах; WGS_EPSG - проекция в градусах
    EPSG = 3857
    WGS_EPSG = 4326

    EPSG_STR = f"EPSG:{EPSG}"
    WGS_EPSG_STR = f"EPSG:{WGS_EPSG}"


class METER:
    WALK = 1250  # Расстояние до метро, парков, воды
    BUILD_LVL_VIEW = 200  # Расстояние до обзора видимых домов (определение высотности зданий)
    BAD_AIR = 500  # Загрязненный воздух

    CENTER_BUFFER = 2000  # Отображение зоны на карте

    GRID = 100  # Размер зонирующей решетки

