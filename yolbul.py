# Barış Adıgüzel - 181307059
import sys
import os.path

row = 0  # Row = Haritanın Satır sayısı
column = 0  # Column = Haritanın Sütun sayısı
start_index = ()  # Başlangıç indeksini atamak için aldık (Tuple)
finish_index = ()  # Bitiş indeksini atamak için aldık (Tuple)
power_cell = []  # Güç hücresinin indeksini atamak için aldık (List)
visited = []  # Hücre Gezinti listemiz  (List)
p_visited = []  # Power Cell hücresi için


# region Boolean Functions
# Condition statements for our maze function
# x = satır
# y = sütun

def is_power_cell(current_index):
    '''Güç hücresinde miyim?'''
    if Map[current_index[0]][current_index[1]] == 'H':  # Şuan ki hücre güç hücresinde mi?
        return True
    else:
        return False


def are_we_there_yet(current_index):
    '''Bitiş noktasına geldik mi?'''
    if Map[current_index[0]][current_index[1]] == 'F':  # Şuan ki hücre, bitiş noktasında mı?
        return True  # return True
    else:
        return False  # return False


def left_available(current_index):
    '''Sol tarafım boş mu?'''
    x = current_index[0]
    y = current_index[1]
    left = [x, y - 1]

    # Sol tarafı duvar değilse ve labirent sınırında değil ve gezilmemişse
    if y - 1 != -1 and Map[x][y - 1] != 'W' and left not in visited:
        if p_visited is not None:  # Yedek listem boş değil ise
            if left not in p_visited:  # Sol kısmım yedek listede yok ise
                return True  # Sola gidebilirim
            else:
                return False  # Varsa gitmem
        else:  # Boş ise klasik kısmın durumu
            return True
    else:
        return False


def right_available(current_index):
    '''Sağ tarafım boş mu?'''
    x = current_index[0]
    y = current_index[1]
    right = [x, y + 1]

    # Sağ tarafı duvar değilse ve labirent sınırında değil ve gezilmemişse
    if y != column - 1 and Map[x][y + 1] != 'W' and right not in visited:
        if p_visited is not None:  # Yedek listem boş değil ise
            if right not in p_visited:  # Sağ kısmım yedek listede yoksa
                return True  # Sağa gidebilirim
            else:
                return False  # Varsa gitmem
        else:  # Boş ise klasik kısmın durumu
            return True
    else:
        return False


def down_available(current_index):
    '''Aşağı tarafım boş mu'''
    x = current_index[0]
    y = current_index[1]
    down = [x + 1, y]

    # Aşağı tarafı duvar değilse ve labirent sınırında değil ve gezilmemişse
    if x != row - 1 and Map[x + 1][y] != 'W' and down not in visited:
        if p_visited is not None:  # Yedek listem boş değil ise
            if down not in p_visited:  # Aşağı kısmım yedek listede yoksa
                return True  # Aşağı inebilirim
            else:
                return False  # Varsa inmem
        else:  # Boş ise klasik kısmın durumu
            return True
    else:
        return False


def up_available(current_index):
    '''Yukarı tarafım boş mu'''
    x = current_index[0]
    y = current_index[1]
    up = [x - 1, y]

    # Üst tarafı duvar değilse ve labirent sınırında değil ve gezilmemişse
    if x - 1 != -1 and Map[x - 1][y] != 'W' and up not in visited:
        if p_visited is not None:  # Yedek listem boş değil ise
            if up not in p_visited:  # Üst kısmım yedek listede yoksa
                return True  # Yukarı çıkabilirim
            else:
                return False  # Varsa çıkamam
        else:  # Boş ise klasik kısmın durumu
            return True
    else:
        return False


# endregion

# region File I/O Functions
# This section reads & writes files

def mapping(file):
    '''Gönderilen dosya içeriklerini alıp bir koordinat haritası ve uygun yol haritasının listesini döndürür.'''
    global row
    global column
    global start_index
    global finish_index
    global power_cell

    # Dosya kontrolü
    try:
        text = open(file, 'r')
    except FileNotFoundError:
        print('Dosya bulunamadı. Lütfen dosya ismini doğru yazdığınızdan emin olunuz.')
        exit(0)
    else:  # yeni ekledim (sıkıntı çıkarsa kaldır)
        Map = list()  # Koordinat Haritamız

        for i in text:
            Map.append((i[:]).strip('\n'))  # bütün karakterleri alıyor ('\n' içerenleri siliyor)
            row += 1  # Satır sayısını vericek döngü sonunda

        text.close()  # İlgili dosyayı kapattık.

        column = len(Map[0])  # Sütun sayımız

        Map = [(' '.join(Map[i])).split(' ') for i in range(row)]  # Nested list yaptık (Labirentimizi oluşturduk)

        for i in range(row):  # Satırlar için döngü
            for j in range(column):  # Sütunlar için döngü
                if 'S' in Map[i][j]:  # Başlangıç noktasının adresini alıyoruz
                    start_index = (i, j)
                if 'F' in Map[i][j]:  # Bitiş noktasının adresini alıyoruz
                    finish_index = (i, j)
                if 'H' in Map[i][j]:  # Güç hücresi noktasının adresini alıyoruz (eğer varsa)
                    power_cell = [i, j]

        return Map


