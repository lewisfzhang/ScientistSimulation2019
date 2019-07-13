import config
import model


def main():
    c = config.Config()
    m = model.Model(c)
    for i in range(c.time_periods):
        print('\nstep', i)
        m.step()
        c.stop_time()


if __name__ == '__main__':
    main()
