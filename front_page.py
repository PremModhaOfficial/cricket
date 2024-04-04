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


def submit(my_manager: ptg.WindowManager, my_window: ptg.Window, another: ptg.Window) -> None:
	for widget in my_window:
		if isinstance(widget, ptg.InputField):
			OUTPUT[widget.prompt] = widget.value
			continue
		
		if isinstance(widget, ptg.Container):
			label, field = iter(widget)
			OUTPUT[label.value] = field.value
		
		my_manager.focus(another)


with ptg.WindowManager() as manager:
	window = (
		ptg.Window(
			"",
			host_team_name,
			visitor_team_name,
			"",
			"",
			["Submit", lambda *_: submit(manager, window, windowb)],
		)
	
	)
	
	window.select(0)
	manager.add(window)

with ptg.WindowManager() as manager:
	windowb = (
		ptg.Window(
			"",
			host_team_name,
			visitor_team_name,
			"",
			'2',
			"",
			["Submit", lambda *_: submit(manager, windowb, window)],
		)
	
	)
	
	windowb.select(0)
	manager.add(windowb)
