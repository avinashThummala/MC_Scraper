# -*- coding: utf-8 -*-

import sys, MySQLdb, hashlib, re
from scrapy.exceptions import DropItem
from scrapy.http import Request

class MetrosCubicosPipeline(object):

	def __init__(self):

		self.conn = MySQLdb.connect(user='root', passwd='baggio', db='pyScrapper', host='localhost', charset="utf8", use_unicode=True)
		self.cursor = self.conn.cursor()

	def getInteger(self, intStr):

		intStr = re.sub("[^0123456789]", '', intStr)

		if intStr:
			return int(intStr)		
		else:
			return None					

	def getFloat(self, floatStr):

		floatStr = re.sub("[^0123456789\.]", '', floatStr)

		if floatStr:
			return float(floatStr)		
		else:
			return None			

	def process_item(self, item, spider): 

	    try:

	        self.cursor.execute("""INSERT INTO metrosCubicos VALUES (

				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
				%s
				        	
	        	)""", (

				item['MC_Categoria_de_inmueble'].encode('utf-8'),
				item['MC_Tipo_de_inmueble'].encode('utf-8'),

				item['MC_Estado'].encode('utf-8'),
				item['MC_Municipio'].encode('utf-8'),
				item['MC_Colonia'].encode('utf-8'),
				item['MC_Calle_avenida'].encode('utf-8'),

				item['MC_Photo_1'].encode('utf-8'),
				item['MC_Photo_2'].encode('utf-8'),
				item['MC_Photo_3'].encode('utf-8'),
				item['MC_Photo_4'].encode('utf-8'),
				item['MC_Photo_5'].encode('utf-8'),
				item['MC_Photo_6'].encode('utf-8'),
				item['MC_Photo_7'].encode('utf-8'),
				item['MC_Photo_8'].encode('utf-8'),
				item['MC_Photo_9'].encode('utf-8'),
				item['MC_Photo_10'].encode('utf-8'),
				item['MC_Video'].encode('utf-8'),

				self.getFloat(item['MC_Latitude']),
				self.getFloat(item['MC_Longitude']),

				item['MC_Telephone'].encode('utf-8'),

				self.getFloat(item['MC_Metros_cuadrados_de_construccion']),
				self.getInteger(item['MC_Numero_de_recamaras']),
				self.getFloat(item['MC_Numero_de_banos']),
				self.getInteger(item['MC_Numero_de_espacios_para_autos']),
				self.getFloat(item['MC_Edad']),
				self.getInteger(item['MC_Nivel_en_el_que_se_encuentra']),
				item['MC_Ubicacion_cuarto_de_servicio'].encode('utf-8'),
				item['MC_Indiviso'].encode('utf-8'),
				item['MC_Linea_telefonica'].encode('utf-8'),
				self.getInteger(item['MC_Numero_de_departamentos']),
				item['MC_Cuota_de_mantenimiento'].encode('utf-8'),
				item['MC_Clave_interna'].encode('utf-8'),
				item['MC_Gas_Natural'].encode('utf-8'),
				item['MC_Amueblado'].encode('utf-8'),

				item['MC_Estudio'],
				item['MC_Cisterna'],
				item['MC_Aire_acondicionado'],
				item['MC_Jacuzzi'],
				item['MC_Escuelas_cercanas'],
				item['MC_Alberca'],
				item['MC_Zona_arbolada'],
				item['MC_Cocina_integral'],
				item['MC_Chimenea'],
				item['MC_Vigilancia_privada'],
				item['MC_Accesos'],
				item['MC_Casa_de_veraneo'],
				item['MC_Parques_cercanos'],
				item['MC_Vista_panoramica'],
				item['MC_Calefaccion'],
				item['MC_Gimnasios_cercanos'],
				item['MC_Metros_cuadrados_de_jardin'],
				item['MC_No_se_admiten_ninos'],
				item['MC_No_se_admiten_animales'],
				item['MC_Solo_familias'],
				item['MC_Para_ejecutivos'],

				item['MC_Precio_de_venta'],
				self.getFloat(item['MC_Monto_Precio_de_venta']),
				item['MC_Moneda_Precio_de_venta'].encode('utf-8'),
				item['MC_Concepto_precio_de_venta'].encode('utf-8'),

				item['MC_Precio_de_renta'],
				self.getFloat(item['MC_Monto_Precio_de_renta']),
				item['MC_Moneda_Precio_de_renta'].encode('utf-8'),
				item['MC_Concepto_precio_de_renta'].encode('utf-8'),

				item['MC_Renta_vacacional'],

				item['MC_Renta_vacacional_mensual'],
				self.getFloat(item['MC_Monto_Precio_de_renta_vacacional_mensual']),
				item['MC_Moneda_Precio_de_renta_vacacional_mensual'].encode('utf-8'),

				item['MC_Renta_vacacional_semanal'],
				self.getFloat(item['MC_Monto_Precio_de_renta_vacacional_semanal']),
				item['MC_Moneda_Precio_de_renta_vacacional_semanal'].encode('utf-8'),

				item['MC_Renta_vacacional_fin_de_semana'],
				self.getFloat(item['MC_Monto_Precio_de_renta_vacacional_fin_de_semana']),
				item['MC_Moneda_Precio_de_renta_vacacional_fin_de_semana'].encode('utf-8'),

				item['MC_Renta_vacacional_diaria'],
				self.getFloat(item['MC_Monto_Precio_de_renta_vacacional_diaria']),
				item['MC_Moneda_Precio_de_renta_vacacional_diaria'].encode('utf-8')	        	

	        ))

	        self.conn.commit()

	    except MySQLdb.Error, e:
	        print "Error %d: %s" % (e.args[0], e.args[1])	       
	        return item
