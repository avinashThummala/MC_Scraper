# -*- coding: utf-8 -*-

import scrapy

class MetroscubicosItem(scrapy.Item):

	MC_Listing_URL = scrapy.Field()
	MC_Ad_Code = scrapy.Field()

	MC_Title = scrapy.Field()
	MC_Description = scrapy.Field()			

	MC_Categoria_de_inmueble = scrapy.Field()
	MC_Tipo_de_inmueble = scrapy.Field()

	MC_Estado = scrapy.Field()
	MC_Municipio = scrapy.Field()
	MC_Colonia = scrapy.Field()
	MC_Calle_avenida = scrapy.Field()

	MC_Photo_1 = scrapy.Field()
	MC_Photo_2 = scrapy.Field()
	MC_Photo_3 = scrapy.Field()
	MC_Photo_4 = scrapy.Field()
	MC_Photo_5 = scrapy.Field()
	MC_Photo_6 = scrapy.Field()
	MC_Photo_7 = scrapy.Field()
	MC_Photo_8 = scrapy.Field()
	MC_Photo_9 = scrapy.Field()
	MC_Photo_10 = scrapy.Field()
	MC_Video = scrapy.Field()

	MC_Latitude = scrapy.Field()
	MC_Longitude = scrapy.Field()	
	MC_Telephone = scrapy.Field()		

	MC_Metros_cuadrados_de_construccion = scrapy.Field()
	MC_Numero_de_recamaras = scrapy.Field()
	MC_Numero_de_banos = scrapy.Field()
	MC_Numero_de_espacios_para_autos = scrapy.Field()
	MC_Edad = scrapy.Field()
	MC_Nivel_en_el_que_se_encuentra = scrapy.Field()
	MC_Ubicacion_cuarto_de_servicio = scrapy.Field()
	MC_Indiviso = scrapy.Field()
	MC_Linea_telefonica = scrapy.Field()
	MC_Numero_de_departamentos = scrapy.Field()
	MC_Cuota_de_mantenimiento = scrapy.Field()
	MC_Clave_interna = scrapy.Field()
	MC_Gas_Natural = scrapy.Field()
	MC_Amueblado = scrapy.Field()
	MC_Estudio = scrapy.Field()
	MC_Cisterna = scrapy.Field()
	MC_Aire_acondicionado = scrapy.Field()
	MC_Jacuzzi = scrapy.Field()
	MC_Escuelas_cercanas = scrapy.Field()
	MC_Alberca = scrapy.Field()
	MC_Zona_arbolada = scrapy.Field()
	MC_Cocina_integral = scrapy.Field()
	MC_Chimenea = scrapy.Field()
	MC_Vigilancia_privada = scrapy.Field()
	MC_Accesos = scrapy.Field()
	MC_Casa_de_veraneo = scrapy.Field()
	MC_Parques_cercanos = scrapy.Field()
	MC_Vista_panoramica = scrapy.Field()
	MC_Calefaccion = scrapy.Field()
	MC_Gimnasios_cercanos = scrapy.Field()
	MC_Metros_cuadrados_de_jardin = scrapy.Field()
	MC_No_se_admiten_ninos = scrapy.Field()
	MC_No_se_admiten_animales = scrapy.Field()
	MC_Solo_familias = scrapy.Field()
	MC_Para_ejecutivos = scrapy.Field()

	MC_Precio_de_venta = scrapy.Field()
	MC_Monto_Precio_de_venta = scrapy.Field()
	MC_Moneda_Precio_de_venta = scrapy.Field()
	MC_Concepto_precio_de_venta = scrapy.Field()

	MC_Precio_de_renta = scrapy.Field()
	MC_Monto_Precio_de_renta = scrapy.Field()
	MC_Moneda_Precio_de_renta = scrapy.Field()
	MC_Concepto_precio_de_renta = scrapy.Field()

	MC_Renta_vacacional = scrapy.Field()

	MC_Renta_vacacional_mensual = scrapy.Field()
	MC_Monto_Precio_de_renta_vacacional_mensual = scrapy.Field()
	MC_Moneda_Precio_de_renta_vacacional_mensual = scrapy.Field()

	MC_Renta_vacacional_semanal = scrapy.Field()
	MC_Monto_Precio_de_renta_vacacional_semanal = scrapy.Field()
	MC_Moneda_Precio_de_renta_vacacional_semanal = scrapy.Field()

	MC_Renta_vacacional_fin_de_semana = scrapy.Field()
	MC_Monto_Precio_de_renta_vacacional_fin_de_semana = scrapy.Field()
	MC_Moneda_Precio_de_renta_vacacional_fin_de_semana = scrapy.Field()

	MC_Renta_vacacional_diaria = scrapy.Field()
	MC_Monto_Precio_de_renta_vacacional_diaria = scrapy.Field()
	MC_Moneda_Precio_de_renta_vacacional_diaria = scrapy.Field()