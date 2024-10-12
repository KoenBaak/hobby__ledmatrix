from driver import MatrixDriver, Color

driver = MatrixDriver()
colors = driver.color_manager
all_blue = [[Color(red=1, green=1, blue=0)] * driver.n_rows]
driver.show_frame(all_blue)
