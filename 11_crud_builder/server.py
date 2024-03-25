from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Base de datos simulada de tacos
tacos = {}


# Producto: tacos
class Tacos:
    def __init__(self):
        self.base = None
        self.guiso = None
        self.toppings = []
        self.salsa= None

    def __str__(self):
        return f"Base: {self.base}, Guiso: {self.guiso}, Toppings: {', '.join(self.toppings)}, Salsa:{self.salsa}"


# Builder: Constructor de tacos
class TacosBuilder:
    def __init__(self):
        self.taco = Tacos()

    def set_base(self, base):
        self.taco.base = base

    def set_guiso(self, guiso):
        self.taco.guiso = guiso

    def add_topping(self, topping):
        self.taco.toppings.append(topping)
    
    def set_salsa(self,salsa):
        self.taco.salsa = salsa

    def get_taco(self):
        return self.taco


# Director: Taqueria
class Taqueria:
    def __init__(self, builder):
        self.builder = builder

    def create_taco(self, base, guiso, toppings, salsa):
        self.builder.set_base(base)
        self.builder.set_guiso(guiso)
        for topping in toppings:
            self.builder.add_topping(topping)
        self.builder.set_salsa(salsa)
        return self.builder.get_tacos()


# Aplicando el principio de responsabilidad única (S de SOLID)
class TacosService:
    def __init__(self):
        self.builder = TacosBuilder()
        self.taqueria = Taqueria(self.builder)

    def create_taco(self, post_data):
        base = post_data.get("base", None)
        guiso = post_data.get("guiso", None)
        toppings = post_data.get("toppings", [])
        salsa = post_data.get("salsa", None)

        tacos = self.taqueria.create_taco(base, guiso, toppings, salsa)
        tacos[len(tacos) + 1] = tacos
        
        return tacos

    def read_tacos(self):
        return {index: tacos.__dict__ for index, tacos in tacos.items()}

    def update_tacos(self, index, post_data):
        if index in tacos:
            tacos = tacos[index]
            base = post_data.get("base", None)
            guiso = post_data.get("guiso", None)
            toppings = post_data.get("toppings", [])
            salsa = post_data.get("salsa", None)

            if base:
                tacos.base = base
            if guiso:
                tacos.guiso = guiso
            if toppings:
                tacos.toppings = toppings
            if salsa:
                tacos.salsa = salsa

            return tacos
        else:
            return None

    def delete_tacos(self, index):
        if index in tacos:
            return tacos.pop(index)
        else:
            return None


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


# Manejador de solicitudes HTTP
class TacosHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = TacosService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/tacos":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_tacos(data)
            HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        if self.path == "/tacos":
            response_data = self.controller.read_tacos()
            HTTPDataHandler.handle_response(self, 200, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/tacos/"):
            index = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_tacos(index, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de tacos no es válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/tacos/"):
            index = int(self.path.split("/")[2])
            deleted_tacos = self.controller.delete_tacos(index)
            if deleted_tacos:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": "Tacos eliminados correctamente"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de tacos no es válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=TacosHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()