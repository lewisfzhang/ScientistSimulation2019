import config
import model
import collect
import functions as f


def main():
    c = config.Config()
    m = model.Model(c)
    col = collect.Collect(m)
    for i in range(c.time_periods):
        print('\nstep', i)
        t = f.Time('model step')
        m.step()
        t.stop_time()
    t = f.Time('\ncollecting')
    col.collect_data()
    t.stop_time()


if __name__ == '__main__':
    main()
