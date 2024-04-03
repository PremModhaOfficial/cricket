from dataclasses import dataclass, field


@dataclass
class Player(object):
	name: str = field(init=True)
	runs: int = field(init=False, default=0)
	over_log: dict[str] = field(default_factory=dict, init=False)
	
	def append_over(self, over_log: str):
		overs_till_now = len(self.over_log)
		self.over_log.update({str(overs_till_now + 1): over_log})
