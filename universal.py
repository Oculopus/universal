#v1.017
import smtplib
import time
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import os
import configparser
import datetime
import traceback

try:
       #Дата сейчас
       current_date = str(datetime.date.today())

       #Cправочник с конфигом.
       config = configparser.ConfigParser()
       config.read('settings.ini')
       way_send = config['WAY']['way_send']
       way = config['WAY']['way']
       way_file = config['WAY']['way_file']
       zip = config['WAY']['zip']
       recipients = config['RECIPIENTS']['recipients']
       login = config['CONNECT']['login']
       passw = config['CONNECT']['passw']
       host = config['CONNECT']['host']
       name_f = config['FILE']['file']
       theme_l = config['LETTER']['theme']
       text_l = config['LETTER']['text']

       log = open("log" + current_date + ".log", "w")

       # Проверка наличия файла
       check_file = len(os.listdir(path=way_send))

       while True:
              if check_file >= 1:
                     print("Файл найден, начинаю архивацию.")
                     log.write((datetime.datetime.today() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                     log.write(" Файл найден, начинаю архивацию. \n")
                     os.system(zip)
                     break
              else:
                     print("Выгрузка отсутствует, посплю часок.")
                     log.write((datetime.datetime.today() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                     log.write(" Выгрузка отсутствует, посплю часок. \n")
                     time.sleep(3600)

       # Подсчёт кол-ва архивов
       couzip = len(os.listdir(path=way_file))

       def body():

              # Функция формирования письма
              def sender():
                     # Тело письма
                     text = text_l
                     part_text = MIMEText(text, 'plain')

                     msg = MIMEMultipart()
                     msg['From'] = 'OPKSZ_Line2EKS@omega.sbrf.ru'
                     msg['To'] = ','.join([recipients])
                     msg['Subject'] = theme_l
                     msg.attach(part)
                     msg.attach(part_text)

                     # Отправка письма
                     server = smtplib.SMTP('smtpas.omega.sbrf.ru', 25)
                     server.ehlo()
                     server.starttls()
                     server.login(login, passw)
                     server.sendmail(msg['From'], recipients, msg.as_string())
                     server.quit()

              i = 1
              while i <= couzip:
                     # Добавление файла в письмо.
                     if os.path.isfile(way_file + "\\" + name_f + ".7z.part0" + str(i) + '.rar'):
                            filepatch = way_file + "\\" + name_f + ".7z.part0" + str(i) + '.rar'
                            basename = os.path.basename(filepatch)
                            part = MIMEBase('application', "octet-stream")
                            part.set_payload(open(filepatch, "rb").read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename)
                            sender()
                            print(str(i) + ' письмо успешно отправлено на', recipients)
                            log.write((datetime.datetime.today() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                            log.write(str(i) + ' письмо успешно отправлено. \n')
                            i += 1
                     else:
                            print('Возникла ошибка при отправке' + str(i) + 'файла архива.')
                            log.write((datetime.datetime.today() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                            log.write(' Возникла ошибка при отправке' + str(i) + 'файла архива. \n')

       #Проверка наличия архива
       i = 1
       while True:
              check_zip = os.path.exists(way_file + "\\" + name_f + ".7z.part01.rar")
              if check_zip == True:
                     body()
                     break
              else:
                     print("Архив отсутствует, посплю минуту.")
                     log.write((datetime.datetime.today() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                     log.write(" Архив отсутствует, посплю минуту. \n")
                     time.sleep(60)

       #Удаление файлов после себя
       print("Начинаю удалять файлы.")
       log.write((datetime.datetime.today() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
       log.write(" Начинаю удалять файлы.\n")
       time.sleep(30)

       i = 1
       while i >= couzip:
              if os.path.isfile(way + "\\" + name_f + ".7z.part0" + str(i) + '.rar'):
                     os.remove(way + "\\" + name_f + ".7z.part0" + str(i) + '.rar')
                     print(str(1 + i) + " файл успешно удалён.")
                     log.write((datetime.datetime.today() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                     log.write(str(1 + i) + " файл успешно удалён. \n")
              else:
                     print(str(1 + i) + "файла для удаления не существует.")
                     log.write((datetime.datetime.today() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                     log.write(str(1 + i) + " файла для удаления не существует. \n")


       log.close()
except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
print("Лог записан")
time.sleep(30)