from driver import MatrixDriver, Color

driver = MatrixDriver(n_color_bits=8)
colors = driver.color_manager
all_blue = [[Color(red=255, green=102, blue=178)] * driver.n_rows] * driver.n_cols
driver.show_frame(all_blue)
