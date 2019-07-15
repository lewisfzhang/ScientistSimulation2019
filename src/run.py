import config
import model
import functions as f


def main():
    c = config.Config()
    m = model.Model(c)
    for i in range(c.time_periods):
        print('\nstep', i)
        t = f.Time('model step')
        m.step()
        t.stop_time()

    t = f.Time('\ncollecting')
    m.collect_data()
    t.stop_time()


if __name__ == '__main__':
    main()
