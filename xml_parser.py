"""
Parser CFDI que extrae datos de XMLs
Extrae información de facturas electrónicas mexicanas
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
from datetime import datetime


class CFDIParser:
    """Parser para archivos CFDI (Comprobante Fiscal Digital por Internet)"""
    
    def __init__(self):
        self.namespaces = {
            'cfdi': 'http://www.sat.gob.mx/cfd/3',
            'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
    
    def parse_xml(self, xml_path: str) -> Optional[Dict[str, Any]]:
        """
        Parsea un archivo XML CFDI
        
        Args:
            xml_path: Ruta al archivo XML
            
        Returns:
            Diccionario con datos del CFDI o None si hay error
        """
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Extrae datos del encabezado
            header_data = self._extract_header(root)
            
            # Extrae conceptos
            concepts = self._extract_concepts(root)
            
            # Extrae impuestos
            taxes = self._extract_taxes(root)
            
            # Extrae timbre
            stamp = self._extract_stamp(root)
            
            return {
                'header': header_data,
                'concepts': concepts,
                'taxes': taxes,
                'stamp': stamp
            }
        except Exception as e:
            print(f"Error parsing {xml_path}: {str(e)}")
            return None
    
    def _extract_header(self, root: ET.Element) -> Dict[str, Any]:
        """Extrae datos del encabezado del CFDI"""
        header = {}
        
        try:
            # Atributos principales del Comprobante
            header['folio'] = root.get('folio', '')
            header['serie'] = root.get('serie', '')
            header['fecha'] = root.get('fecha', '')
            header['total'] = root.get('total', '')
            header['subtotal'] = root.get('subtotal', '')
            header['descuento'] = root.get('descuento', '')
            header['tipo_comprobante'] = root.get('tipoDeComprobante', '')
            header['moneda'] = root.get('moneda', 'MXN')
            header['version'] = root.get('version', '')
            
            # Emisor
            emisor = root.find('.//cfdi:Emisor', self.namespaces)
            if emisor is not None:
                header['emisor_rfc'] = emisor.get('rfc', '')
                header['emisor_nombre'] = emisor.get('nombre', '')
                header['emisor_regimen_fiscal'] = emisor.find('.//cfdi:RegimenFiscal', self.namespaces)
                if header['emisor_regimen_fiscal'] is not None:
                    header['emisor_regimen_fiscal'] = header['emisor_regimen_fiscal'].get('Regimen', '')
            
            # Receptor
            receptor = root.find('.//cfdi:Receptor', self.namespaces)
            if receptor is not None:
                header['receptor_rfc'] = receptor.get('rfc', '')
                header['receptor_nombre'] = receptor.get('nombre', '')
                header['receptor_uso_cfdi'] = receptor.get('usoCFDI', '')
            
            # Referencia
            ref = root.find('.//cfdi:CfdiRelacionados', self.namespaces)
            if ref is not None:
                header['tipo_relacion'] = ref.get('tipoRelacion', '')
        
        except Exception as e:
            print(f"Error extracting header: {str(e)}")
        
        return header
    
    def _extract_concepts(self, root: ET.Element) -> List[Dict[str, Any]]:
        """Extrae conceptos (líneas) del CFDI"""
        concepts = []
        
        try:
            items = root.findall('.//cfdi:Concepto', self.namespaces)
            
            for item in items:
                concept = {
                    'cantidad': item.get('cantidad', ''),
                    'unidad': item.get('unidad', ''),
                    'clave_prod_serv': item.get('claveProductoServicio', ''),
                    'descripcion': item.get('descripcion', ''),
                    'valor_unitario': item.get('valorUnitario', ''),
                    'importe': item.get('importe', ''),
                    'descuento': item.get('descuento', '')
                }
                concepts.append(concept)
        
        except Exception as e:
            print(f"Error extracting concepts: {str(e)}")
        
        return concepts
    
    def _extract_taxes(self, root: ET.Element) -> Dict[str, Any]:
        """Extrae información de impuestos"""
        taxes = {
            'trasladados': [],
            'retenciones': []
        }
        
        try:
            # Traslados
            traslados = root.findall('.//cfdi:Traslado', self.namespaces)
            for traslado in traslados:
                taxes['trasladados'].append({
                    'impuesto': traslado.get('impuesto', ''),
                    'tasa': traslado.get('tasa', ''),
                    'importe': traslado.get('importe', '')
                })
            
            # Retenciones
            retenciones = root.findall('.//cfdi:Retencion', self.namespaces)
            for retencion in retenciones:
                taxes['retenciones'].append({
                    'impuesto': retencion.get('impuesto', ''),
                    'tasa': retencion.get('tasa', ''),
                    'importe': retencion.get('importe', '')
                })
        
        except Exception as e:
            print(f"Error extracting taxes: {str(e)}")
        
        return taxes
    
    def _extract_stamp(self, root: ET.Element) -> Dict[str, Any]:
        """Extrae información del Timbre Fiscal Digital (TFD)"""
        stamp = {}
        
        try:
            tfd = root.find('.//tfd:TimbreFiscalDigital', self.namespaces)
            if tfd is not None:
                stamp['uuid'] = tfd.get('UUID', '')
                stamp['fecha_timbrado'] = tfd.get('FechaTimbrado', '')
                stamp['rfc_prov_certif'] = tfd.get('RFCProvCertif', '')
                stamp['leyenda'] = tfd.get('Leyenda', '')
                stamp['numero_certificado_sat'] = tfd.get('NoCertificadoSAT', '')
                stamp['numero_certificado_csd'] = tfd.get('noCertificado', '')
        
        except Exception as e:
            print(f"Error extracting stamp: {str(e)}")
        
        return stamp
