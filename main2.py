from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from pyBCV import Currency

class CajaProducto(BoxLayout):
    nombre = StringProperty("")
    precio = StringProperty("")
    precio_numerico = NumericProperty(0.0)

class MiPantalla(BoxLayout):
    
    texto_total = StringProperty("Total: $0.00 ref")
    texto_bolivares = StringProperty("Total: 0.00 Bs")
    total_acumulado = NumericProperty(0.0) 
    total_bs = NumericProperty(0.0)

    currency = Currency()

    usd_rate = currency.get_rate(currency_code='USD', prettify=False)
    fecha = currency.get_rate(currency_code='Fecha')

    dolar = round(float(usd_rate), 2)  

    # Productos llamados

    productos_llamados = []

    dic = {
        "Manzana": 10.5,
        "Durazno": 5.2,
        "Pera": 7,
        "Piña": 8,
        "Caramelo": 1
    }
   
    def buscar_y_agregar(self, texto_buscado):
        producto = texto_buscado.strip().capitalize()
        
        if producto in self.dic:
            precio_producto = self.dic[producto]

            # 1. Creamos la caja visual (Como lo hace tu función agregar_producto_a_lista)
            nueva_caja = CajaProducto(
                nombre=producto, 
                precio=f"${precio_producto:.2f}",
                precio_numerico=precio_producto
            )

            # 2. Guardamos la referencia de ESTA caja exacta en la lista interna
            self.productos_llamados.append({
                "nombre": producto,
                "precio": precio_producto,
                "caja_id": nueva_caja  # <--- ID ÚNICO VINCULADO
            })
            
            # 3. La agregamos al contenedor
            self.ids.contenedor_productos.add_widget(nueva_caja)
            
            # Recalculamos totales evitando imprecisiones de Python
            self.total_acumulado = round(self.total_acumulado + precio_producto, 2)
            self.texto_total = f"Total: ${self.total_acumulado:.2f} ref"

            self.total_bs = round(self.total_acumulado * self.dolar, 2)
            self.texto_bolivares = f"Total: {self.total_bs:.2f} Bs"
            
            self.ids.entrada_texto.text = ""

    def agregar_producto_a_lista(self, nombre_prod, precio_prod):
        nueva_caja = CajaProducto(
            nombre=nombre_prod, 
            precio=f"${precio_prod:.2f}",
            precio_numerico=precio_prod
        )

        self.ids.contenedor_productos.add_widget(nueva_caja)
        
    def eliminar(self):
        self.productos_llamados.clear()
        self.ids.contenedor_productos.clear_widgets()
        self.total_acumulado = 0.0
        self.texto_total = f"Total: ${self.total_acumulado:.2f} ref"

        self.total_bs = 0.0
        self.texto_bolivares = f"Total: {self.total_bs:.2f} bs"

        self.ids.entrada_texto.text = ""


    def eliminar_un_producto(self, caja_a_eliminar):
        # Restamos el precio usando round para cuadres de caja exactos
        self.total_acumulado = round(self.total_acumulado - caja_a_eliminar.precio_numerico, 2)
        self.texto_total = f"Total: ${self.total_acumulado:.2f} ref"
        
        self.total_bs = round(self.total_acumulado * self.dolar, 2)
        self.texto_bolivares = f"Total: {self.total_bs:.2f} bs"
        
        # 4. Buscamos por la caja exacta que envió el botón 'X' de tu .kv
        for item in self.productos_llamados:
            if item["caja_id"] == caja_a_eliminar: # <--- SEGURO: Compara objetos, no nombres
                self.productos_llamados.remove(item)
                break
        
        # Eliminamos el widget de la pantalla
        self.ids.contenedor_productos.remove_widget(caja_a_eliminar)

class MiApp(App):
    def build(self):
        vista = MiPantalla()

        self.title = "Total price"
        
        return vista

if __name__ == '__main__':
    MiApp().run()