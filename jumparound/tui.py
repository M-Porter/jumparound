from threading import Thread
from typing import List
import string
from .config import Config
from .analyzer import Analyzer
from rich.console import RenderableType
from textual.app import App
from textual import events
from textual.keys import Keys
from textual.reactive import Reactive
from textual.widget import Widget


class ListBody(Widget):
    cursor_pos: Reactive[int] = Reactive(0)
    projects: Reactive[List[str]] = Reactive([])
    update_projects: Reactive[bool] = Reactive(False)

    def render(self) -> RenderableType:
        lines = []
        if self.projects:
            for x in range(min(self.console.height - 1, len(self.projects))):
                if x == self.cursor_pos:
                    lines.append(
                        f"[bold red on grey27]❯[/bold red on grey27][white on grey27] {self.projects[x]} [/white on grey27]"
                    )
                else:
                    lines.append(
                        f"[grey27 on grey27] [/grey27 on grey27] {self.projects[x]}"
                    )
        return "\n".join(lines)

    def set_cursor_pos(self, cursor_pos: int) -> None:
        self.cursor_pos = cursor_pos

    def set_projects(self, projects: List[str]) -> None:
        self.projects = projects
        self.update_projects = not self.update_projects


class InputBox(Widget):
    input_text: Reactive[str] = Reactive("")

    def render(self) -> RenderableType:
        return f"[blue]❯[/blue] {self.input_text}"

    def set_input_text(self, input_text: str) -> None:
        self.input_text = input_text


class JumpAroundApp(App):
    input_text: Reactive[str] = Reactive("")
    cursor_pos: Reactive[int] = Reactive(0)
    projects: Reactive[List[str]] = Reactive([])
    update_projects: Reactive[bool] = Reactive(False)

    input_box: InputBox
    list_body: ListBody

    analyzer: Analyzer
    config: Config

    async def on_load(self) -> None:
        self.console._highlight = False  # turn of rich's auto-highlighting
        await self.bind(Keys.Escape, "quit")

    def on_key(self, key: events.Key) -> None:
        # Handle up down cursor pos
        if key.key in [Keys.Up, Keys.Down]:
            self.log(f"cursor_pos: {self.cursor_pos}")
            if key.key == Keys.Up:
                # up == decrement
                self.cursor_pos = max(0, self.cursor_pos - 1)
            elif key.key == Keys.Down:
                # down == increment
                self.cursor_pos = min(self.console.height - 2, self.cursor_pos + 1)
            return

        # Handle text input events
        if key.key == Keys.ControlH:
            self.input_text = self.input_text[:-1]
        elif key.key == Keys.Delete:
            self.input_text = ""
        elif key.key in string.printable:
            self.input_text += key.key

    def watch_input_text(self, input_text) -> None:
        self.input_box.set_input_text(input_text)

    def watch_cursor_pos(self, cursor_pos) -> None:
        self.list_body.set_cursor_pos(cursor_pos)

    def watch_projects(self, projects) -> None:
        self.list_body.set_projects(projects)

    def set_projects(self, projects: List[str]) -> None:
        self.projects = projects
        self.update_projects = not self.update_projects

    async def on_mount(self, event: events.Mount) -> None:
        self.input_box = InputBox()
        self.list_body = ListBody()

        self.config = Config()
        self.analyzer = Analyzer(self.config)
        Thread(target=self.analyzer.run, args=(self.set_projects,)).start()

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
