# -*- coding: utf-8 -*-
#
# j00zek: 
#

from __future__ import absolute_import #zmiana strategii ladowanie modulow w py2 z relative na absolute jak w py3
from time import localtime, strftime
from Components.Converter.Converter import Converter
from Components.Element import cached
import os

class j00zekModimieniny(Converter, object):
    def __init__(self, type):
        fileDict = '/etc/enigma2/BH-Imieniny.txt'
        Converter.__init__(self, type)
        
        if not os.path.exists(fileDict):
            with open(fileDict, 'w') as f:
                f.write("""01-01=Mieszka, Mieczysława, Marii
01-02=Izydora, Bazylego, Grzegorza
01-03=Arlety, Genowefy, Danuty
01-04=Tytusa, Anieli, Eugeniusza
01-05=Hanny, Szymona, Edwarda
01-06=Kacpra, Melchiora, Baltazara
01-07=Juliana, Lucjana, Rajmunda
01-08=Seweryna, Mścisława, Juliusza
01-09=Marceliny, Marianny, Juliana
01-10=Wilhelma, Dobrosława, Danuty
01-11=Honoraty, Teodozjusza, Matyldy
01-12=Grety, Arkadiusza, Rajmunda
01-13=Bogumiły, Weroniki, Hilarego
01-14=Feliksa, Domosława, Niny
01-15=Pawła, Arnolda, Izydora
01-16=Marcelego, Włodzimierza, Waldemara
01-17=Antoniego, Rościsława, Jana
01-18=Piotra, Małgorzaty, Moniki
01-19=Henryka, Mariusza, Marty
01-20=Fabiana, Sebastiana, Euzebiusza
01-21=Agnieszki, Jarosława, Sobiesława
01-22=Anastazego, Wincentego, Kasandry
01-23=Ildefonsa, Rajmunda, Daniela
01-24=Felicji, Franciszka, Rafała
01-25=Pawła, Miłosza, Elwiry
01-26=Tymoteusza, Michała, Tytusa
01-27=Przybysława, Anieli, Jerzego
01-28=Walerego, Radomira, Tomasza
01-29=Zdzisława, Franciszka, Anieli
01-30=Macieja, Martyny, Teofila
01-31=Marceli, Ludwiki, Jana
02-01=Brygidy, Ignacego, Seweryna
02-02=Marii, Miłosława, Kornela
02-03=Błażeja, Oskara, Telimeny
02-04=Andrzeja, Weroniki, Joanny
02-05=Agaty, Adelajdy, Saby
02-06=Doroty, Bogdana, Pawła
02-07=Ryszarda, Teodora, Romana
02-08=Hieronima, Sebastiana, Ireny
02-09=Apolonii, Eryki, Cyryla
02-10=Elwiry, Jacka, Scholastyki
02-11=Adolfa, Olgierda, Świętomira 
02-12=Eulalii, Radosława, Modesta
02-13=Grzegorza, Katarzyny, Gilberta
02-14=Cyryla, Metodego, Walentego
02-15=Jowity, Faustyna, Zygfryda
02-16=Danuty, Julianny, Daniela
02-17=Aleksego, Zbigniewa, Łukasza
02-18=Szymona, Konstancji, Flawiana
02-19=Arnolda, Konrada, Marcelego
02-20=Leona, Ludomira, Zenobiusza
02-21=Eleonory, Fortunata, Roberta
02-22=Marty, Małgorzaty, Piotra
02-23=Romany, Damiana, Polikarpa
02-24=Macieja, Bogusza, Sergiusza
02-25=Wiktora, Cezarego, Nicefora
02-26=Mirosława, Aleksandra, Otokara
02-27=Gabriela, Anastazji, Prokopa
02-28=Romana, Ludomira, Lecha
02-29=Lecha, Lutosława
03-01=Antoniny, Radosława, Dawida
03-02=Heleny, Halszki, Pawła
03-03=Maryny, Kunegundy, Tycjana
03-04=Łucji, Kazimierza, Eugeniusza
03-05=Adriana, Fryderyka, Teofila
03-06=Jordana, Agnieszki, Frydolina
03-07=Tomasza, Perpetuy, Felicyty
03-08=Beaty, Wincentego, Jana
03-09=Franciszki, Dominika, Rebeki
03-10=Cypriana, Marcela, Aleksandra
03-11=Ludosława, Konstantyna, Benedykta
03-12=Grzegorza, Justyna, Alojzego
03-13=Bożeny, Krystyny, Salomona
03-14=Leona, Matyldy, Łazarza
03-15=Klemensa, Longina, Ludwika
03-16=Gabriela, Hilarego, Izabeli
03-17=Patryka, Zbigniewa, Gertrudy
03-18=Cyryla, Edwarda, Boguchwały
03-19=Bogdana, Józefa, Leoncjusza
03-20=Klaudii, Eufemii, Maurycego
03-21=Lubomira, Benedykta, Filemona
03-22=Katarzyny, Bogusława, Zachariasza
03-23=Pelagii, Oktawiana, Feliksa
03-24=Marka, Gabriela, Katarzyny
03-25=Marioli, Wieczysława, Ireneusza
03-26=Larysy, Emanuela, Teodora
03-27=Lidii, Ernesta, Archibalda
03-28=Anieli, Sykstusa, Jana
03-29=Wiktoryna, Helmuta, Eustachego
03-30=Anieli, Kwiryna, Leonarda
03-31=Beniamina, Dobromierza, Leonarda
04-01=Teodory, Grazyny, Ireny
04-02=Wladysława, Franciszka, Teodozji
04-03=Ryszarda, Pankracego, Ingi
04-04=Izydora, Wacława, Zdzimira
04-05=Ireny, Wincentego, Dobromiła
04-06=Izoldy, Celestyna, Wilhelma
04-07=Rufina, Celestyna, Jana
04-08=Cezaryny, Dionizego, Julii
04-09=Marii, Dymitra, Heliodora
04-10=Michała, Makarego, Ezechiela
04-11=Filipa, Leona, Hermana
04-12=Juliusza, Lubosława, Zenona
04-13=Przemysława, Hermenegildy, Marcina
04-14=Bereniki, Waleriana, Justyny
04-15=Ludwiny, Waławy, Anastazji
04-16=Kseni, Cecylii, Bernardety
04-17=Patrycego, Roberta, Eliasza 
04-18=Bogusławy, Apoloniusza
04-19=Adolfa, Tymona, Leona
04-20=Czesława, Agnieszki, Mariana
04-21=Anzelma, Bartosza, Feliksa
04-22=Kai, Leonii, Sotera
04-23=Jerzego, Wojciecha, Adalberta
04-24=Horacego, Feliksa, Grzegorza
04-25=Marka, Jarosława, Wasyla
04-26=Marzeny, Klaudiusza, Marii
04-27=Zyty, Teofila, Felicji
04-28=Piotra, Walerii, Witalisa
04-29=Rity, Katarzyny, Bogusława
04-30=Mariana, Donaty, Balladyny
05-01=Jeremiasza, Filipa, Wiwalda
05-02=Zygmunta, Atanazego, Anatola
05-03=Marii, Antoniny, \xc5\xbbakliny 
05-04=Moniki, Floriana, Wladysława
05-05=Ireny, Waldemara, Penelopy
05-06=Judyty, Jakuba, Filipa
05-07=Gizeli, Ludmiły, Benedykta
05-08=Stanisława, Lizy, Wiktora
05-09=Bożydara, Grzegorza, Karoliny
05-10=Izydora, Antoniny, Symeona
05-11=Igi, Miry, Wladysławy
05-12=Pankracego, Dominika, Achillesa
05-13=Serwacego, Roberta, Glorii
05-14=Bonifacego, Dobiesława, Macieja
05-15=Zofii, Nadziei, Izydora
05-16=Andrzeja, Jędrzeja, Szymona
05-17=Paschalisa, Sławomira, Weroniki
05-18=Eryka, Feliksa, Jana
05-19=Iwa, Piotra, Celestyna
05-20=Bazylego, Bernardyna, Aleksandra
05-21=Wiktora, Kryspina, Tymoteusza
05-22=Heleny, Wiesławy, Ryty
05-23=Iwony, Dezyderego, Kryspina
05-24=Joanny, Zuzanny, Mileny
05-25=Grzegorza, Urbana, Magdaleny
05-26=Filipa, Pauliny, Alwina
05-27=Augustyna, Juliana, Magdaleny
05-28=Jaromira, Justa, Justyny
05-29=Magdaleny, Bogumily, Urszuli
05-30=Ferdynanda, Karola, Jana
05-31=Anieli, Petroneli, Petronii
06-01=Justyna, Anieli, Konrada
06-02=Marianny, Marcelina, Piotra
06-03=Leszka, Tamary, Karola
06-04=Karola, Kwiryny, Franciszka, 
06-05=Waltera, Bonifacego, Walerii
06-06=Norberta, Laurentego, Bogumila
06-07=Roberta, Wiesława, Jeremiego
06-08=Medarda, Maksyma, Seweryna
06-09=Pelagii, Dominika, Efrema
06-10=Bogumiła, Małgorzaty, Diany
06-11=Barnaby, Radomiła, Feliksa
06-12=Janiny, Onufrego, Leona
06-13=Lucjana, Antoniego, Gracji
06-14=Bazylego, Elwiry, Michała
06-15=Wita, Jolanty, Abrahama
06-16=Aliny, Benona, Anety
06-17=Laury, Marcjana, Alberta
06-18=Marka, Elżbiety, Amandy
06-19=Gerwazego, Protazego, Borzysława
06-20=Diny, Bogny, Florentyny
06-21=Alicji, Alojzego, Terencjusza
06-22=Pauliny, Tomasza, Jana
06-23=Wandy, Zenona, Arystoklesa
06-24=Jana, Danuty, Longiny
06-25=Łucji, Wilhelma, Doroty
06-26=Jana, Pawła, Wigiliusza
06-27=Maryli, Władysława, Cyryla
06-28=Leona, Ireneusza, Herona
06-29=Piotra, Pawła, Emy, Beaty
06-30=Emilii, Lucyny, Teobalda
07-01=Haliny, Mariana, Marcina
07-02=Jagody, Urbana, Marii
07-03=Jacka, Anatola, Tomasza
07-04=Odona, Malwiny, Elżbiety
07-05=Karoliny, Antoniego, Cyryli 
07-06=Gotarda, Dominiki, Lucji
07-07=Cyryla, Estery, Metodego
07-08=Edgara, Elżbiety, Eugeniusza
07-09=Lukrecji, Weroniki, Zenona
07-10=Sylwany, Witalisa, Antoniego
07-11=Olgi, Kaliny, Benedykta
07-12=Jana, Brunona, Bonifacego
07-13=Henryka, Kingi, Andrzeja
07-14=Ulryka, Bonawentury, Kamila
07-15=Henryka, Włodzimierza, Dawida
07-16=Mariki, Benity, Eustachego
07-17=Anety, Bogdana, Jadwigi
07-18=Erwina, Kamila, Szymona
07-19=Wincentego, Wodzisława, Marcina
07-20=Czesława, Hieronima, Małgorzaty
07-21=Daniela, Diany, Wawrzyńca
07-22=Bolesława, Magdaleny, Platona
07-23=Stwosza, Bogny, Brygidy
07-24=Kingi, Krystyny, Krzesimira
07-25=Walentyny, Krzysztofa, Jakuba
07-26=Anny, Mirosławy, Grażyny
07-27=Lilii, Julii, Natalii
07-28=Aidy, Marceli, Wiktora
07-29=Olafa, Marty, Ludmiły
07-30=Julity, Piotra, Aldony
07-31=Ignacego, Lubomira, Heleny
08-01=Nadii, Justyna, Juliana
08-02=Kariny, Gustawa, Euzebiusza
08-03=Lidii, Augusta, Nikodema
08-04=Dominika, Protazego, Jana
08-05=Oswalda, Marii, Mariana
08-06=Sławy, Jakuba, Oktawiana
08-07=Kajetana, Doroty, Sykstusa
08-08=Cypriana, Emiliana, Dominika
08-09=Romana, Ryszarda, Edyty
08-10=Borysa, Filomeny, Wawrzyńca
08-11=Klary, Zuzanny, Lecha
08-12=Innocentego, Lecha, Euzebii
08-13=Diany, Hipolita, Poncjana
08-14=Alfreda, Euzebiusza, Maksymiliana
08-15=Marii, Napoleona, Trzebiemira
08-16=Rocha, Stefana, Joachima
08-17=\xc5\xbbanny, Mirona, Jacka, Anity
08-18=Ilony, Bronisława, Heleny
08-19=Bolesława, Juliana, Magnusa
08-20=Bernarda, Samuela, Sobiesława
08-21=Joanny, Kazimiery, Piusa
08-22=Cezarego, Tymoteusza, Lamberta
08-23=Apolinarego, Filipa, Flawii
08-24=Jerzego, Bartosza, Haliny
08-25=Luizy, Ludwika, Elwira
08-26=Marii, Aleksandra, Zefiryny
08-27=Cezarego, Moniki, Józefa
08-28=Patrycji, Wyszomira, Augustyna
08-29=Beaty, Jana, Sabiny, Racibora
08-30=Szczęsnego, Feliksa, Róży
08-31=Bogdana, Ramony, Rajmunda
09-01=Idziego, Bronisława, Egona 
09-02=Juliana, Stefana, Wilhelma
09-03=Grzegorza, Izabeli, Szymona
09-04=Rozalii, Róży, Hermiony
09-05=Doroty, Teodora, Wawrzyńca
09-06=Beaty, Eugeniusza, Germana
09-07=Domosławy, Melchiora, Reginy
09-08=Marii, Adrianny, Serafiny
09-09=Czcibora, Sergiusza, Piotra
09-10=Łukasza, Aldony, Mścisława
09-11=Jacka, Prota, Dagny, Hiacynta
09-12=Gwidona, Amadeusza, Maji
09-13=Eugenii, Aureliusza, Jana
09-14=Roksany, Bernarda, Cypriana
09-15=Albina, Nikodema, Marii
09-16=Edyty, Kornela, Edyty
09-17=Franciszka, Roberta, Justyna
09-18=Irmy, Stanisława, Ireny
09-19=Januarego, Konstancji, Teodora
09-20=Filipiny, Eustachego, Euzebii
09-21=Jonasza, Mateusza, Hipolita
09-22=Tomasza, Maurycego, Joachima
09-23=Tekli, Bogusława, Poli
09-24=Gerarda, Ruperta, Tomiry
09-25=Aurelii, Wladysława, Kleofasa
09-26=Wawrzyńca, Kosmy, Damiana
09-27=Wincentego, Mirabeli, Justyny
09-28=Wacława, Tymona, Marka
09-29=Michała, Gabriela, Rafała
09-30=Wery, Honoriusza, Hieronima
10-01=Danuty, Remigiusza, Teresy
10-02=Teofila, Dionizego, Sławomira
10-03=Teresy, Heliodora, Jana
10-04=Rozalii, Edwina, Franciszka
10-05=Placyda, Apolinarego, Faustyny
10-06=Artura, Brunona, Alberty
10-07=Marii, Marka, Mirelli
10-08=Pelagii, Brygidy, Walerii
10-09=Amolda, Dionizego, Wincentego
10-10=Pauliny, Danieli, Leona
10-11=Aldony, Aleksandra, Dobromiry
10-12=Eustachego, Maksymiliana, Edwina
10-13=Geralda, Edwarda, Honorata
10-14=Liwii, Kaliksta, Bernarda
10-15=Jadwigi, Teresy, Leonarda
10-16=Gawła, Ambrożego, Florentyny
10-17=Wiktora, Marity, Ignacego
10-18=Juliana, Łukasza, Remigiusza
10-19=Ziemowita, Piotra, Kleopatry 
10-20=Ireny, Kleopatry, Jana
10-21=Urszuli, Hilarego, Jakuba
10-22=Halki, Filipa, Salomei
10-23=Marleny, Seweryna, Igi
10-24=Rafała, Marcina, Antoniego
10-25=Darii, Wilhelminy, Bonifacego
10-26=Lucjana, Ewarysta, Damiana
10-27=Iwony, Sabiny, Manfreda
10-28=Szymona, Tadeusza, Ksymeny
10-29=Euzebii, Wioletty, Felicjana
10-30=Zenobii, Przemysława, Edmunda
10-31=Urbana, Saturnina, Krzysztofa
11-01=Seweryna, Wiktoryny, Konrada
11-02=Bohdany, Bożydara, Malachiasza
11-03=Sylwii, Marcina, Huberta
11-04=Karola, Olgierda, Franciszki
11-05=Elżbiety, Sławomira, Dominika
11-06=Feliksa, Leonarda, Ziemowita
11-07=Antoniego, Zytomira, Ernesta
11-08=Seweryna, Bogdana, Klaudiusza
11-09=Aleksandra, Ludwika, Teodora
11-10=Leny, Ludomira, Leona
11-11=Marcina, Bartłomieja, Teodora
11-12=Renaty, Witolda, Jonasza
11-13=Mateusza, Izaaka, Stanisława
11-14=Rogera, Serafina, Wawrzyńca
11-15=Alberta, Leopolda, Artura
11-16=Gertrudy, Edmunda, Marii
11-17=Salomei, Grzegorza, Elżbiety
11-18=Romana, Klaudyny, Karoliny
11-19=Seweryny, Maksyma, Salomei
11-20=Anatola, Sędzimira, Rafała
11-21=Alberta, Janusza, Konrada
11-22=Cecylii, Wszemiły, Stefana
11-23=Adelii, Klemensa, Felicyty
11-24=Flory, Emmy, Chryzogona
11-25=Erazma, Katarzyny, Alana
11-26=Delfiny, Sylwestra, Konrada
11-27=Waleriana, Wirgiliusza, Maksyma
11-28=Lesława, Zdzisława, Stefana
11-29=Błażeja, Saturnina, Klementyny
11-30=Andrzeja, Maury, Konstantego
12-01=Natalii, Eligiusza, Edmunda
12-02=Balbiny, Bibianny, Pauliny
12-03=Franciszka, Ksawerego, Kasjana
12-04=Barbary, Krystiana, Jana
12-05=Sabiny, Krystyny, Edyty
12-06=Mikołaja, Jaremy, Emiliana
12-07=Marcina, Ambrożego, Teodora
12-08=Marii, Wirginiusza, Makarego
12-09=Wiesława Leokadii Joanny
12-10=Julii, Danieli, Bogdana
12-11=Damazego, Waldemara, Daniela
12-12=Dagmary, Aleksandra, Ady
12-13=Łucji, Otylii, Eugeniusza 
12-14=Alfreda, Izydora, Jana
12-15=Niny, Celiny, Waleriana
12-16=Albiny, Zdzisławy, Alicji
12-17=Olimpii, Lazarza, Floriana
12-18=Gracjana, Bogusława, Laurencji
12-19=Gabrieli, Dariusza, Eleonory
12-20=Bogumiły, Dominika, Ptolemeusza
12-21=Tomisława, Seweryna, Piotra
12-22=Zenona, Honoraty, Franciszki
12-23=Wiktorii, Sławomiry, Jana
12-24=Adama, Ewy, Eweliny
12-25=Anastazji, Eugenii, Natana
12-26=Dionizego, Szczepana, Teodora
12-27=Jana, \xc5\xbbanety, Maksyma
12-28=Teofilii, Godzisława, Cezarego
12-29=Dawida, Tomasza, Dominika
12-30=Rainera, Eugeniusza, Irmy
12-31=Sylwestra, Melanii, Mariusza
""")
                f.close()
        
        self.DailyInfoDict = {}
        with open(fileDict, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line == '' or not '=' in line:
                    continue
                else:
                    cfg = line.split('=')
                    self.DailyInfoDict[cfg[0].strip()] = cfg[1].strip()
            f.close()

    @cached
    def getText(self):
        MonthDay = strftime('%m-%d')
        retVal = self.DailyInfoDict.get(MonthDay, '')
        return retVal

    text = property(getText)