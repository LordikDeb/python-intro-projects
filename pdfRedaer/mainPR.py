import remi.gui as gui
from remi import start, App
from Reader import Reader
from Ttranslate import *
import pyperclip
import pyautogui

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def copy_clipboard(self, *args):

        pyperclip.copy("")
        pyautogui.hotkey('ctrl', 'c')
        self.clipboard = pyperclip.paste()

    def print_translate(self, *args):
        self.translated_txt.set_text(translate(self.clipboard,"en","ru"))

    def print_paraphraze(self, *args):
        self.translated_txt.set_text(paraphrase(self.clipboard))

    def print_summarize(self, *args):
        self.translated_txt.set_text(summarize(self.clipboard))

    def main(self):
        self.clipboard = ''
        self.full_text = 'Для начала выберите pdf файл, для этого нажмите на кнопку ниже'
        verticalContainer = gui.Container(width='100%', margin='0px auto',
                                          style={'display': 'block', 'overflow': 'hidden'})

        self.horizontalContainer = gui.Container(width='100%', layout_orientation=gui.Container.LAYOUT_HORIZONTAL,
                                                 margin='0px', style={'display': 'block', 'overflow': 'auto'})

        self.lbl = gui.Label('Переводчик', width="95%", height=30, margin='10px',style={'text-align': 'center', 'font-size': '30px', 'background':'99CCCC'})
        #Заголовок и его настройка (проверка работы remi как css редактор)


        self.full_txt = gui.TextInput(width="40%", height="600", margin='2%',style = {'font-size': '20px', 'text-align': 'justify'})
        self.full_txt.set_text(self.full_text)
        #Текст из файла pdf, текст задается из writing_fulltext


        self.translated_txt = gui.TextInput(width="40%", height="600", margin='2%',
                                            style={'font-family': 'Time New Roman', 'font-size': '24px',
                                                   'text-align': 'justify'})
        self.translated_txt.set_text("Здесь высветится перевод, просто выделите текст и нажмите на кнопку")
        #Блок для текста перевода/перефразы/и тд и тп
        self.Buttons = gui.Container(width='10%', margin='0px auto',
                                          style={'display': 'block', 'overflow': 'hidden'})
        self.bt_translate = gui.Button('ПЕРЕВЕСТИ', width ='95%', height='25px', margin='1%', style={'margin-top': '50px', 'font-size':'18px', 'background':'#662E1C'})
        #Добавление кнопки перевода текста

        self.bt_paraphrase = gui.Button('ПЕРЕФРАЗА', width='95%', height='25px', margin='1%',
                                       style={'margin-top': '50px', "display": "block", "alt": "", 'font-size': '18px', 'background': '#662E1C'})
        # Добавление кнопки перефразы текста

        self.bt_summarize = gui.Button('ПЕРЕСКАЗАТЬ', width='95%', height='25px', margin='1%',
                                       style={'margin-top': '50px', "display": "block", "alt": "", 'font-size': '18px', 'background': '#662E1C'})
        # Добавление кнопки пересказа текста

        self.full_txt.onmouseup.do(self.copy_clipboard)
        #Реакция экрана на выделение текста

        self.bt_FileDialog = gui.Button('Выбрать PDF файл', width=200, height=30, margin='10px')
        self.bt_FileDialog.onclick.do(self.open_fileselection_dialog)
        #Кнопка выбора файла
        self.btUploadFile = gui.FileUploader('./', width=200, height=30, margin='10px')
        self.btUploadFile.onsuccess.do(self.fileupload_on_success)
        self.btUploadFile.onfailed.do(self.fileupload_on_failed)
        #Аоооэээ, загрузчик файла
        self.link = gui.Link("http://localhost:8081", "A link to here", width=200, height=30, margin='10px')

        self.dropDown = gui.DropDown.new_from_list(('DropDownItem 0', 'DropDownItem 1'),
                                                   width=200, height=20, margin='10px')
        self.dropDown.onchange.do(self.drop_down_changed)
        self.dropDown.select_by_value('DropDownItem 0')

        self.slider = gui.Slider(10, 0, 100, 5, width=200, height=20, margin='10px')
        self.slider.onchange.do(self.slider_changed)

        self.colorPicker = gui.ColorPicker('#ffbb00', width=200, height=20, margin='10px')
        self.colorPicker.onchange.do(self.color_picker_changed)

        self.date = gui.Date('2015-04-13', width=200, height=20, margin='10px')
        self.date.onchange.do(self.date_changed)


        self.horizontalContainer.append(self.lbl)
        self.horizontalContainer.append(self.full_txt)
        self.Buttons.append(self.bt_translate)
        self.Buttons.append(self.bt_paraphrase)
        self.Buttons.append(self.bt_summarize)
        self.horizontalContainer.append(self.Buttons)
        self.horizontalContainer.append(self.translated_txt)
        self.horizontalContainer.append(self.bt_FileDialog)

        verticalContainer.append(self.horizontalContainer)

        self.bt_translate.onclick.do(self.print_translate)
        self.bt_paraphrase.onclick.do(self.print_paraphraze)
        self.bt_summarize.onclick.do(self.print_summarize)

        return verticalContainer
    def open_fileselection_dialog(self, widget):
        self.fileselectionDialog = gui.FileSelectionDialog('File Selection Dialog', 'Select files and folders',
                                                           False,
                                                           '.')

        self.fileselectionDialog.confirm_value.do(
            self.on_fileselection_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.fileselectionDialog.show(self)

    def on_fileselection_dialog_confirm(self, widget, filelist):
        self.lbl.set_text(','.join(filelist))
        if len(filelist):
            self.full_text = Reader(filelist[0]).content
            self.full_txt.set_text(self.full_text)


    def menu_dialog_clicked(self, widget):
        self.dialog = gui.GenericDialog(title='Dialog Box', message='Click Ok to transfer content to main page', width='500px')
        self.dtextinput = gui.TextInput(width=200, height=30)
        self.dtextinput.set_value('Initial Text')
        self.dialog.add_field_with_label('dtextinput', 'Text Input', self.dtextinput)

        self.dcheck = gui.CheckBox(False, width=200, height=30)
        self.dialog.add_field_with_label('dcheck', 'Label Checkbox', self.dcheck)
        values = ('Danny Young', 'Christine Holand', 'Lars Gordon', 'Roberto Robitaille')
        self.dlistView = gui.ListView.new_from_list(values, width=200, height=120)
        self.dialog.add_field_with_label('dlistView', 'Listview', self.dlistView)

        self.ddropdown = gui.DropDown.new_from_list(('DropDownItem 0', 'DropDownItem 1'),
                                                    width=200, height=20)
        self.dialog.add_field_with_label('ddropdown', 'Dropdown', self.ddropdown)

        self.dspinbox = gui.SpinBox(min=0, max=5000, width=200, height=20)
        self.dspinbox.set_value(50)
        self.dialog.add_field_with_label('dspinbox', 'Spinbox', self.dspinbox)

        self.dslider = gui.Slider(10, 0, 100, 5, width=200, height=20)

        self.dialog.add_field_with_label('dslider', 'Slider', self.dslider)


        self.dialog.confirm_dialog.do(self.dialog_confirm)
        self.dialog.show(self)
    def dialog_confirm(self, widget):
        result = self.dialog.get_field('dtextinput').get_value()
        self.full_txt.set_value(result)

        result = self.dialog.get_field('dcheck').get_value()
        self.check.set_value(result)

        result = self.dialog.get_field('ddropdown').get_value()
        self.dropDown.select_by_value(result)

        result = self.dialog.get_field('dspinbox').get_value()
        self.spin.set_value(result)

        result = self.dialog.get_field('dslider').get_value()
        self.slider.set_value(result)

        result = self.dialog.get_field('dcolor').get_value()
        self.colorPicker.set_value(result)

        result = self.dialog.get_field('ddate').get_value()
        self.date.set_value(result)

        result = self.dialog.get_field('dlistView').get_value()
        self.listView.select_by_value(result)

    def drop_down_changed(self, widget, value):
        self.lbl.set_text('New Combo value: ' + value)

    def slider_changed(self, widget, value):
        self.lbl.set_text('New slider value: ' + str(value))

    def color_picker_changed(self, widget, value):
        self.lbl.set_text('New color value: ' + value)

    def date_changed(self, widget, value):
        self.lbl.set_text('New date value: ' + value)

    def menu_save_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Save')

    def menu_saveas_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Save As')

    def menu_open_clicked(self, widget):
        self.lbl.set_text('Menu clicked: Open')

    def fileupload_on_success(self, widget, filename):
        self.lbl.set_text('File upload success: ' + filename)

    def fileupload_on_failed(self, widget, filename):
        self.lbl.set_text('File upload failed: ' + filename)

    def on_close(self):

        self.stop_flag = True
        super(MyApp, self).on_close()

if __name__ == "__main__":
    start(MyApp, debug=True, address='0.0.0.0', port=8081, start_browser=True, multiple_instance=True)


