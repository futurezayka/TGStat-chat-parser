from bs4 import BeautifulSoup


class TGStatParser:
    def __init__(self):
        self.valid_tags = []

    @staticmethod
    def get_html(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
            return None
        except Exception as e:
            print(f"Произошла ошибка при чтении файла '{file_path}': {str(e)}")
            return None

    def parse_tags(self, html, max_subs):
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('div', class_='row justify-content-center lm-list-container')
        if element:
            child_elements = element.find_all('div', class_='col-12 col-sm-6 col-lg-4')
            for child_element in child_elements:
                card_element = child_element.find('div',
                                                  class_='card card-body peer-item-box py-2 border mb-2 mb-sm-3 border-info-hover position-relative')
                a_element = card_element.find('a', class_='text-body')
                href = None
                if 'https://tgstat.ru/chat/' in a_element.get('href'):
                    href = a_element.get('href')[len('https://tgstat.ru/chat/'):]
                subs = int(a_element.find('b').text.replace(' ', ''))
                if subs < max_subs and href and href not in self.valid_tags:
                    self.valid_tags.append(href)

    def save_tags_to_file(self, filename='tags.txt'):
        with open(filename, 'w') as f:
            f.write('\n'.join(self.valid_tags))


if __name__ == "__main__":
    urls = input('Введите названия файлов страниц для парсинга (разделенные запятой): ').split(',')
    max_subs = int(input('Введите максимальное количество участников чата: '))
    parser = TGStatParser()

    for url in urls:
        html_content = parser.get_html(url.strip())
        if html_content:
            max_subscribers = max_subs
            parser.parse_tags(html_content, max_subscribers)

    parser.save_tags_to_file()
