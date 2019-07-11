import config
import model


class Run:
    def main(self):
        c = config.Config()
        m = model.Model(c)
        for i in range(c.time_periods):
            m.step()