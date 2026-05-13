window.GAME_CONFIG = {
    "ui": {
        "title": "¿Listo para probar tu suerte?",
        "start_text": "↑↑↑  Presiona el botón para empezar  ↑↑↑",
        "logo": "media/logo.png",
        "logo_width": "300px",
        "theme": {
            "primary_color": "#8b6508",
            "background_gradient": "linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #1a1410 50%, #0a0a0a 75%, #000000 100%)"
        }
    },
    "wheel": {
        "colors": {
            "segmentA": "#DC143C",
            "segmentB": "#222222",
            "text": "#ffffff",
            "stroke": "#8b6508"
        },
        "text_size": 30,
        "spin_duration_seconds": 10,
        "extra_spins": 12
    },
    "audio": {
        "spin_sound": "media/spin.mp3"
    },
    "prizes": [
        {
            "number": 1,
            "color": "segmentA",
            "label": "FP 100",
            "weight": 355
        },
        {
            "number": 2,
            "color": "segmentB",
            "label": "FP 500",
            "weight": 1
        },
        {
            "number": 3,
            "color": "segmentA",
            "label": "FP 200",
            "weight": 30
        },
        {
            "number": 4,
            "color": "segmentB",
            "label": "FP 150",
            "weight": 100
        },
        {
            "number": 5,
            "color": "segmentA",
            "label": "FP 250",
            "weight": 14
        },
        {
            "number": 6,
            "color": "segmentB",
            "label": "FP 1000",
            "weight": 0
        }
    ]
};
