# Hecho por Kaléin Tamaríz
class MockRepository:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._categories = [
            {"id": 1, "name": "Robótica"},
            {"id": 2, "name": "Impresiones 3D"},
            {"id": 3, "name": "Drones"},
            {"id": 4, "name": "Electrónica"}
        ]
        self._products = [
            {"id": 101, "name": "Brazo Robótico v1", "price": 12500.0, "desc": "Manipulador de 6 GDL para cargas pequeñas"},
            {"id": 102, "name": "Set de Engranajes Personalizados", "price": 45.0, "desc": "Engranajes impresos en ASA de alto torque"},
            {"id": 103, "name": "Micro Servo", "price": 15.0, "desc": "Micro motor servo de 9g"},
            {"id": 104, "name": "Motor a Pasos NEMA 17", "price": 25.0, "desc": "Motor a pasos de alta precisión"},
            {"id": 105, "name": "Filamento PLA 1kg", "price": 20.0, "desc": "Filamento PLA de 1.75mm, negro"},
            {"id": 106, "name": "Filamento PETG 1kg", "price": 25.0, "desc": "Filamento PETG de 1.75mm, blanco"},
            {"id": 107, "name": "Marco de Cuadrirrotor", "price": 50.0, "desc": "Marco de drone de 5 pulgadas en fibra de carbono"},
            {"id": 108, "name": "Motor Brushless 2207", "price": 18.0, "desc": "Motor brushless de 2400KV"},
            {"id": 109, "name": "Controlador de Vuelo F4", "price": 45.0, "desc": "Controlador de vuelo F4 con OSD"},
            {"id": 110, "name": "Arduino Uno R3", "price": 25.0, "desc": "Placa de microcontrolador ATmega328P"},
            {"id": 111, "name": "Raspberry Pi 4", "price": 75.0, "desc": "Computadora de placa única con 4GB de RAM"},
            {"id": 112, "name": "Fuente de Alimentación para Protoboard", "price": 5.0, "desc": "Módulo de fuente de alimentación de 3.3V/5V"},
            {"id": 113, "name": "Cables Jumper", "price": 8.0, "desc": "Juego de 120 cables dupont"},
            {"id": 114, "name": "Kit de Resistencias", "price": 12.0, "desc": "600 resistencias de película metálica de 1/4W"},
            {"id": 115, "name": "Cautín", "price": 35.0, "desc": "Cautín de 60W con temperatura ajustable"},
            {"id": 116, "name": "Batería Lipo 3S", "price": 25.0, "desc": "Batería lipo 3S de 1500mAh"},
            {"id": 117, "name": "Batería Lipo 4S", "price": 35.0, "desc": "Batería lipo 4S de 1500mAh"},
            {"id": 118, "name": "Batería Lipo 6S", "price": 45.0, "desc": "Batería lipo 6S de 1300mAh"},
            {"id": 126, "name": "Filamento ABS 1kg", "price": 22.0, "desc": "Filamento ABS de 1.75mm, negro"},
            {"id": 127, "name": "Filamento TPU 1kg", "price": 28.0, "desc": "Filamento TPU flexible de 1.75mm"},
            {"id": 136, "name": "Motor DC 12V", "price": 10.0, "desc": "Motor DC de alto torque"},
            {"id": 137, "name": "Controlador de Motor L298N", "price": 4.0, "desc": "Controlador de motor de puente H doble"},
        ]
        self._junction = [
            {"p_id": 101, "c_id": 1}, {"p_id": 102, "c_id": 1}, {"p_id": 102, "c_id": 2},
            {"p_id": 103, "c_id": 1}, {"p_id": 104, "c_id": 1}, {"p_id": 104, "c_id": 2},
            {"p_id": 105, "c_id": 2}, {"p_id": 106, "c_id": 2}, {"p_id": 107, "c_id": 3},
            {"p_id": 108, "c_id": 3}, {"p_id": 109, "c_id": 3}, {"p_id": 110, "c_id": 4},
            {"p_id": 111, "c_id": 4}, {"p_id": 112, "c_id": 4}, {"p_id": 113, "c_id": 4},
            {"p_id": 114, "c_id": 4}, {"p_id": 115, "c_id": 4}, {"p_id": 116, "c_id": 3},
            {"p_id": 117, "c_id": 3}, {"p_id": 118, "c_id": 3}, {"p_id": 126, "c_id": 2},
            {"p_id": 127, "c_id": 2}, {"p_id": 136, "c_id": 1}, {"p_id": 137, "c_id": 1},
        ]
        self._media = [
            {"product_id": 101, "filename": "robot_arm.jpg", "is_primary": True},
            {"product_id": 102, "filename": "gears.png", "is_primary": True},
            {"product_id": 103, "filename": "servo.jpg", "is_primary": True},
            {"product_id": 104, "filename": "stepper.jpg", "is_primary": True},
            {"product_id": 105, "filename": "pla.jpg", "is_primary": True},
            {"product_id": 106, "filename": "petg.jpg", "is_primary": True},
            {"product_id": 107, "filename": "frame.jpg", "is_primary": True},
            {"product_id": 108, "filename": "motor.jpg", "is_primary": True},
            {"product_id": 109, "filename": "fc.jpg", "is_primary": True},
            {"product_id": 110, "filename": "arduino.jpg", "is_primary": True},
            {"product_id": 111, "filename": "rpi.jpg", "is_primary": True},
            {"product_id": 112, "filename": "breadboard_ps.jpg", "is_primary": True},
            {"product_id": 113, "filename": "jumper.jpg", "is_primary": True},
            {"product_id": 114, "filename": "resistors.jpg", "is_primary": True},
            {"product_id": 115, "filename": "soldering_iron.jpg", "is_primary": True},
            {"product_id": 116, "filename": "lipo_3s.jpg", "is_primary": True},
            {"product_id": 117, "filename": "lipo_4s.jpg", "is_primary": True},
            {"product_id": 118, "filename": "lipo_6s.jpg", "is_primary": True},
            {"product_id": 126, "filename": "abs.jpg", "is_primary": True},
            {"product_id": 127, "filename": "tpu.jpg", "is_primary": True},
            {"product_id": 136, "filename": "dc_motor.jpg", "is_primary": True},
            {"product_id": 137, "filename": "l298n.jpg", "is_primary": True},
        ]

    def get_categories(self):
        return self._categories

    def get_products(self, category_id: int = None):
        results = []
        for p in self._products:
            c_ids = [j["c_id"] for j in self._junction if j["p_id"] == p["id"]]
            if category_id and int(category_id) not in c_ids:
                continue
            
            cat_names = [c["name"] for c in self._categories if c["id"] in c_ids]
            p_media = [{"media_url": f"{self.base_url}/{m['filename']}", "is_primary": m['is_primary'], "position": 1} 
                       for m in self._media if m["product_id"] == p["id"]]
            
            primary = next((m["media_url"] for m in p_media if m["is_primary"]), None)

            results.append({
                **p, "categories": cat_names, "media": p_media, "primary_image": primary, "description": p.get("desc")
            })
        return results
