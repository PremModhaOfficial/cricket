from dataclasses import dataclass, field


@dataclass
class Player(object):
    name: str = field(init=True)
    runs: int = field(init=False, default=0)
    run_log: list[str] = field(init=False, default_factory=list)
    over_log: dict[str] = field(default_factory=dict, init=False)
    wicket_log: str = field(default_factory=str, init=False)
    is_out: bool = field(init=False, default=False)

    def append_over(self, over_log: str):
        overs_till_now = len(self.over_log)
        self.over_log.update({str(overs_till_now + 1): over_log})

    def update_runs(self, runs: int, ball_info: str):
        self.runs += int(runs)
        log = (ball_info.split(" "))
        self.run_log.append(log[0] + " " + log[1])