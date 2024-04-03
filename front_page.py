import pytermgui as ptg

CONFIG = """
config:
    InputField:
        styles:
            prompt: dim italic
            cursor: '@72'
    Label:
        styles:
            value: dim bold

    Window:
        styles:
            border: '60'
            corner: '60'

    Container:
        styles:
            border: '96'
            corner: '96'
"""

with ptg.YamlLoader() as loader:
	loader.load(CONFIG)

host_team_name = ptg.InputField(prompt="host team name: ", name="host")
visitor_team_name = ptg.InputField(prompt="visitor team name: ", name="visitor")

OUTPUT = {}


def submit(manager: ptg.WindowManager, window: ptg.Window, stop=False) -> None:
	for widget in window:
		if isinstance(widget, ptg.InputField):
			OUTPUT[widget.prompt] = widget.value
			continue
		
		if isinstance(widget, ptg.Container):
			label, field = iter(widget)
			OUTPUT[label.value] = field.value
		
		manager.stop()


li = []
for i in range(2):
	li.append(ptg.InputField(prompt=f"{i}"))

li = tuple(li)
with ptg.WindowManager() as manager:
	window = (
		ptg.Window(
			"",
			host_team_name,
			visitor_team_name,
			"",
			li,
			"",
			["Submit", lambda *_: submit(manager, window)],
		)
	
	)
	
	window.select(0)
	manager.add(window)
