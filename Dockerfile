FROM python:3.7
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y libaio1 wget unzip
WORKDIR /opt/oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
mkdir instantclient && mv instantclient_*/* instantclient/ && rmdir instantclient_*/

RUN cd /opt/oracle/instantclient && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci
RUN echo /opt/oracle/instantclient > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig
WORKDIR /app
#RUN setx path '%path%;C:\oracle\instantclient_19_3'
#RUN setx ORACLE_HOME 'C:\oracle\instantclient_19_3'
#ADD https://download.microsoft.com/download/6/A/A/6AA4EDFF-645B-48C5-81CC-ED5963AEAD48/vc_redist.x64.exe /vc_redist.x64.exe
#RUN C:\vc_redist.x64.exe /quiet /install
#RUN powershell.exe "wget https://download.oracle.com/otn_software/nt/instantclient/19300/instantclient-basic-windows.x64-19.3.0.0.0dbru.zip -OutFile cx.zip"
#RUN powershell.exe "wget https://download.oracle.com/otn_software/nt/instantclient/19300/instantclient-sdk-windows.x64-19.3.0.0.0dbru.zip -OutFile cxsdk.zip"
#RUN powershell -Command "expand-archive -Path 'cx.zip' -DestinationPath 'C:\oracle'"
#RUN powershell -Command "expand-archive -Path 'cxsdk.zip' -DestinationPath 'C:\oracle'"
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["manage.py run", "--host", "0.0.0.0"]
