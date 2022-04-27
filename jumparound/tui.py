import string
from collections import Callable
from threading import Thread
from typing import List, Union

from rich.console import RenderableType, Console
from textual import events
from textual.app import App
from textual.keys import Keys
from textual.reactive import Reactive
from textual.widget import Widget

from .analyzer import Analyzer, Project
from .config import Config
from .enum import ViewMode
from .match import match_items


class ListBody(Widget):
    cursor_pos: Union[Reactive[int], int] = Reactive(0)
    items: Union[Reactive[List[Project]], List[Project]] = Reactive([])
    config: Config

    def __init__(self, *args, config: Config = None, **kwargs):
        if not config:
            raise TypeError("ListBody() needs keyword-only argument config")
        self.config = config
        super().__init__(*args, **kwargs)

    def render(self) -> RenderableType:
        lines = []

        if self.items:
            for x in range(min(self.console.height - 1, len(self.items))):
                line = self.format_line(self.items[x])

                if x == self.cursor_pos:
                    lines.append(
                        f"[bold red on grey27]❯[/bold red on grey27][bright_white on grey27] {line} [/bright_white on grey27]"
                    )
                else:
                    lines.append(f"[grey27 on grey27] [/grey27 on grey27] {line}")

        return "\n".join(lines)

    def format_line(self, project: Project):
        view_mode = self.config.get_view_mode()
        if view_mode == ViewMode.BASIC:
            # only shows the final directory name
            return f"{project.name}"
        elif view_mode == ViewMode.COMBINED:
            # path is displayed in the format of `folder (/path/to)`
            return f"{project.name} [dim]({project.dirname})[/dim]"
        elif view_mode == ViewMode.FULL:
            # the default, shows the full path
            return f"[dim]{project.dirname}/[/dim]{project.name}"
        return project.path

    def set_cursor_pos(self, cursor_pos: int) -> None:
        self.cursor_pos = cursor_pos

    def set_list_values(self, items: List[Project]) -> None:
        self.items = items


class InputBox(Widget):
    input_text: Union[Reactive[str], str] = Reactive("")

    def render(self) -> RenderableType:
        return f"[blue]❯[/blue] {self.input_text}"

    def set_input_text(self, input_text: str) -> None:
        self.input_text = input_text


class JumpAroundApp(App):
    on_quit_callback: Callable[[Union[Project, None]], None] = None

    input_text: Union[Reactive[str], str] = Reactive("")
    cursor_pos: Union[Reactive[int], int] = Reactive(0)
    projects: Union[Reactive[List[Project]], List[Project]] = Reactive([])
    filtered_projects: Union[Reactive[List[Project]], List[Project]] = Reactive([])

    input_box: InputBox
    list_body: ListBody

    analyzer: Analyzer
    config: Config

    def __init__(
        self,
        *args,
        on_quit_callback: Callable[[Union[Project, None]], None] = None,
        **kwargs,
    ):
        self.on_quit_callback = on_quit_callback
        super().__init__(*args, **kwargs)

    async def on_load(self) -> None:
        await self.bind(Keys.Escape, "quit")
        await self.bind(Keys.ControlI, "rotate_view_mode")
        await self.bind(Keys.Up, "move_cursor_up")
        await self.bind(Keys.Down, "move_cursor_down")
        await self.bind(Keys.Enter, "callback_and_quit")

    async def action_callback_and_quit(self):
        try:
            self.on_quit_callback(self.filtered_projects[self.cursor_pos])
        except IndexError:
            self.on_quit_callback(None)
        await self.action_quit()

    def action_move_cursor_up(self):
        self.cursor_pos = max(0, self.cursor_pos - 1)

    def action_move_cursor_down(self):
        max_h = min(len(self.projects) - 1, self.console.height - 2)
        self.cursor_pos = min(max_h, self.cursor_pos + 1)

    def action_rotate_view_mode(self):
        self.config.next_view_mode()
        self.list_body.refresh()

    async def on_key(self, key: events.Key) -> None:
        # Handle text input events
        if key.key == Keys.ControlH:  # backspace / delete
            self.input_text = self.input_text[:-1]
        elif key.key == Keys.Delete:
            self.input_text = ""
        elif key.key in string.printable:
            self.input_text += key.key

    def watch_input_text(self, input_text) -> None:
        self.cursor_pos = 0
        self.input_box.set_input_text(input_text)
        self.do_search()

    def watch_cursor_pos(self, cursor_pos) -> None:
        self.list_body.set_cursor_pos(cursor_pos)

    def watch_filtered_projects(self, filtered_projects) -> None:
        self.list_body.set_list_values(filtered_projects)

    def set_projects(self, projects: List[Project]) -> None:
        self.projects = projects
        self.do_search()

    def do_search(self):
        if not self.input_text.strip():
            self.filtered_projects = self.projects
        elif self.projects and len(self.projects) > 0:
            self.filtered_projects = match_items(self.input_text, self.projects)
        else:
            self.filtered_projects = self.projects

    async def on_mount(self, event: events.Mount) -> None:
        self.config = Config()

        self.analyzer = Analyzer(self.config)
        Thread(
            target=self.analyzer.run,
            kwargs={
                "callback": self.set_projects,
                "use_cache": True,
            },
        ).start()

        self.input_box = InputBox()
        self.list_body = ListBody(config=self.config)

        grid = await self.view.dock_grid(edge="left", name="left")

        grid.add_column(name="body")

        grid.add_row(size=1, name="input")
        grid.add_row(name="list")

        grid.add_areas(
            areaInputBox="body,input",
            areaListBody="body,list",
        )

        grid.place(
            areaInputBox=self.input_box,
            areaListBody=self.list_body,
        )