def result(map, txt_output):
    '''Labirent sonucunun çıktısını ikinci argümanda verilen dosyanın içine yazar.'''

    Maze = map[:]  # Bütün elemanlarını Maze nesnesine kopyaladık.
    printed = visited[1:-1]  # indis numarası '1' olucak elemanların listesini aldık

    if os.path.isfile(txt_output):  # cikti.txt adında bir dosyamız var mı?
        file = open(txt_output, 'w')  # Varsa 'Write' modunda dosyayı aç
    else:
        file = open(txt_output, 'x')  # Eğer yok ise dosyayı oluştur. ('x' parametresi

    for i, j in printed:  # Labirentin çözüm hücrelerin '1' olarak değiştirildi
        Maze[i][j] = '1'

    for i in range(row):  # S ve F hücreleri dışındaki hücreleri '0' yaptık.
        for j in range(column):
            if Maze[i][j] != 'S' and Maze[i][j] != 'F' and Maze[i][j] != '1':
                Maze[i][j] = '0'

    Maze = [','.join(Maze[i]) for i in range(row)]  # Satırlar birleştirildi.

    # Çıktı Dosyasına yazma işlemi
    for line in Maze:
        file.write(line)
        file.write('\n')

    file.close()  # İlgili dosyamızı kapattık

    return True


# endregion

# region Maze Functions
# This section contains finding possible paths and finding the finish point

def available_paths(current_index):
    '''Gelen şuan ki hücre içinde kaç yola ayrıldığını belirler.'''
    path_count = 0

    if up_available(current_index) is True:
        path_count += 1
    if down_available(current_index) is True:
        path_count += 1
    if right_available(current_index) is True:
        path_count += 1
    if left_available(current_index) is True:
        path_count += 1

    return path_count


