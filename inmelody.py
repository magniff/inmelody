import yaml
import watch
import click

from libtunes import networking
from libtunes import ui
from libtunes import playback


class Config(watch.WatchMe):
    app_id = watch.builtins.InstanceOf(int)
    login = watch.builtins.InstanceOf(str)
    password = watch.builtins.InstanceOf(str)

    def __init__(self, dictionary):
        self.app_id = dictionary.get('APP_ID')
        self.login = dictionary.get('LOGIN')
        self.password = dictionary.get('PASSWORD')


@click.command()
@click.option('-c', '--config', type=click.File(), required=True)
def vktunes(config):
    config_object = Config(yaml.load(config))
    api_object = networking.create_api_handler(config_object)
    getter = networking.AudioGet(api_object)
    _, *audios = getter.call_api()
    records = [playback.AudioRecord(item) for item in audios]
    left = ui.UIFiltrableRecordList(records=records, album_name="ALL RECORDS")
    right = ui.UIFiltrableRecordList(records=records, album_name="ALL RECORDS")
    columns = ui.UIDoubleColumnFiltrableList(left, right)
    app = ui.UIApplication(ui.UIMainFrame(columns))
    palette = [
        ('focused', 'white,bold', 'dark green', 'bold'),
        ('unfocused', 'light gray', 'black', 'bold'),
    ]
    app.run_mainloop(palette)


if __name__ == '__main__':
    vktunes()
