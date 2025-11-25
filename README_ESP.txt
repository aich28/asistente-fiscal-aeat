ASISTENTE FISCAL AEAT (MODULAR) – INSTRUCCIONES RÁPIDAS (MAC)

1) REQUISITOS
   - Tener instalado Python 3.10 o superior.
   - Tener una clave de API de OpenAI (https://platform.openai.com).

2) PREPARAR EL PROYECTO
   - Copia esta carpeta completa a tu Mac (por ejemplo, en Escritorio).
   - Abre la app "Terminal".
   - Ve a la carpeta del proyecto. Si la carpeta se llama "fiscal_aeat_modular" en el Escritorio:
     cd ~/Escritorio/fiscal_aeat_modular

3) CREAR ENTORNO VIRTUAL (OPCIONAL PERO RECOMENDADO)
     python3 -m venv venv
     source venv/bin/activate

4) INSTALAR DEPENDENCIAS
     pip install -r requirements.txt

5) CONFIGURAR LA CLAVE DE OPENAI
   - Copia el archivo ".env.example" renombrándolo a ".env".
   - Edita el archivo ".env" y pon tu clave real en:
     OPENAI_API_KEY=TU_CLAVE_DE_OPENAI_AQUI

6) EJECUTAR LA APLICACIÓN
     streamlit run app.py

   - Se abrirá una ventana en tu navegador (normalmente en http://localhost:8501).
   - Ahí podrás:
     * Subir un documento de la AEAT (PDF, DOCX, TXT).
     * Explicar tu caso en el cuadro de texto.
     * Elegir entre:
       - Solo análisis y estrategia.
       - Análisis + redacción de borrador de escrito.

7) USO COMERCIAL
   - Esta base te sirve como MVP (producto mínimo viable).
   - A partir de aquí, un desarrollador puede:
     * Añadir login, pagos, multiusuario.
     * Integrar llamadas reales a APIs oficiales (BOE, AEAT, etc.).
     * Crear plantillas DOCX/PDF con formato corporativo.
