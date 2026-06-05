"""
Procesador que orquesta la descompresión de ZIPs y procesamiento de XMLs
Coordina el flujo completo de extracción y generación de reportes
"""

import os
import zipfile
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Tuple
from xml_parser import CFDIParser
from excel_generator import ExcelGenerator


class ZIPProcessor:
    """Procesador de archivos ZIP con XMLs CFDI"""
    
    def __init__(self):
        self.parser = CFDIParser()
        self.generator = ExcelGenerator()
        self.temp_dir = None
    
    def process_zip(self, zip_path: str, output_excel_path: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Procesa un archivo ZIP: descomprime y extrae XMLs
        
        Args:
            zip_path: Ruta del archivo ZIP
            output_excel_path: Ruta del Excel de salida
            
        Returns:
            Tupla (éxito, mensaje, estadísticas)
        """
        stats = {
            'total_files': 0,
            'xml_files_found': 0,
            'xml_files_processed': 0,
            'xml_files_failed': 0,
            'excel_generated': False
        }
        
        try:
            # Crea directorio temporal
            self.temp_dir = tempfile.mkdtemp()
            
            # Descomprime el ZIP
            success, msg = self._extract_zip(zip_path, self.temp_dir)
            if not success:
                return False, msg, stats
            
            # Busca y procesa XMLs
            xml_files = self._find_xml_files(self.temp_dir)
            stats['xml_files_found'] = len(xml_files)
            
            if xml_files == 0:
                return False, "No se encontraron archivos XML en el ZIP", stats
            
            # Parsea los XMLs
            parsed_data = []
            for xml_file in xml_files:
                data = self.parser.parse_xml(xml_file)
                if data:
                    parsed_data.append(data)
                    stats['xml_files_processed'] += 1
                else:
                    stats['xml_files_failed'] += 1
            
            if not parsed_data:
                return False, "No se pudieron procesar los archivos XML", stats
            
            # Genera el Excel
            if self.generator.generate_report(parsed_data, output_excel_path):
                stats['excel_generated'] = True
                message = f"Procesamiento exitoso: {stats['xml_files_processed']} XMLs procesados"
                return True, message, stats
            else:
                return False, "Error al generar el archivo Excel", stats
        
        except Exception as e:
            return False, f"Error durante el procesamiento: {str(e)}", stats
        
        finally:
            # Limpia directorio temporal
            self._cleanup_temp_dir()
    
    def _extract_zip(self, zip_path: str, extract_path: str) -> Tuple[bool, str]:
        """
        Extrae un archivo ZIP
        
        Args:
            zip_path: Ruta del ZIP
            extract_path: Directorio de destino
            
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            if not os.path.exists(zip_path):
                return False, f"El archivo ZIP no existe: {zip_path}"
            
            if not zipfile.is_zipfile(zip_path):
                return False, "El archivo no es un ZIP válido"
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            return True, "ZIP descomprimido exitosamente"
        
        except Exception as e:
            return False, f"Error descomprimiendo ZIP: {str(e)}"
    
    def _find_xml_files(self, root_path: str) -> List[str]:
        """
        Encuentra todos los archivos XML recursivamente
        
        Args:
            root_path: Directorio raíz de búsqueda
            
        Returns:
            Lista de rutas a archivos XML
        """
        xml_files = []
        
        try:
            for root, dirs, files in os.walk(root_path):
                for file in files:
                    if file.lower().endswith('.xml'):
                        xml_files.append(os.path.join(root, file))
        
        except Exception as e:
            print(f"Error searching for XML files: {str(e)}")
        
        return xml_files
    
    def _cleanup_temp_dir(self):
        """Limpia el directorio temporal"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                import shutil
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                print(f"Error cleaning up temp directory: {str(e)}")
