from termcolor import colored


def print_progress_bar(current_value: float, profits: [], last_value: float, min_20=1, max_20=10, position_price=0,
                       fill='█', symbol='USD'):
    blocks = 31
    interval = max_20 - min_20
    block_value = interval / blocks
    profit = sum(profits)

    down_side = int((current_value - min_20) / block_value) + 1
    up_side = int((max_20 - current_value) / block_value) + 1

    down_side_bar = [fill for _ in range(down_side)]
    up_side_bar = [fill for _ in range(up_side)]

    print(f'last: {last_value} current: {current_value}')

    value_color = get_value_color(current_value, last_value)
    bar = ''.join(down_side_bar) + f'{colored(float(current_value).__round__(4), value_color)}' + ''.join(up_side_bar)

    # manager = WindowManager()
    # window = (
    #         Window(min_width=50)
    #         + [f"{symbol} trading BOT!", lambda _: manager.add(window.copy().center())]
    #         + ""
    #         + f'{colored(min_20, "red")} {bar} {colored(max_20, "green")} {symbol}'
    #         + f'profit: {colored(profit, "green" if profit >= 0 else "red")} orders: {len(profits)}'
    #         + f'in position: {position_price if position_price != 0 else colored("Negative", "red")}'
    # )
    #
    # manager.add(window)
    # manager.run()

    print(f'\r\n\n\n{colored(min_20, "red")} {bar} {colored(max_20, "green")} {symbol}\n'
          f'profit: {colored(profit, "green" if profit >= 0 else "red")} orders: {len(profits)}\n'
          f'in position: {position_price if position_price != 0 else colored("Negative", "red")} \r')


def get_value_color(current_value, last_value):
    if last_value is None or current_value is None or last_value == current_value:
        return 'white'
    elif last_value < current_value:
        return 'green'
    else:
        return 'red'

