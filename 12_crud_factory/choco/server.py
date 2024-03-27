from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Base de datos simulada de vehículos
chocolates = {}


class DeliveryChoco:
    def __init__(self, tipo, peso, sabor, relleno):
        self.tipo = tipo
        self.peso = peso
        self.sabor = sabor
        self.relleno = relleno


class Tabletas(DeliveryChoco):
    def __init__(self, peso, sabor,relleno):
        super().__init__("tabletas", peso, sabor,relleno)


class Bombones(DeliveryChoco):
    def __init__(self, peso, sabor, relleno):
        super().__init__("bombones", peso, sabor, relleno)

class Trufas(DeliveryChoco):
    def __init__(self, peso, sabor, relleno):
        super().__init__("trufas", peso, sabor, relleno)


class DeliveryFactory:
    @staticmethod
    def create_choco(tipo, peso, sabor, relleno):
        if tipo == "tabletas":
            return Tabletas(peso, sabor, None)
        elif tipo == "bombones":
            return Bombones(peso, sabor, relleno)
        elif tipo == "trufas":
            return Trufas(peso, sabor, relleno)
        else:
            raise ValueError("Tipo de chocolate no válido")


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


class DeliveryService:
    def __init__(self):
        self.factory = DeliveryFactory()

    def add_choco(self, data):
        tipo = data.get("tipo", None)
        peso = data.get("peso", None)
        sabor = data.get("sabor", None)
        relleno = data.get("relleno", None)

        delivery_choco = self.factory.create_choco(tipo, peso, sabor, relleno)
        chocolates[len(chocolates) + 1] = delivery_choco
        return delivery_choco

    def list_choco(self):
        return {index: chocolates.__dict__ for index, chocolates in chocolates.items()}

    def update_choco(self, choco_id, data):
        if choco_id in chocolates:
            chocos = chocolates[choco_id]
            tipo = data.get("tipo", None)
            sabor = data.get("sabor", None)
            relleno = data.get("relleno", None)
            if tipo:
                chocos.tipo = tipo
            if sabor:
                chocos.sabor = sabor
            if relleno:
                chocos.relleno= relleno
            return chocos
        else:
            return ValueError

    def delete_choco(self, choco_id):
        if choco_id in chocolates:
            del chocolates[choco_id]
            return {"message": "Chocolate eliminado"}
        else:
            return None


class DeliveryRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.delivery_service = DeliveryService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/chocolates":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.delivery_service.add_choco(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_GET(self):
        if self.path == "/chocolates":
            response_data = self.delivery_service.list_choco()
            HTTPDataHandler.handle_response(self, 200, response_data)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_PUT(self):
        if self.path.startswith("/chocolates/"):
            choco_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.delivery_service.update_choco(choco_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Chocolate no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_DELETE(self):
        if self.path.startswith("/chocolates/"):
            choco_id = int(self.path.split("/")[-1])
            response_data = self.delivery_service.delete_choco(choco_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "chocolate no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, DeliveryRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()