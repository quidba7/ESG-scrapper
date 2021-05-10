@ECHO OFF
echo -- Scrap ESG score from Refinitive website
%windir%\System32\cmd.exe /k "C:\Users\Administrator\PycharmProjects\myscrapper\venv\Scripts\activate.bat & activate & C:\Users\Administrator\PycharmProjects\myscrapper\venv\Scripts\python.exe C:/Users/Administrator/PycharmProjects/myscrapper/refinitiv_esg/esg_score.py"
PAUSE