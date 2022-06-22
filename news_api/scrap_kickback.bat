@ECHO OFF
echo -- Scrap news for kickback word
%windir%\System32\cmd.exe /k "C:\Users\Administrator\PycharmProjects\myscrapper\venv\Scripts\activate.bat & activate & C:\Users\Administrator\PycharmProjects\myscrapper\venv\Scripts\python.exe C:/Users/Administrator/PycharmProjects/myscrapper/news_api/scrap_news.py"