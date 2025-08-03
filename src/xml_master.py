from lxml import etree
import os



class MakerMPD:
    def __init__(self, global_path):
        self.global_path = global_path
        self.output_file = ''
        self.first_AdaptationSet = {}
        self.sounds = []
        self.qualities = []
        self.output_master = None


    def main_control(self):
        self.parse_sounds()
        self.parse_qualities()

        self.ShellCreate()
        self.edit_mpd()

    
    def ShellCreate(self):
        # Определяем пространства имен
        NSMAP = {
            'xsi': "http://www.w3.org/2001/XMLSchema-instance",
            None: "urn:mpeg:dash:schema:mpd:2011",  # Основное пространство имен (по умолчанию)
            'xlink': "http://www.w3.org/1999/xlink"
        }

        mpd_path = f"{self.global_path}/video/360p/video.mpd"
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(mpd_path, parser)

        mpd = tree.getroot()

        mpd_attrs = dict(mpd.attrib)  # Копируем все атрибуты
        
        # 3. Очищаем содержимое MPD, но сохраняем атрибуты
        mpd.clear()
        for attr, value in mpd_attrs.items():
            mpd.set(attr, value)  # Восстанавливаем атрибуты
            

        mpd.text = '\n    '  # Добавляем отступ

        # 4. Создаем структуру MPD
        period = etree.SubElement(mpd, "Period", start="PT0S")
        period.text = "\n        "
        period.tail = "\n    "

        adaptation_set = etree.SubElement(period, "AdaptationSet")
        adaptation_set.text = "\n            "
        adaptation_set.tail = "\n        "

        # Добавляем атрибуты из self.first_AdaptationSet
        for key, value in self.first_AdaptationSet.items():
            adaptation_set.set(key, value)

        # 5. Сохраняем новый MPD
        tree.write(
            f"{self.global_path}/master.mpd",
            pretty_print=True,
            encoding='utf-8',
            xml_declaration=True,
            standalone=False
        )
        
    
    def parse_sounds(self):
        sounds_list = [f for f in os.listdir(f'{self.global_path}/audio')]
        for index, name in enumerate(sounds_list):
            tree = etree.parse(f"{self.global_path}/audio/{name}/output.mpd")
            root = tree.getroot()

            adaptation_set = root.find(".//{*}AdaptationSet")
            adaptation_set.set("id", f"{index+1}")  # Меняем ID


            role = etree.SubElement(adaptation_set, "Role",  schemeIdUri="urn:mpeg:dash:role:2011", value=name)
            role.tail = "\n            "  # Отступ после BaseURL
            adaptation_set.insert(0, role)


            label = etree.SubElement(adaptation_set, "Label")
            label.text = f"{name}"  # Пример URL, можно изменить
            label.tail = "\n            "  # Отступ после BaseURL
            adaptation_set.insert(0, label)

            if index != len(sounds_list) - 1:
                adaptation_set.tail = '\n        '

            Represen = adaptation_set.find(".//{*}Representation")

            base_url = etree.SubElement(Represen, "BaseURL")
            base_url.text = f"audio/{name}/"  # Пример URL, можно изменить
            base_url.tail = "\n                "  # Отступ после BaseURL
            Represen.insert(0, base_url)

            self.sounds.append([adaptation_set, name])

    def parse_qualities(self):
        qualities_list = [int(f[:-1]) for f in os.listdir(f'{self.global_path}/video')]
        qualities_list.sort(reverse=True)

        for index, name in enumerate(qualities_list):
            tree = etree.parse(f"{self.global_path}/video/{name}p/video.mpd")
            root = tree.getroot()
            
            if not index:
                self.first_AdaptationSet = root.find(".//{*}AdaptationSet").attrib
                

            adaptation_set = root.find(".//{*}Representation")
            adaptation_set.set("id", f"{name}")  # Меняем ID

            base_url = etree.SubElement(adaptation_set, "BaseURL")
            base_url.text = f"video/{name}p/"  # Пример URL, можно изменить
            base_url.tail = "\n                "  # Отступ после BaseURL
            adaptation_set.insert(0, base_url)

            if index != len(qualities_list) - 1:
                adaptation_set.tail = '\n           '
                
            self.qualities.append([adaptation_set, name])


    def edit_mpd(self):
        output_file = f"{self.global_path}/master.mpd"
        output_tree = etree.parse(output_file)
        output_root = output_tree.getroot()

        period = output_root.find(".//{*}Period")
        adaptation_set = period.find("{*}AdaptationSet")

        for x in self.qualities:
            adaptation_set.append(x[0])

        for y in self.sounds:
            period.append(y[0])


        # 5. Сохраняем результат
        output_tree.write(
            output_file,
            pretty_print=True,
            encoding="UTF-8",
            xml_declaration=True
        )


if __name__ == '__main__':
    # C:/Admin/project/Python/dash-hls-_creator/mpd_test/test00
    print('Укажите директорию с dash проектом')
    lam = input(':')

    files_w = [f for f in os.listdir(lam)]

    for x in files_w:
        path = f'{lam}/{x}'
        debugStart = MakerMPD(global_path=path)
        debugStart.main_control()