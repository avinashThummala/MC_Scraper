#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy, sys, locale, re, time, os, traceback
from metrosCubicos.items import MetroscubicosItem

import part0;
import part1;
import part2;

from scrapy.http import Request
from scrapy import Selector

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DOMAIN = 'www.metroscubicos.com'
DUMMY_URL = 'http://www.metroscubicos.com/resultados/'
WAIT_TIME = 5
MULTIPLIER = 60

class MCSpider(scrapy.Spider):

    name = 'mcspider'
    allowed_domains = [DOMAIN]
    start_urls = part0.getStartURLS()+part1.getStartURLS()+part2.getStartURLS()

    def __init__(self):

        """
        options = webdriver.ChromeOptions()
        options.add_extension("Block-image_v1.0.crx")

        self.driver = webdriver.Chrome(chrome_options = options)
        """

        self.driver = webdriver.PhantomJS(service_args=['--load-images=no'])
        self.driver.maximize_window() 

        """
        self.enterEmailInfo()
        self.driver.refresh()
        """

    def enterEmailInfo(self):

        self.driver.get(DUMMY_URL)

        mElement = WebDriverWait(self.driver, WAIT_TIME*MULTIPLIER).until(EC.visibility_of_element_located((By.ID, "ouibounce-modal")) )

        tEmail = self.driver.find_element_by_xpath("//form[@id=\'bounce-form\']/input[@name=\'email\']")
        tEmail.send_keys('dhthummala@gmail.com')

        sButton = self.driver.find_element_by_xpath("//form[@id=\'bounce-form\']/input[@type=\'button\']")
        sButton.click()      

    def extractText(self, eList, index):

        if len(eList)>index:
            return eList[index].strip()

        else:
            return ''                            

    def parse(self, response):

        hxs = Selector(response)

        newItem = MetroscubicosItem()

        newItem['MC_Listing_URL'] = response.url
        newItem['MC_Ad_Code'] = self.extractText( hxs.xpath("//span[@id=\'alfaclave\']/text()").extract(), 0)

        if newItem['MC_Ad_Code']:

            newItem['MC_Title'] = self.extractText( hxs.xpath("//div[@class=\'address-detalle-new\']/text()").extract(), 0)
            newItem['MC_Description'] = self.extractText( hxs.xpath("string(//div[@id=\'dvDescripcionAc\']/div)").extract(), 0)

            self.getAgentTelephone(newItem, response.url)

            self.getImageLinks(hxs, newItem)

            string = self.extractText(hxs.xpath("//div[@class=\'address-detalle-new\']/text()").extract(), 0)

            if string:        
                newItem['MC_Estado'] = string[string.rindex(',')+1:].strip()
            else:            
                newItem['MC_Estado'] = ''             

            newItem['MC_Municipio'] = self.extractText( hxs.xpath("//section[@itemtype=\'http://schema.org/PostalAddress\']/meta[@itemprop=\'addressRegion\']/@content").extract(), 0)   

            if not newItem['MC_Municipio']:

                string = response.url[38+len(newItem['MC_Estado']):]
                newItem['MC_Municipio'] = string[:string.index('/')].replace("-"," ")

            newItem['MC_Colonia'] = self.extractText( hxs.xpath("//section[@itemtype=\'http://schema.org/PostalAddress\']/meta[@itemprop=\'addressLocality\']/@content").extract(), 0)
            newItem['MC_Calle_avenida'] = self.extractText( hxs.xpath("//section[@itemtype=\'http://schema.org/PostalAddress\']/meta[@itemprop=\'streetAddress\']/@content").extract(), 0)

            string = self.extractText( hxs.xpath("//h1[@class=\'title-detalle-new\']/span[@itemprop=\'name\']/text()").extract(), 0)

            if string:

                sSList = string.split(' ')

                newItem['MC_Tipo_de_inmueble'] = sSList[0]
                newItem['MC_Categoria_de_inmueble'] = ''                        

                if len(sSList)>1:                
                    newItem['MC_Categoria_de_inmueble'] = sSList[-1]                

            else:

                newItem['MC_Tipo_de_inmueble'] = ''
                newItem['MC_Categoria_de_inmueble'] = ''

            self.getListingDetails(hxs, newItem)
            self.getBooleanValues(hxs, newItem)        

            newItem['MC_Video'] = self.extractText( response.xpath("//div[@id=\'video\']/div/iframe/@src").extract(), 0)   

            newItem['MC_Latitude'] = self.extractText( response.xpath("//meta[@itemprop=\'latitude\']/@content").extract(), 0)   
            newItem['MC_Longitude'] = self.extractText( response.xpath("//meta[@itemprop=\'longitude\']/@content").extract(), 0)                

            self.getPriceDetails(hxs, newItem)

            if newItem['MC_Numero_de_banos']=='':
                self.checkListingDetails(hxs, newItem, 1)

            if newItem['MC_Numero_de_recamaras']=='':
                self.checkListingDetails(hxs, newItem, 2)

            if newItem['MC_Metros_cuadrados_de_construccion']=='':
                self.checkListingDetails(hxs, newItem, 3)   

            if newItem['MC_Numero_de_espacios_para_autos']=='':
                self.checkListingDetails(hxs, newItem, 4)                        

            yield newItem

        else:
            print "Invalid Url: "+response.url

    def getAgentTelephone(self, newItem, url):

        self.driver.get(url)

        try:

            phoneNum = WebDriverWait(self.driver, WAIT_TIME).until(EC.presence_of_element_located((By.ID, "dvMuestraFon")) )            

            self.driver.execute_script("muestraFon()")
            newItem['MC_Telephone'] = self.driver.find_element_by_id('dvMuestraFon').text.replace("Tel: ", "")           

        except:

            print traceback.format_exc()
            print "Unable to obtain agent's phone number"
            newItem['MC_Telephone'] = ''

    def getBooleanValues(self, hxs, newItem):

        detailsList=[

            u'Estudio', u'Cisterna', u'Aire acondicionado', u'Jacuzzi', u'Escuelas cercanas', u'Alberca', 
            u'Zona arbolada', u'Cocina integral', u'Chimenea:', u'Vigilancia privada', u'Accesos:', u'Casa de veraneo', 
            u'Parques cercanos', u'Vista panorámica', u'Calefacción', u'Gimnasios cercanos', u'Metros cuadrados de jardín', 
            u'No se admiten niños', u'No se admiten animales', u'Sólo familias', u'Para ejecutivos'
        ]

        varList = [

            'MC_Estudio', 'MC_Cisterna', 'MC_Aire_acondicionado', 'MC_Jacuzzi', 'MC_Escuelas_cercanas', 'MC_Alberca',
            'MC_Zona_arbolada', 'MC_Cocina_integral', 'MC_Chimenea', 'MC_Vigilancia_privada', 'MC_Accesos', 'MC_Casa_de_veraneo',
            'MC_Parques_cercanos', 'MC_Vista_panoramica', 'MC_Calefaccion', 'MC_Gimnasios_cercanos', 'MC_Metros_cuadrados_de_jardin',
            'MC_No_se_admiten_ninos', 'MC_No_se_admiten_animales', 'MC_Solo_familias','MC_Para_ejecutivos'
        ]   

        for x in varList:
            newItem[x] = 0  

        keyElements = hxs.xpath("//ul[@class=\'adicionales\']/li/b/text()").extract()  
                
        for x in range(len(keyElements)):            

            keyElements[x] = keyElements[x].strip()

            if keyElements[x][-1]==':':
                keyElements[x] = keyElements[x][:-1]

            if keyElements[x] in detailsList:

                index = detailsList.index(keyElements[x])
                newItem[varList[index]] = 1   

    def getModifiedValue(self, valStr):

        if valStr and valStr[0]==':':
            return valStr[1:].strip()
        else:            
            return valStr

    def getListingDetails(self, hxs, newItem):

        detailsList=[

            u'm2 construcción', u'Recámaras', u'Baños', u'Número de espacios para autos',  
            u'Edad', u'Nivel en el que se encuentra', u'Ubicación cuarto de servicio', u'Indiviso', 
            u'Línea telefónica', u'Departamentos', u'Cuota de mantenimiento', u'Clave interna', u'Gas Natural', 
            u'Amueblado', u'Metros cuadrados de construcción'
        ]

        varList=[

            'MC_Metros_cuadrados_de_construccion', 'MC_Numero_de_recamaras', 'MC_Numero_de_banos', 'MC_Numero_de_espacios_para_autos',
            'MC_Edad', 'MC_Nivel_en_el_que_se_encuentra', 'MC_Ubicacion_cuarto_de_servicio', 'MC_Indiviso', 'MC_Linea_telefonica',
            'MC_Numero_de_departamentos', 'MC_Cuota_de_mantenimiento', 'MC_Clave_interna', 'MC_Gas_Natural','MC_Amueblado',
            'MC_Metros_cuadrados_de_construccion'                     
        ]

        for x in varList:
            newItem[x] = ''  

        
        dElements = hxs.xpath("//div[@id=\'dvDetalleP\']/div/ul/li/text()").extract()

        for x in range(0, len(dElements), 2):

            dElements[x] = dElements[x].strip()

            if dElements[x][-1]==':':
                dElements[x] = dElements[x][:-1]            

            if dElements[x] in detailsList:

                index = detailsList.index(dElements[x])
                newItem[varList[index]] = self.getModifiedValue( dElements[x+1].strip() )

        keyElements = hxs.xpath("//ul[@class=\'adicionales\']/li/b/text()").extract()  
        valueElements = hxs.xpath("//ul[@class=\'adicionales\']/li/text()").extract()  
        
        for x in range(len(keyElements)):            

            keyElements[x] = keyElements[x].strip()

            if keyElements[x][-1]==':':
                keyElements[x] = keyElements[x][:-1]            

            if keyElements[x] in detailsList:

                index = detailsList.index(keyElements[x])
                newItem[varList[index]] = self.getModifiedValue( valueElements[x].strip() )

    def getImageLinks(self, hxs, newItem):

        imgNList = [ 'MC_Photo_1', 'MC_Photo_2', 'MC_Photo_3', 'MC_Photo_4', 'MC_Photo_5', 'MC_Photo_6', 'MC_Photo_7', 'MC_Photo_8', 'MC_Photo_9', 'MC_Photo_10' ]

        for x in imgNList:
            newItem[x]=''

        iIndex = 0    
        for x in hxs.xpath("//div[@class=\'slides\']/div/a/@href").extract():

            newItem[imgNList[iIndex]] = x
            iIndex = iIndex+1

            if iIndex>9:
                break

    def fillPriceVals(self, pStr, newItem, monto, moneda):

        if 'USD' in pStr:
            newItem[moneda] = u'Dólares'
        else:
            newItem[moneda] = u'Pesos'

        newItem[monto] = pStr            

    def fillPriceCategory(self, hxs, newItem):

        varList =[
                                    
            'MC_Precio_de_venta', 'MC_Precio_de_renta', 'MC_Renta_vacacional','MC_Renta_vacacional_mensual',
            'MC_Renta_vacacional_semanal', 'MC_Renta_vacacional_fin_de_semana', 'MC_Renta_vacacional_diaria'
        ]

        for x in varList:
            newItem[x] = 0

        priceStr = self.getPrice(hxs)        

        if newItem['MC_Categoria_de_inmueble'] == 'Renta':

            newItem['MC_Precio_de_renta'] = 1  

            self.fillPriceVals(priceStr, newItem, 'MC_Monto_Precio_de_renta', 'MC_Moneda_Precio_de_renta') 

            if u'por m\xb2' in priceStr:
                newItem['MC_Concepto_precio_de_renta'] = u'Precio metro cuadrado'
            else:
                newItem['MC_Concepto_precio_de_renta'] = u'Precio total'                       

        elif newItem['MC_Categoria_de_inmueble'] == 'Venta':

            newItem['MC_Precio_de_venta'] = 1

            self.fillPriceVals(priceStr, newItem, 'MC_Monto_Precio_de_venta', 'MC_Moneda_Precio_de_venta')                        

            if u'por m\xb2' in priceStr:
                newItem['MC_Concepto_precio_de_venta'] = u'Precio metro cuadrado'
            else:
                newItem['MC_Concepto_precio_de_venta'] = u'Precio total'                                   

        if newItem['MC_Categoria_de_inmueble'] == 'Vacacional':

            newItem['MC_Renta_vacacional'] = 1            
            newItem['MC_Renta_vacacional_mensual'] = 1

            self.fillPriceVals(priceStr, newItem, 'MC_Monto_Precio_de_renta_vacacional_mensual', 'MC_Moneda_Precio_de_renta_vacacional_mensual')                                    


    def getPriceDetails(self, hxs, newItem):
    
        varList =[
                                    
            'MC_Monto_Precio_de_venta', 'MC_Moneda_Precio_de_venta', 'MC_Concepto_precio_de_venta',
            'MC_Monto_Precio_de_renta', 'MC_Moneda_Precio_de_renta', 'MC_Concepto_precio_de_renta',
            'MC_Monto_Precio_de_renta_vacacional_mensual', 'MC_Moneda_Precio_de_renta_vacacional_mensual',
            'MC_Monto_Precio_de_renta_vacacional_semanal', 'MC_Moneda_Precio_de_renta_vacacional_semanal',
            'MC_Monto_Precio_de_renta_vacacional_fin_de_semana', 'MC_Moneda_Precio_de_renta_vacacional_fin_de_semana',
            'MC_Monto_Precio_de_renta_vacacional_diaria', 'MC_Moneda_Precio_de_renta_vacacional_diaria' 
        ]

        for x in varList:
            newItem[x] = ''

        self.fillPriceCategory(hxs, newItem)

        index = 1
        for x in hxs.xpath("//div[@id=\'dvPRenta\']/div/table/tr[2]/td/text()").extract():

            if x==u'Por d\xeda':

                newItem['MC_Renta_vacacional_diaria'] = 1

                priceStr = self.extractText( hxs.xpath("//div[@id=\'dvPRenta\']/div/table/tr[3]/td["+str(index)+"]/text()").extract(), 0) 
                self.fillPriceVals(priceStr, newItem, 'MC_Monto_Precio_de_renta_vacacional_diaria', 'MC_Moneda_Precio_de_renta_vacacional_diaria')

            elif x==u'Por fin de semana':

                newItem['MC_Renta_vacacional_fin_de_semana'] = 1                

                priceStr = self.extractText( hxs.xpath("//div[@id=\'dvPRenta\']/div/table/tr[3]/td["+str(index)+"]/text()").extract(), 0) 
                self.fillPriceVals(priceStr, newItem, 'MC_Monto_Precio_de_renta_vacacional_fin_de_semana', 'MC_Moneda_Precio_de_renta_vacacional_fin_de_semana')                

            elif x==u'Semanal':

                newItem['MC_Renta_vacacional_semanal'] = 1                        

                priceStr = self.extractText( hxs.xpath("//div[@id=\'dvPRenta\']/div/table/tr[3]/td["+str(index)+"]/text()").extract(), 0) 
                self.fillPriceVals(priceStr, newItem, 'MC_Monto_Precio_de_renta_vacacional_semanal', 'MC_Moneda_Precio_de_renta_vacacional_semanal')                                

            index = index+1

    def getRelevantIndexes(self, hxs, numItem):

        tHeaderList = hxs.xpath('//table[@class=\'table table-striped\']/thead/tr/th/text()').extract()

        try:
            if tHeaderList:  

                if numItem==1:
                    return tHeaderList.index('Precio')+1, tHeaderList.index(u'Baños')+1
                
                elif numItem==2:
                    return tHeaderList.index('Precio')+1, tHeaderList.index(u'Recámaras')+1

                elif numItem==3:
                    return tHeaderList.index('Precio')+1, tHeaderList.index(u'm² const.')+1

                elif numItem==4:
                    return tHeaderList.index('Precio')+1, tHeaderList.index(u'Espacios p/auto')+1

            else:
                return -1, -1
                
        except:
            return -1,-1                

    def getRelevantRowIndex(self, hxs, pCIndex):

        index = 0

        while True:     

            index = index+1

            cList = hxs.xpath('//table[@class=\'table table-striped\']/tbody/tr['+str(index)+']/td['+str(pCIndex)+']/text()').extract()

            if cList:
                if self.compareFloats( self.extractText( cList, 0), self.getPrice(hxs) ):
                    return index
            else:
                break

        return -1                                

    def checkListingDetails(self, hxs, newItem, numItem):

        pCIndex, oIndex = self.getRelevantIndexes(hxs, numItem)

        if pCIndex<0:
            return

        rowIndex = self.getRelevantRowIndex(hxs, pCIndex)

        if rowIndex<0:
            return          

        if numItem==1:
            if oIndex>0:
                newItem['MC_Numero_de_banos'] = self.extractText( hxs.xpath('//table[@class=\'table table-striped\']/tbody/tr['+str(rowIndex)+']/td['+str(oIndex)+']/text()').extract(), 0)

        elif numItem==2:
            if oIndex>0:
                newItem['MC_Numero_de_recamaras'] = self.extractText( hxs.xpath('//table[@class=\'table table-striped\']/tbody/tr['+str(rowIndex)+']/td['+str(oIndex)+']/text()').extract(), 0)

        elif numItem==3:
            if oIndex>0:
                newItem['MC_Metros_cuadrados_de_construccion'] = self.extractText( hxs.xpath('//table[@class=\'table table-striped\']/tbody/tr['+str(rowIndex)+']/td['+str(oIndex)+']/text()').extract(), 0)

        elif numItem==4:
            if oIndex>0:
                newItem['MC_Numero_de_espacios_para_autos'] = self.extractText( hxs.xpath('//table[@class=\'table table-striped\']/tbody/tr['+str(rowIndex)+']/td['+str(oIndex)+']/text()').extract(), 0)

    def getFloat(self, floatStr):

        floatStr = re.sub("[^0123456789\.]", '', floatStr)

        if floatStr:
            return float(floatStr)      
        else:
            return None             

    def compareFloats(self, str1, str2):

        f1=self.getFloat(str1)
        f2=self.getFloat(str2)

        if f1!=None and f2!=None:
            if f1==f2:
                return True

        return False

    def getPrice(self, hxs):

        priceStr = self.extractText( hxs.xpath("//p[@class=\'precio \']/span/text()").extract(), 0)

        if priceStr:
            return priceStr
        else:
            return self.extractText( hxs.xpath("//p[@class=\'precio bajo\']/span/text()").extract(), 0)                 