def movement(map, current_index, path_no=0):
    '''Metin dosyasından oluşturulan matris ile başlangıç noktasını alıp, labirentin sonucunu çıkartır.'''
    global visited  # Gezilen hücrelerin listesi global olarak fonksiyona ekledik.
    global p_visited  # Power Cell için  listemiz (var ise kullanıcağımız)
    global save_point  # Kayıt noktası ve seçim sayısını global olarak ekledik.

    # Güç hücresi varsa
    if len(power_cell) == 2:
        # Bitiş noktasını duvar yap
        x = finish_index[0]
        y = finish_index[1]
        Map[x][y] = 'W'
    # Güç hücresi yoksa (silindikten sonra)
    if len(power_cell) == 0:
        # Bitiş çizgisini tekrar F yap
        x = finish_index[0]
        y = finish_index[1]
        Map[x][y] = 'F'

    if is_power_cell(current_index) is True:  # Eğer güncel hücre, güç hücresinde ise
        # Güç hücresini P yaptık
        Map[current_index[0]][current_index[1]] = 'P'
        p_visited = visited[:]  # Gezinti listesinin kopyasını alıyoruz.
        visited.clear()  # Gezinti listesini temizle
        temp = power_cell[:]  # Güç hücresini kopyala
        power_cell.clear()  # Güç hücresinin adresini sil
        return movement(Map, temp)

    if are_we_there_yet(current_index) is True:  # Eğer güncel hücre, bitiş noktasında ise (Base Case)
        if p_visited:  # Eğer yedek liste varsa
            visited = p_visited + visited  # visited ile birleştir
        visited.append(current_index)  # En son bulunduğumuz konum, bitiş noktasıdır onu da listemize ekliyoruz
        return True  # Labirent işlemi tamamlanmış olur

    # Çıkmaz sokak durumu
    if path_no != 0 and available_paths(current_index) == 0 and are_we_there_yet(current_index) is False:
        # Çıkmaz sokağa varırsak
        if path_no == 1:  # Eğer seçim bir ise, en son kayıt noktası hücresinin solundaki hücreyi duvar yap
            map[save_point[0]][save_point[1] - 1] = 'W'
        if path_no == 2:  # Eğer seçim iki ise, en son kayıt noktası hücresinin aşağısındaki hücreyi duvar yap
            map[save_point[0] + 1][save_point[1]] = 'W'
        if path_no == 3:  # Eğer seçim üç ise, en son kayıt noktası hücresinin sağındaki hücreyi duvar yap
            map[save_point[0]][save_point[1] + 1] = 'W'
        if path_no == 4:  # Eğer seçim dört ise, en son kayıt noktası hücresinin üstündeki hücreyi duvar yap.
            map[save_point[0] - 1][save_point[1]] = 'W'

        visited.clear()  # Gezme listesini sıfırla

        return movement(Map, list(start_index))  # Başlangıç noktasından tekrar başla

    # Tek yol mevcut ise
    if available_paths(current_index) == 1:
        # Normal hangi yol mevcut ise ilerle

        temp = [current_index[0], current_index[1]]

        if down_available(current_index) is True:
            '''Labirentte aşağı gider.'''
            visited.append(temp)
            x = current_index[0]  # Satır adresi
            current_index[0] = x + 1  # x değerini 1 arttır

            return movement(Map, current_index, path_no)

        if right_available(current_index) is True:
            '''Labirentte sağa gider.'''
            visited.append(temp)
            y = current_index[1]  # Sütun adresi
            current_index[1] = y + 1  # y değerini 1 arttır
            return movement(Map, current_index, path_no)

        if left_available(current_index) is True:
            visited.append(temp)
            '''Labirentte sola gider.'''
            y = current_index[1]  # Sütun adresi
            current_index[1] = y - 1  # y değerini 1 azalt

            return movement(Map, current_index, path_no)

        if up_available(current_index) is True:
            '''Labirentte  yukarı gider.'''
            visited.append(temp)
            x = current_index[0]  # Satır adresi
            current_index[0] = x - 1  # x değerini 1 azalttır

            return movement(Map, current_index, path_no)

    # Eğer birden fazla gidilecek yol var ise
    if available_paths(current_index) != 1:

        # Kayıt noktası nesnesi oluşturup, mevcut nesnemizi yeni nesneye kopyalarız.
        temp_x = current_index[0]
        temp_y = current_index[1]
        save_point = [temp_x, temp_y]  # Kayıt noktamız
        temp = [temp_x, temp_y]

        if left_available(current_index) is True:
            '''Labirentte sola gider.'''
            path_no = 1  # Sol kısım
            visited.append(temp)
            y = current_index[1]  # Sütun adresi
            current_index[1] = y - 1  # y değerini 1 azalt

            return movement(Map, current_index, path_no)

        if down_available(current_index) is True:
            '''Labirentte aşağı gider.'''
            path_no = 2  # Aşağı kısım
            visited.append(temp)
            x = current_index[0]  # Satır adresi
            current_index[0] = x + 1  # x değerini 1 arttır

            return movement(Map, current_index, path_no)

        if right_available(current_index) is True:
            '''Labirentte sağa gider.'''
            path_no = 3  # Sağ kısım
            visited.append(temp)
            y = current_index[1]  # Sütun adresi
            current_index[1] = y + 1  # y değerini 1 arttır

            return movement(Map, current_index, path_no)

        if up_available(current_index) is True:
            '''Labirentte  yukarı gider.'''
            path_no = 4  # Üst kısım
            visited.append(temp)
            x = current_index[0]  # Satır adresi
            current_index[0] = x - 1  # x değerini 1 azalttır

            return movement(Map, current_index, path_no)


# endregion

# region Main Function
# This is the section where the program starts
args_len = len(sys.argv)  # Python programını kaç argümanla çağırdığımızı alıyoruz

# Program çalıştığında kaç tane argüman aldığımızı test ediyoruz
if args_len == 3:
    # print('Başarılı argüman sayısı : 3')
    txt_input = sys.argv[1]  # ilk argümanı atadık
    txt_output = sys.argv[2]  # ikinci argümanı atadık

    #  Dosya tiplerinin kontrolü yapılıyor
    if txt_input.endswith('.txt') is False or txt_output.endswith('.txt') is False:
        print('Lütfen .txt uzantılı dosya isimlerini argüman olarak giriniz.')
        exit(0)
    else:  # Dosya tipleri doğru ise buradan devam et.

        Map = mapping(txt_input)  # Girilen metin dosyasının labirent haritasını ve uygun yol haritasını çıkartır
        is_finish = movement(Map, list(start_index))  # Labirentin çözümünü yapıyoruz.
        flag = result(Map,
                      txt_output)  # Labirentin çıktısını text dosyasına yazdırır. Eğer işlem bittiyse True döndürür

        if flag is True and is_finish is True:
            print('İşlem bitmiştir. %s dosyasına bakabilirsiniz.' % txt_output)
            exit(0)
        else:
            print('Çıktı yazdırılamadı.')
            exit(0)
else:
    print('Eksik veya fazla argüman girildi.')
    print('KULLANIMI : py yolbul.py {girdi.txt} {cikti.txt}')
    exit(0)
# endregion
